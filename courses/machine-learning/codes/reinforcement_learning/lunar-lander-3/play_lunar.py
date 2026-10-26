"""
Load PPO Model and show visual simulation
"""

import gymnasium as gym
from stable_baselines3 import PPO

ENV_ID = "LunarLander-v3"
MODEL_PATH = "models/ppo_10"
model = PPO.load(MODEL_PATH)

env = gym.make(ENV_ID, render_mode='human')

obs, _ = env.reset()
done = False
total_reward = 0.0

while not done:
    action, _ = model.predict(obs, deterministic=True)
    obs, reward, terminated, truncated, _ = env.step(action)
    # terminated could be (bool): landed or crashed
    # truncated (bool): if the agent reach the limit of steps
    total_reward += reward
    done = terminated or truncated

print(f"Final Reward: {total_reward}")
env.close()
