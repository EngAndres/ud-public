import gymnasium as gym
from sb3_contrib import TRPO
from stable_baselines3.common.vec_env import DummyVecEnv, VecNormalize

ENV_ID = "Hopper-v5"

MODEL_PATH = "models/trpo_03"
STATS_PATH = "models/trpo_03_vecnorm.pkl"
N_EPISODES = 3

model = TRPO.load(MODEL_PATH)
venv = DummyVecEnv([lambda: gym.make(ENV_ID, render_mode="human")])
venv = VecNormalize.load(STATS_PATH, venv)
venv.training = False
venv.norm_reward = False

for episode in range(N_EPISODES):
    obs = venv.reset()
    done = False
    total_reward = 0.0

    while not done:
        action, _ = model.predict(obs, deterministic=True)
        obs, reward, done_, _ = venv.step(action)
        # done (bool): terminated or not
        total_reward += reward
        done = done_[0]
    
    print(f'Episode: {episode} -> Reward: {total_reward}')

venv.close()
