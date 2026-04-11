"""
Load a saved checkpoint and show the agent play.

Run:
    python evaluate.py   # best checkpoint, 10 episodes, rendered
    python evaluate.py --checkpoint checkpoints/ppo_lunarlander_final.pt
    python evaluate.py --n-episodes 20 --no-render  # headless benchmark
    python evaluate.py --record    # saves a video to results/

Author: Carlos Andrés Sierra <cavirguezs@udistrital.edu.co>
"""

import argparse
import os

import gymnasium as gym
import numpy as np

from ppo_agent import PPOAgent


def parse_args():
    """This function just defines the possible parameters in the execution
    to be received in the terminal."""
    p = argparse.ArgumentParser(description="Evaluate PPO — LunarLander-v2")
    p.add_argument(
        "--checkpoint",
        type=str,
        default="checkpoints/ppo_lunarlander_best.pt",
        help="Path to the .pt checkpoint file",
    )
    p.add_argument(
        "--n-episodes",
        type=int,
        default=10,
        help="Number of evaluation episodes (default: 10)",
    )
    p.add_argument("--no-render", action="store_true", help="Run headless (no window)")
    p.add_argument(
        "--record",
        action="store_true",
        help="Record a video to results/ (implies --no-render)",
    )
    p.add_argument(
        "--results-dir", type=str, default="results", help="Directory for video output"
    )
    p.add_argument("--seed", type=int, default=0)
    return p.parse_args()


def run_evaluation(args):
    """This function just execute the agent simulation."""
    if not os.path.isfile(args.checkpoint):
        print(f"[error] Checkpoint not found: {args.checkpoint}")
        print("        Train first:  python train.py")
        return

    render_mode = None
    if args.record:
        render_mode = "rgb_array"
    elif not args.no_render: # this is what you like: see the agent playing
        render_mode = "human"

    env = gym.make("LunarLander-v3", render_mode=render_mode)

    if args.record:
        os.makedirs(args.results_dir, exist_ok=True)
        env = gym.wrappers.RecordVideo(
            env,
            video_folder=args.results_dir,
            name_prefix="ppo_lunarlander",
            episode_trigger=lambda _: True,  # record every episode
        )

    obs_dim = env.observation_space.shape[0]
    act_dim = env.action_space.n

    agent = PPOAgent(obs_dim=obs_dim, act_dim=act_dim)
    agent.load(args.checkpoint)
    agent.network.eval()

    print(f"Checkpoint  : {args.checkpoint}")
    print(f"Episodes    : {args.n_episodes}")
    print(f"Render mode : {render_mode or 'none (headless)'}")
    print("-" * 40)

    rewards = []
    for ep in range(1, args.n_episodes + 1):
        obs, _ = env.reset(seed=args.seed + ep)
        total_reward = 0.0
        steps = 0
        done = False

        while not done:
            action = agent.predict(obs)  
            obs, reward, terminated, truncated, _ = env.step(action)
            done = terminated or truncated
            total_reward += reward
            steps += 1

        rewards.append(total_reward)
        status = "LANDED" if total_reward >= 200 else "CRASHED"
        print(
            f"  Episode {ep:3d}: reward = {total_reward:+8.2f}  steps = {steps:4d}  [{status}]"
        )

    env.close()

    print("-" * 50)
    print(f"Mean reward : {np.mean(rewards):+.2f}")
    print(f"Std reward  : {np.std(rewards):.2f}")
    print(f"Min / Max   : {np.min(rewards):+.2f} / {np.max(rewards):+.2f}")
    solved = sum(r >= 200 for r in rewards)
    print(f"Solved      : {solved}/{args.n_episodes} episodes (≥ 200)")


if __name__ == "__main__":
    args = parse_args()
    run_evaluation(args)
