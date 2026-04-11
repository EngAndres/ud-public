"""
PPO Agent — Proximal Policy Optimization
Actor-Critic implementation for discrete action spaces (LunarLander-v2).
Here are some concepts from the course, the last we see for optimal policies:
  - Clipped surrogate objective (ε-clip)
  - Generalized Advantage Estimation (GAE, λ)
  - Shared feature extractor, separate policy/value heads
  - Entropy bonus for exploration

Reference: Schulman et al. 2017 — "Proximal Policy Optimization Algorithms"

Author: Carlos Andrés Sierra <cavirguezs@udistrital.edu.co>
"""

import numpy as np
import torch
import torch.nn as nn
import torch.optim as optim
from torch.distributions import Categorical


class ActorCritic(nn.Module):
    """Shared backbone with separate policy (actor) and value (critic) heads.
    Here is where """

    def __init__(self, obs_dim: int, act_dim: int, hidden_dim: int = 256):
        super().__init__()

        # Shared feature extractor
        self.shared = nn.Sequential(
            nn.Linear(obs_dim, hidden_dim),
            nn.Tanh(),
            nn.Linear(hidden_dim, hidden_dim),
            nn.Tanh(),
        )

        # Policy head — outputs logits over actions
        self.actor_head = nn.Linear(hidden_dim, act_dim)

        # Value head — outputs a scalar state value V(s)
        self.critic_head = nn.Linear(hidden_dim, 1)

        # Orthogonal initialization (improves stability)
        self._init_weights()

    def _init_weights(self):
        for layer in self.shared:
            if isinstance(layer, nn.Linear):
                nn.init.orthogonal_(layer.weight, gain=np.sqrt(2))
                nn.init.zeros_(layer.bias)
        nn.init.orthogonal_(self.actor_head.weight, gain=0.01)
        nn.init.zeros_(self.actor_head.bias)
        nn.init.orthogonal_(self.critic_head.weight, gain=1.0)
        nn.init.zeros_(self.critic_head.bias)

    def forward(self, obs: torch.Tensor):
        features = self.shared(obs)
        logits = self.actor_head(features)
        value = self.critic_head(features).squeeze(-1)
        return logits, value

    def get_action_and_value(self, obs: torch.Tensor, action=None):
        """Sample (or evaluate) an action and return log-prob, entropy, value."""
        logits, value = self(obs)
        dist = Categorical(logits=logits)
        if action is None:
            action = dist.sample()
        return action, dist.log_prob(action), dist.entropy(), value

    def get_value(self, obs: torch.Tensor) -> torch.Tensor:
        _, value = self(obs)
        return value


# ─── Rollout Buffer ───────────────────────────────────────────────────────────

class RolloutBuffer:
    """Stores one horizon of experience; computes returns & GAE advantages."""

    def __init__(self, horizon: int, obs_dim: int, device: torch.device):
        self.horizon = horizon
        self.device = device

        self.obs = torch.zeros(horizon, obs_dim, device=device)
        self.actions = torch.zeros(horizon, dtype=torch.long, device=device)
        self.log_probs = torch.zeros(horizon, device=device)
        self.rewards = torch.zeros(horizon, device=device)
        self.values = torch.zeros(horizon, device=device)
        self.dones = torch.zeros(horizon, device=device)

        self.ptr = 0

    def store(self, obs, action, log_prob, reward, value, done):
        self.obs[self.ptr] = obs
        self.actions[self.ptr] = action
        self.log_probs[self.ptr] = log_prob
        self.rewards[self.ptr] = reward
        self.values[self.ptr] = value
        self.dones[self.ptr] = done
        self.ptr += 1

    def is_full(self) -> bool:
        return self.ptr >= self.horizon

    def compute_advantages(
        self,
        last_value: torch.Tensor,
        gamma: float,
        gae_lambda: float,
    ) -> tuple[torch.Tensor, torch.Tensor]:
        """Returns (advantages, returns) using GAE(γ, λ)."""
        advantages = torch.zeros_like(self.rewards)
        last_gae = 0.0

        for t in reversed(range(self.horizon)):
            if t == self.horizon - 1:
                next_non_terminal = 1.0 - self.dones[t]
                next_value = last_value
            else:
                next_non_terminal = 1.0 - self.dones[t]
                next_value = self.values[t + 1]

            delta = (
                self.rewards[t]
                + gamma * next_value * next_non_terminal
                - self.values[t]
            )
            last_gae = delta + gamma * gae_lambda * next_non_terminal * last_gae
            advantages[t] = last_gae

        returns = advantages + self.values
        return advantages, returns

    def reset(self):
        self.ptr = 0

    def get(self) -> dict:
        return {
            "obs": self.obs,
            "actions": self.actions,
            "log_probs": self.log_probs,
            "values": self.values,
        }


# ─── PPO Agent ────────────────────────────────────────────────────────────────

