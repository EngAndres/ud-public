"""
This module trains a PPO agent on the LunarLander-v2 environment from OpenAI Gymnasium.

Run:
    python train.py
    python train.py --total-steps 500000     # longer run
    python train.py --no-plot      # skip live chart

Saved artifacts:
    checkpoints/ppo_lunarlander_best.pt   — best model by episode reward
    checkpoints/ppo_lunarlander_final.pt  — model at end of training
    results/training_curve.png            — reward & episode-length curves
"""

import argparse
import os
import random
import time

import gymnasium as gym
import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import torch

matplotlib.use("Agg")

from ppo_agent import PPOAgent


def parse_args():
    """Parse command-line arguments for PPO training.

    Returns:
        Parsed arguments with training hyperparameters and settings.
    """
    p = argparse.ArgumentParser(description="PPO — LunarLander-v2")
    p.add_argument(
        "--total-steps",
        type=int,
        default=1_000_000,
        help="Total environment steps (default: 1 000 000)",
    )
    p.add_argument(
        "--horizon",
        type=int,
        default=2048,
        help="Steps collected per update (default: 2048)",
    )
    p.add_argument(
        "--n-epochs",
        type=int,
        default=10,
        help="PPO gradient epochs per update (default: 10)",
    )
    p.add_argument(
        "--batch-size", type=int, default=64, help="Mini-batch size (default: 64)"
    )
    p.add_argument(
        "--lr", type=float, default=3e-4, help="Adam learning rate (default: 3e-4)"
    )
    p.add_argument(
        "--gamma", type=float, default=0.99, help="Discount factor (default: 0.99)"
    )
    p.add_argument(
        "--gae-lambda", type=float, default=0.95, help="GAE lambda (default: 0.95)"
    )
    p.add_argument(
        "--clip-eps", type=float, default=0.2, help="PPO clip epsilon (default: 0.2)"
    )
    p.add_argument(
        "--ent-coef",
        type=float,
        default=0.01,
        help="Entropy coefficient (default: 0.01)",
    )
    p.add_argument("--seed", type=int, default=42, help="Random seed (default: 42)")
    p.add_argument(
        "--checkpoint-dir",
        type=str,
        default="checkpoints",
        help="Directory to save model checkpoints",
    )
    p.add_argument(
        "--results-dir", type=str, default="results", help="Directory to save plots"
    )
    p.add_argument(
        "--no-plot", action="store_true", help="Skip saving training curve plot"
    )
    p.add_argument(
        "--log-interval", type=int, default=5, help="Log every N updates (default: 5)"
    )
    return p.parse_args()


def set_seed(seed: int):
    """Set random seed for reproducibility.

    Args:
        seed: The seed value to set.
    """
    random.seed(seed)
    np.random.seed(seed)
    torch.manual_seed(seed)


def moving_average(x, window=20):
    """Compute the moving average of a sequence.
    The moving average is a metric that smooths out short-term fluctuations 
    in data by averaging over a specified window size.

    Args:
        x: The input sequence.
        window: The window size for the moving average.

    Returns:
        The moving average of the input sequence.
    """
    if len(x) < window:
        return np.array(x)
    return np.convolve(x, np.ones(window) / window, mode="valid")


def save_plot(ep_rewards, ep_lengths, path: str):
    """Save training curves for episode rewards and lengths.

    Args:
        ep_rewards: List of episode rewards.
        ep_lengths: List of episode lengths.
        path: Path to save the plot.
    """
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 8))

    ax1.plot(ep_rewards, alpha=0.3, color="steelblue", label="Episode reward")
    ma = moving_average(ep_rewards, window=20)
    ax1.plot(
        range(len(ma)), ma, color="steelblue", linewidth=2, label="Moving avg (20)"
    )
    ax1.axhline(200, color="green", linestyle="--", linewidth=1, label="Solved (200)")
    ax1.set_xlabel("Episode")
    ax1.set_ylabel("Total Reward")
    ax1.set_title("PPO — LunarLander-v2 Training")
    ax1.legend()
    ax1.grid(alpha=0.3)

    ax2.plot(ep_lengths, alpha=0.4, color="coral", label="Episode length")
    ma2 = moving_average(ep_lengths, window=20)
    ax2.plot(range(len(ma2)), ma2, color="coral", linewidth=2, label="Moving avg (20)")
    ax2.set_xlabel("Episode")
    ax2.set_ylabel("Steps")
    ax2.legend()
    ax2.grid(alpha=0.3)

    plt.tight_layout()
    plt.savefig(path, dpi=150)
    plt.close(fig)
    print(f"[plot] Saved → {path}")

