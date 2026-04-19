"""
PPO Agent — Proximal Policy Optimization
Actor-Critic implementation for discrete action spaces (LunarLander-v3).
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
from typing import Dict, Optional, Tuple


class ActorCritic(nn.Module):
    """Shared backbone with separate policy (actor) and value (critic) heads.
    Both the actor and the critic are neural networks with two hidden layers
    and Tanh activations.
    The actor outputs logits for a categorical distribution over actions,
    while the critic outputs a scalar value estimate for the input state.
    """

    def __init__(self, obs_dim: int, act_dim: int, hidden_dim: int = 256) -> None:
        """Build the shared feature extractor and the policy/value heads.

        Args:
            obs_dim (int): Number of observation features in the environment state.
            act_dim (int): Number of discrete actions available to the agent.
            hidden_dim (int): Width of the shared hidden layers.
        """
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

    def _init_weights(self) -> None:
        """Initialize linear layers orthogonally for stable RL optimization."""
        for layer in self.shared:
            if isinstance(layer, nn.Linear):
                nn.init.orthogonal_(layer.weight, gain=np.sqrt(2))
                nn.init.zeros_(layer.bias)
        nn.init.orthogonal_(self.actor_head.weight, gain=0.01)
        nn.init.zeros_(self.actor_head.bias)
        nn.init.orthogonal_(self.critic_head.weight, gain=1.0)
        nn.init.zeros_(self.critic_head.bias)

    def forward(self, obs: torch.Tensor) -> Tuple[torch.Tensor, torch.Tensor]:
        """Forward pass through the network.

        Args:
            obs (torch.Tensor): Input observations with shape ``(batch_size, obs_dim)``.

        Returns:
            A tuple containing:
                logits: Action logits with shape ``(batch_size, act_dim)``.
                value: State-value estimates with shape ``(batch_size,)``.
        """
        features = self.shared(obs)
        logits = self.actor_head(features)
        value = self.critic_head(features).squeeze(-1)
        return logits, value

    def get_action_and_value(
        self, obs: torch.Tensor, action: Optional[torch.Tensor] = None
    ) -> Tuple[torch.Tensor, torch.Tensor, torch.Tensor, torch.Tensor]:
        """Sample (or evaluate) an action and return log-prob, entropy, value.

        Args:
            obs (torch.Tensor): Input observations with shape ``(batch_size, obs_dim)``.
            action (Optional[torch.Tensor]): Optional actions with shape ``(batch_size,)``. When omitted,
                actions are sampled from the policy distribution.

        Returns:
            A tuple containing:
                action: Sampled or provided actions.
                log_prob: Log probability of each action.
                entropy: Entropy of the policy distribution.
                value: State-value estimates.
        """
        logits, value = self(obs)
        dist = Categorical(logits=logits)
        if action is None:
            action = dist.sample()
        return action, dist.log_prob(action), dist.entropy(), value

    def get_value(self, obs: torch.Tensor) -> torch.Tensor:
        """Compute the critic value estimate for a batch of observations.

        Args:
            obs (torch.Tensor): Input observations with shape ``(batch_size, obs_dim)``.

        Returns:
            State-value estimates with shape ``(batch_size,)``.
        """
        _, value = self(obs)
        return value


class RolloutBuffer:
    """Stores one horizon of experience; computes returns & GAE advantages.
    Horizon is the number of environment steps collected before each PPO update.
    Advantages are the GAE estimates used for the policy loss, while returns are the
    bootstrapped targets for the value loss.
    GAE (Generalized Advantage Estimation) is a method to compute advantage estimates
    that balances bias and variance using a λ parameter. It uses the rewards,
    value estimates, and done flags to compute the advantages in a backward-looking manner.
    """

    def __init__(self, horizon: int, obs_dim: int, device: torch.device) -> None:
        """Allocate rollout storage for a fixed number of environment steps.

        Args:
            horizon (int): Number of transitions to store before each PPO update.
            obs_dim (int): Dimension of each observation vector.
            device (torch.device): Torch device used to store the tensors.
        """
        self.horizon = horizon
        self.device = device

        self.obs = torch.zeros(horizon, obs_dim, device=device)
        self.actions = torch.zeros(horizon, dtype=torch.long, device=device)
        self.log_probs = torch.zeros(horizon, device=device)
        self.rewards = torch.zeros(horizon, device=device)
        self.values = torch.zeros(horizon, device=device)
        self.dones = torch.zeros(horizon, device=device)

        self.ptr = 0

    def store(
        self,
        obs: torch.Tensor,
        action: torch.Tensor,
        log_prob: torch.Tensor,
        reward: torch.Tensor,
        value: torch.Tensor,
        done: torch.Tensor,
    ) -> None:
        """Store a single transition in the buffer.

        Args:
            obs (torch.Tensor): Observation tensor with shape ``(obs_dim,)``.
            action (torch.Tensor): Action taken at the current step.
            log_prob (torch.Tensor): Log probability of the sampled action.
            reward (torch.Tensor): Reward observed after the action.
            value (torch.Tensor): Critic value estimate for the observation.
            done (torch.Tensor): Terminal flag stored as ``0.0`` or ``1.0``.
        """
        self.obs[self.ptr] = obs
        self.actions[self.ptr] = action
        self.log_probs[self.ptr] = log_prob
        self.rewards[self.ptr] = reward
        self.values[self.ptr] = value
        self.dones[self.ptr] = done
        self.ptr += 1

    def is_full(self) -> bool:
        """Return ``True`` when the rollout horizon has been collected.

        Returns:
            ``True`` if the buffer has collected ``horizon`` transitions.
        """
        return self.ptr >= self.horizon

    def compute_advantages(
        self,
        last_value: torch.Tensor,
        gamma: float,
        gae_lambda: float,
    ) -> Tuple[torch.Tensor, torch.Tensor]:
        """Compute GAE advantages and bootstrapped returns for the rollout.

        Args:
            last_value: Value estimate for the observation following the last stored step.
            gamma: Discount factor applied to future rewards.
            gae_lambda: GAE smoothing parameter controlling the bias-variance trade-off.

        Returns:
            A tuple containing:
                advantages: Advantage estimates for each stored transition.
                returns: Bootstrapped returns computed as ``advantages + values``.
        """
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

    def reset(self) -> None:
        """Reset the write pointer before collecting the next rollout."""
        self.ptr = 0

    def get(self) -> Dict[str, torch.Tensor]:
        """Return the stored rollout tensors in a dictionary.

        Returns:
            A dictionary with the stored observations, actions, log probabilities,
            and value estimates.
        """
        return {
            "obs": self.obs,
            "actions": self.actions,
            "log_probs": self.log_probs,
            "values": self.values,
        }


class PPOAgent:
    """
    Proximal Policy Optimization agent. This one is designed for discrete action spaces (like LunarLander-v2) and uses an
    Actor-Critic architecture.

    Hyperparameters:
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
    ) -> None:
        """Create the PPO policy, optimizer, and rollout buffer.

        Args:
            obs_dim: Dimension of the observation vector.
            act_dim: Number of discrete actions.
            horizon: Number of environment steps per PPO update.
            n_epochs: Number of optimization epochs per rollout.
            batch_size: Mini-batch size used during optimization.
            gamma: Discount factor for returns.
            gae_lambda: GAE smoothing parameter.
            clip_eps: PPO clipping range.
            vf_coef: Weight applied to the value loss.
            ent_coef: Weight applied to the entropy bonus.
            max_grad_norm: Gradient-clipping threshold.
            lr: Learning rate for Adam.
            hidden_dim: Width of the shared hidden layers.
            device: Device string or ``"auto"`` for CUDA/CPU selection.
        """
        if device == "auto":
            # this just is to activate the use GPU if available, otherwise use CPU
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

    @torch.no_grad()
    def select_action(self, obs: np.ndarray) -> Tuple[int, float, float]:
        """Sample an action from the current policy for environment interaction.

        Args:
            obs: Current environment observation.

        Returns:
            A tuple containing:
                action: Sampled discrete action.
                log_prob: Log probability of the sampled action.
                value: Critic value estimate for the observation.
        """
        obs_t = torch.tensor(obs, dtype=torch.float32, device=self.device).unsqueeze(0)
        action, log_prob, _, value = self.network.get_action_and_value(obs_t)
        return (
            action.item(),
            log_prob.item(),
            value.item(),
        )

    def store_transition(
        self,
        obs: np.ndarray,
        action: int,
        log_prob: float,
        reward: float,
        value: float,
        done: bool,
    ) -> None:
        """Copy one environment transition into the rollout buffer.

        Args:
            obs: Observation before the action was taken.
            action: Action applied to the environment.
            log_prob: Log probability returned by :meth:`select_action`.
            reward: Scalar reward from the environment step.
            value: Critic estimate for ``obs``.
            done: Whether the episode terminated or truncated after the step.
        """
        obs_t = torch.tensor(obs, dtype=torch.float32, device=self.device)
        self.buffer.store(
            obs_t,
            torch.tensor(action, device=self.device),
            torch.tensor(log_prob, device=self.device),
            torch.tensor(reward, dtype=torch.float32, device=self.device),
            torch.tensor(value, dtype=torch.float32, device=self.device),
            torch.tensor(float(done), device=self.device),
        )

    def update(self, last_obs: np.ndarray) -> Dict[str, float]:
        """Update the policy and value networks using the collected rollout.
        This is the learning step of PPO.

        Args:
            last_obs: Observation reached after collecting the current rollout.

        Returns:
            Dictionary with mean policy loss, value loss, entropy, and approximate KL.
        """
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
                surr2 = (
                    torch.clamp(ratio, 1 - self.clip_eps, 1 + self.clip_eps) * mb_adv
                )
                policy_loss = -torch.min(surr1, surr2).mean()

                # Value loss (clipped)
                mb_returns = b_returns[mb_idx_t]
                value_loss = 0.5 * ((new_values - mb_returns) ** 2).mean()

                # Entropy bonus
                entropy_loss = -entropy.mean()

                loss = (
                    policy_loss
                    + self.vf_coef * value_loss
                    + self.ent_coef * entropy_loss
                )

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

    def save(self, path: str) -> None:
        """Save the policy network and optimizer state to disk.

        Args:
            path: Destination file path for the checkpoint.
        """
        torch.save(
            {
                "network": self.network.state_dict(),
                "optimizer": self.optimizer.state_dict(),
            },
            path,
        )

    def load(self, path: str) -> None:
        """Load the policy network and optimizer state from disk.

        Args:
            path: Checkpoint file produced by :meth:`save`.
        """
        ckpt = torch.load(path, map_location=self.device, weights_only=True)
        self.network.load_state_dict(ckpt["network"])
        self.optimizer.load_state_dict(ckpt["optimizer"])

    @torch.no_grad()
    def predict(self, obs: np.ndarray) -> int:
        """Return the greedy action for evaluation.

        Args:
            obs: Current environment observation.

        Returns:
            The action index with the highest policy logit.
        """
        obs_t = torch.tensor(obs, dtype=torch.float32, device=self.device).unsqueeze(0)
        logits, _ = self.network(obs_t)
        return logits.argmax(dim=-1).item()