class PPOAgent:
    """
    Proximal Policy Optimization agent.

    Hyperparameters (all exposed in __init__):
      horizon        — steps collected per update (T)
      n_epochs       — gradient update passes per horizon
      batch_size     — mini-batch size
      gamma          — discount factor
      gae_lambda     — GAE smoothing parameter
      clip_eps       — PPO clip epsilon
      vf_coef        — value-function loss coefficient
      ent_coef       — entropy bonus coefficient
      max_grad_norm  — gradient clipping
      lr             — Adam learning rate
    """

    def __init__(
        self,
        obs_dim: int,
        act_dim: int,
        horizon: int = 2048,
        n_epochs: int = 10,
        batch_size: int = 64,
        gamma: float = 0.99,
        gae_lambda: float = 0.95,
        clip_eps: float = 0.2,
        vf_coef: float = 0.5,
        ent_coef: float = 0.01,
        max_grad_norm: float = 0.5,
        lr: float = 3e-4,
        hidden_dim: int = 256,
        device: str = "auto",
    ):
        if device == "auto":
            self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        else:
            self.device = torch.device(device)

        self.horizon = horizon
        self.n_epochs = n_epochs
        self.batch_size = batch_size
        self.gamma = gamma
        self.gae_lambda = gae_lambda
        self.clip_eps = clip_eps
        self.vf_coef = vf_coef
        self.ent_coef = ent_coef
        self.max_grad_norm = max_grad_norm

        self.network = ActorCritic(obs_dim, act_dim, hidden_dim).to(self.device)
        self.optimizer = optim.Adam(self.network.parameters(), lr=lr, eps=1e-5)

        self.buffer = RolloutBuffer(horizon, obs_dim, self.device)

    # ── Interaction ──────────────────────────────────────────────────────────

    @torch.no_grad()
    def select_action(self, obs: np.ndarray):
        """Return (action, log_prob, value) as Python scalars / numpy."""
        obs_t = torch.tensor(obs, dtype=torch.float32, device=self.device).unsqueeze(0)
        action, log_prob, _, value = self.network.get_action_and_value(obs_t)
        return (
            action.item(),
            log_prob.item(),
            value.item(),
        )

    def store_transition(self, obs, action, log_prob, reward, value, done):
        obs_t = torch.tensor(obs, dtype=torch.float32, device=self.device)
        self.buffer.store(
            obs_t,
            torch.tensor(action, device=self.device),
            torch.tensor(log_prob, device=self.device),
            torch.tensor(reward, dtype=torch.float32, device=self.device),
            torch.tensor(value, dtype=torch.float32, device=self.device),
            torch.tensor(float(done), device=self.device),
        )

    # ── Learning ─────────────────────────────────────────────────────────────

    def update(self, last_obs: np.ndarray) -> dict:
        """Run n_epochs of mini-batch gradient updates. Returns loss stats."""
        # Bootstrap value for last state
        with torch.no_grad():
            last_obs_t = torch.tensor(
                last_obs, dtype=torch.float32, device=self.device
            ).unsqueeze(0)
            last_value = self.network.get_value(last_obs_t).squeeze()

        advantages, returns = self.buffer.compute_advantages(
            last_value, self.gamma, self.gae_lambda
        )

        # Normalize advantages
        advantages = (advantages - advantages.mean()) / (advantages.std() + 1e-8)

        # Collect all data
        b_obs = self.buffer.obs
        b_actions = self.buffer.actions
        b_old_log_probs = self.buffer.log_probs
        b_returns = returns
        b_advantages = advantages

        # Mini-batch SGD over n_epochs
        stats = {"policy_loss": [], "value_loss": [], "entropy": [], "approx_kl": []}
        indices = np.arange(self.horizon)

        for _ in range(self.n_epochs):
            np.random.shuffle(indices)
            for start in range(0, self.horizon, self.batch_size):
                mb_idx = indices[start : start + self.batch_size]
                mb_idx_t = torch.tensor(mb_idx, device=self.device)

                _, new_log_probs, entropy, new_values = (
                    self.network.get_action_and_value(
                        b_obs[mb_idx_t], b_actions[mb_idx_t]
                    )
                )

                log_ratio = new_log_probs - b_old_log_probs[mb_idx_t]
                ratio = log_ratio.exp()

                # Approximate KL for diagnostics
                with torch.no_grad():
                    approx_kl = ((ratio - 1) - log_ratio).mean()

                mb_adv = b_advantages[mb_idx_t]

                # Clipped surrogate objective
                surr1 = ratio * mb_adv
                surr2 = torch.clamp(ratio, 1 - self.clip_eps, 1 + self.clip_eps) * mb_adv
                policy_loss = -torch.min(surr1, surr2).mean()

                # Value loss (clipped)
                mb_returns = b_returns[mb_idx_t]
                value_loss = 0.5 * ((new_values - mb_returns) ** 2).mean()

                # Entropy bonus
                entropy_loss = -entropy.mean()

                loss = policy_loss + self.vf_coef * value_loss + self.ent_coef * entropy_loss

                self.optimizer.zero_grad()
                loss.backward()
                nn.utils.clip_grad_norm_(self.network.parameters(), self.max_grad_norm)
                self.optimizer.step()

                stats["policy_loss"].append(policy_loss.item())
                stats["value_loss"].append(value_loss.item())
                stats["entropy"].append(-entropy_loss.item())
                stats["approx_kl"].append(approx_kl.item())

        self.buffer.reset()
        return {k: float(np.mean(v)) for k, v in stats.items()}

    # ── Persistence ──────────────────────────────────────────────────────────

    def save(self, path: str):
        torch.save(
            {
                "network": self.network.state_dict(),
                "optimizer": self.optimizer.state_dict(),
            },
            path,
        )

    def load(self, path: str):
        ckpt = torch.load(path, map_location=self.device, weights_only=True)
        self.network.load_state_dict(ckpt["network"])
        self.optimizer.load_state_dict(ckpt["optimizer"])

    @torch.no_grad()
    def predict(self, obs: np.ndarray) -> int:
        """Greedy (deterministic) action — used for evaluation."""
        obs_t = torch.tensor(obs, dtype=torch.float32, device=self.device).unsqueeze(0)
        logits, _ = self.network(obs_t)
        return logits.argmax(dim=-1).item()