def train(args):
    """Main training loop for PPO on LunarLander-v2.
    
    Args:
        args: Parsed command-line arguments with training settings.
    """
    set_seed(args.seed)
    os.makedirs(args.checkpoint_dir, exist_ok=True)
    os.makedirs(args.results_dir, exist_ok=True)

    # Environment
    env = gym.make("LunarLander-v3")
    obs_dim = env.observation_space.shape[0]  # 8
    act_dim = env.action_space.n  # 4

    print(f"Environment : LunarLander-v3")
    print(f"Obs dim     : {obs_dim}  |  Act dim : {act_dim}")

    # Agent
    agent = PPOAgent(
        obs_dim=obs_dim,
        act_dim=act_dim,
        horizon=args.horizon,
        n_epochs=args.n_epochs,
        batch_size=args.batch_size,
        gamma=args.gamma,
        gae_lambda=args.gae_lambda,
        clip_eps=args.clip_eps,
        ent_coef=args.ent_coef,
        lr=args.lr,
    )
    print(f"Device      : {agent.device}")
    print(f"Total steps : {args.total_steps:,}")
    print("-" * 55)

    # Tracking
    ep_rewards, ep_lengths = [], []
    ep_reward, ep_length = 0.0, 0
    best_mean_reward = -np.inf
    total_steps = 0
    update_count = 0
    start_time = time.time()

    obs, _ = env.reset(seed=args.seed)

    while total_steps < args.total_steps:
        for _ in range(args.horizon):
            action, log_prob, value = agent.select_action(obs)
            next_obs, reward, terminated, truncated, _ = env.step(action)
            done = terminated or truncated

            agent.store_transition(obs, action, log_prob, reward, value, done)

            obs = next_obs
            ep_reward += reward
            ep_length += 1
            total_steps += 1

            if done:
                ep_rewards.append(ep_reward)
                ep_lengths.append(ep_length)
                ep_reward, ep_length = 0.0, 0
                obs, _ = env.reset()

        loss_stats = agent.update(last_obs=obs)
        update_count += 1

        if update_count % args.log_interval == 0 and ep_rewards:
            elapsed = time.time() - start_time
            fps = total_steps / elapsed
            recent = ep_rewards[-20:] if len(ep_rewards) >= 20 else ep_rewards
            mean_r = np.mean(recent)
            mean_r_str = f"{mean_r:+.1f}"

            print(
                f"Update {update_count:4d} | "
                f"Steps {total_steps:>8,} | "
                f"FPS {fps:5.0f} | "
                f"Episodes {len(ep_rewards):5d} | "
                f"Mean reward (20) {mean_r_str:>8} | "
                f"π-loss {loss_stats['policy_loss']:+.4f} | "
                f"V-loss {loss_stats['value_loss']:.4f} | "
                f"H {loss_stats['entropy']:.3f}"
            )

            # Save best
            if mean_r > best_mean_reward:
                best_mean_reward = mean_r
                best_path = os.path.join(args.checkpoint_dir, "ppo_lunarlander_best.pt")
                agent.save(best_path)
                print(f"  ★ New best mean reward {mean_r:+.1f} → saved to {best_path}")

    # Final save & plot
    final_path = os.path.join(args.checkpoint_dir, "ppo_lunarlander_final.pt")
    agent.save(final_path)
    print(f"\nTraining complete | {total_steps:,} steps | {len(ep_rewards)} episodes")
    print(f"Final model saved → {final_path}")

    if not args.no_plot and ep_rewards:
        plot_path = os.path.join(args.results_dir, "training_curve.png")
        save_plot(ep_rewards, ep_lengths, plot_path)

    env.close()


if __name__ == "__main__":
    args = parse_args()
    train(args)
