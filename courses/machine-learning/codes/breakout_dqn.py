"""
Train and play Atari Breakout with Deep Q-Network (DQN).

Features:
- Train mode using Stable-Baselines3 DQN + Atari preprocessing
- Play mode with a human-rendered UI window
- Save/load model checkpoints

Quick start:
1) Install dependencies:
    python -m pip install --upgrade pip setuptools wheel
    pip install "stable-baselines3>=2.3,<3" "gymnasium[atari,accept-rom-license]>=0.29" ale-py autorom
    python -m AutoROM --accept-license

    Recommended Python: 3.11 or 3.12

2) Train:
   python breakout_dqn.py --mode train --timesteps 300000 --model-path models/breakout_dqn

3) Watch agent play with UI:
   python breakout_dqn.py --mode play --model-path models/breakout_dqn --episodes 3

   
"""

from __future__ import annotations

import argparse
import os
from pathlib import Path

import ale_py
import gymnasium as gym

gym.register_envs(ale_py)  # ensures ALE namespace is available

from stable_baselines3 import DQN
from stable_baselines3.common.atari_wrappers import AtariWrapper
from stable_baselines3.common.env_util import make_atari_env
from stable_baselines3.common.vec_env import DummyVecEnv, VecFrameStack

ENV_ID = "ALE/Breakout-v5"


def build_train_env(seed: int) -> VecFrameStack:
    env = make_atari_env(ENV_ID, n_envs=1, seed=seed)
    env = VecFrameStack(env, n_stack=4)
    return env


def build_play_env() -> VecFrameStack:
    def _make_env():
        base_env = gym.make(ENV_ID, render_mode="human")
        return AtariWrapper(base_env, terminal_on_life_loss=False, clip_reward=False)

    env = DummyVecEnv([_make_env])
    env = VecFrameStack(env, n_stack=4)
    return env


def train(model_path: str, timesteps: int, seed: int, tensorboard_log: str | None) -> None:
    model_dir = Path(model_path).parent
    model_dir.mkdir(parents=True, exist_ok=True)

    env = build_train_env(seed=seed)

    model = DQN(
        policy="CnnPolicy",
        env=env,
        learning_rate=1e-4,
        buffer_size=100_000,
        learning_starts=10_000,
        batch_size=32,
        tau=1.0,
        gamma=0.99,
        train_freq=4,
        gradient_steps=1,
        target_update_interval=1_000,
        exploration_fraction=0.1,
        exploration_final_eps=0.01,
        verbose=1,
        tensorboard_log=tensorboard_log,
        seed=seed,
    )

    model.learn(total_timesteps=timesteps, progress_bar=True)
    model.save(model_path)

    env.close()
    print(f"Model saved at: {model_path}.zip")


def play(model_path: str, episodes: int) -> None:
    zip_path = f"{model_path}.zip"
    if not os.path.exists(zip_path):
        raise FileNotFoundError(
            f"Model file not found: {zip_path}. Train first or set --model-path correctly."
        )

    env = build_play_env()
    model = DQN.load(model_path, env=env)

    completed = 0
    obs = env.reset()
    episode_reward = 0.0

    while completed < episodes:
        action, _ = model.predict(obs, deterministic=True)
        obs, rewards, dones, infos = env.step(action)

        episode_reward += float(rewards[0])
        if dones[0]:
            completed += 1
            print(f"Episode {completed}/{episodes} reward: {episode_reward:.2f}")
            obs = env.reset()
            episode_reward = 0.0

    env.close()


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Atari Breakout DQN training/play script")
    parser.add_argument("--mode", choices=["train", "play"], required=True)
    parser.add_argument("--model-path", default="models/breakout_dqn")
    parser.add_argument("--timesteps", type=int, default=300_000)
    parser.add_argument("--episodes", type=int, default=3)
    parser.add_argument("--seed", type=int, default=42)
    parser.add_argument("--tensorboard-log", default="logs/breakout_dqn")
    return parser.parse_args()


def main() -> None:
    args = parse_args()

    if args.mode == "train":
        train(
            model_path=args.model_path,
            timesteps=args.timesteps,
            seed=args.seed,
            tensorboard_log=args.tensorboard_log,
        )
    else:
        play(model_path=args.model_path, episodes=args.episodes)


if __name__ == "__main__":
    main()
