# pip install "stable-baselines3[extra]" "gymnasium[atari,accept-rom-license]" pygame ale-py
import os
import argparse

import ale_py
import gymnasium
gymnasium.register_envs(ale_py)

from stable_baselines3 import DQN
from stable_baselines3.common.callbacks import (BaseCallback,
                                                CheckpointCallback)
from stable_baselines3.common.env_util import make_atari_env
from stable_baselines3.common.vec_env import VecFrameStack

ENV_ID = 'ALE/Breakout-v5'
MODEL_PATH = 'models/dqn_breakout'
CKPT_DIR = 'models/checkpoints'
LOG_DIR = "logs"

LEARNING_RATE = 1e-4
BATCH_SIZE = 32
GAMMA = 0.99
EXPLORATION_FRACTION = 0.1  # fraction of total training steps over which epsilon decays 1.0 -> MIN_EPSILON
MIN_EPSILON = 0.01


def make_env(render=False, seed=0):
    kwargs = {"render_mode": "human"} if render else {}
    env = make_atari_env(ENV_ID, 1, seed=seed, env_kwargs=kwargs)
    return VecFrameStack(env, n_stack=4)

def play(model: DQN, lives: int = 5):
    env = make_env(render=True, seed=42)
    obs = env.reset()
    played, score = 0, 0.0
    while played < lives:
        action, _ = model.predict(obs, deterministic=False)
        obs, reward, done, _ = env.step(action)
        score += reward
        if done[0]:
            played += 1
        print(f'Reward over {played} lives: {score}')
    env.close()


class WatchCallback(BaseCallback):

    def __init__(self, every: int = 50_000, lives: int = 5):
        super().__init__()
        self.every = every
        self.lives = lives
        self.last = 0

    def _on_step(self):
        if self.num_timesteps - self.last >= self.every:
            self.last = self.num_timesteps
            print(f"CB. Agent at step {self.num_timesteps}")
            play(self.model, self.lives)
        return True

def train(args):
    os.makedirs(CKPT_DIR, exist_ok=True)
    os.makedirs(LOG_DIR, exist_ok=True)
    env = make_env()

    if args.resume and os.path.exists(MODEL_PATH + ".zip"):
        model = DQN.load(MODEL_PATH, env=env, tensorboard_log=LOG_DIR)
        print("Model resumed.")
    else:
        model = DQN(
            "CnnPolicy",
            env,
            learning_rate=LEARNING_RATE,
            buffer_size=100_000,
            learning_starts=50_000,
            batch_size=BATCH_SIZE,
            gamma=GAMMA,
            train_freq=4,
            exploration_fraction=EXPLORATION_FRACTION,
            exploration_final_eps=MIN_EPSILON,
            tensorboard_log=LOG_DIR,
            device="auto",
            verbose=1
        )

    callbacks = [CheckpointCallback(save_freq=100_000,
                                    save_path=CKPT_DIR,
                                    name_prefix='dqn'),
                 WatchCallback(every=args.watch_every)]

    try:
        model.learn(
            total_timesteps=args.steps,
            callback=callbacks,
            reset_num_timesteps=not args.resume,
            progress_bar=True
        )
    except Exception as e:
        print(f"Exception. {e}")

    model.save(MODEL_PATH)
    print(f"Model saved at {MODEL_PATH}")


def watch(_args):
    model = DQN.load(MODEL_PATH)
    play(model, lives=10)

if __name__ == '__main__':
    parsing = argparse.ArgumentParser()
    parsing.add_argument('mode', choices=['train', 'watch'])
    parsing.add_argument('--steps', type=int, default=3_000_000)
    parsing.add_argument('--watch_every', type=int, default=50_000)
    parsing.add_argument("--resume", action="store_true")
    a = parsing.parse_args()
    train(a) if a.mode == "train" else watch(a)
