"""
Lunar Lander 3 using PPO (Proximal Policy Optimization)

Architecture Actor [policy index - pi] - Critic [value function - vf]

Experiment sweep: 20 configurations (a baseline plus 19 variants) are trained,
evaluated and saved. Results are appended to RESULTS_PATH and ranked by mean reward.
"""

import argparse
import csv
import os
import time

import gymnasium as gym
import torch
from stable_baselines3 import PPO
from stable_baselines3.common.env_util import make_vec_env
from stable_baselines3.common.evaluation import evaluate_policy
from stable_baselines3.common.monitor import Monitor

# SETUP GYM
ENV_ID = "LunarLander-v3"
SEED = 42
TOTAL_TIMESTEPS = 500_000
MODEL_DIR = "models"
LOG_DIR = "logs"
RESULTS_PATH = os.path.join(LOG_DIR, "ppo_lunar_sweep.csv")

os.makedirs(MODEL_DIR, exist_ok=True)
os.makedirs(LOG_DIR, exist_ok=True)

# Parallel Environments
N_ENVS = 8

# SETUP MODEL - baseline values (the original single-run config)
BASELINE = {
    "learning_rate": 3e-3,  # ADAM
    "n_steps": 1_024,
    "batch_size": 64,
    "n_epochs": 4,
    "gamma": 0.999,
    "ent_coef": 0.01,
}

# Variants on top of BASELINE: one change at a time, plus the most relevant pairs/triples
VARIANTS = [
    # one change
    {"learning_rate": 1e-3},
    {"learning_rate": 3e-4},
    {"n_steps": 2_048},
    {"batch_size": 128},
    {"n_epochs": 10},
    {"gamma": 0.99},
    {"ent_coef": 0.0},
    # combinations
    {"learning_rate": 1e-3, "n_epochs": 10},
    {"learning_rate": 1e-3, "n_steps": 2_048},
    {"learning_rate": 3e-4, "n_steps": 2_048},
    {"learning_rate": 1e-3, "gamma": 0.99},
    {"learning_rate": 1e-3, "ent_coef": 0.0},
    {"n_steps": 2_048, "batch_size": 128},
    {"n_steps": 2_048, "n_epochs": 10},
    {"batch_size": 128, "n_epochs": 10},
    {"gamma": 0.99, "ent_coef": 0.0},
    {"n_steps": 2_048, "batch_size": 128, "n_epochs": 10},
    {"learning_rate": 1e-3, "n_steps": 2_048, "n_epochs": 10},
    {"learning_rate": 3e-4, "n_steps": 2_048, "n_epochs": 10},
]

# Fixed values shared by every combination
GAE_LAMBDA = 0.98  # reduce bias -> increase variance
CLIP_RANGE = 0.2
NET_ARCH = [64, 64]  # same size for pi (actor) and vf (critic)

# Detect - GPU
if torch.cuda.is_available():
    DEVICE = "cuda"
else:
    DEVICE = "cpu"

RESULT_FIELDS = [
    "run_id",
    *BASELINE.keys(),
    "timesteps",
    "mean_reward",
    "std_reward",
    "train_seconds",
]


def build_runs():
    """Return the 20 (run_id, params) pairs: the baseline followed by each variant."""
    configs = [BASELINE] + [{**BASELINE, **variant} for variant in VARIANTS]
    return [(f"ppo_{idx:02d}", params) for idx, params in enumerate(configs)]


def load_done_ids():
    """Run ids already present in the results file, so an interrupted sweep can resume."""
    if not os.path.exists(RESULTS_PATH):
        return set()
    with open(RESULTS_PATH, newline="") as f:
        return {row["run_id"] for row in csv.DictReader(f)}


def train_and_evaluate(run_id, params, timesteps):
    env = make_vec_env(ENV_ID, n_envs=N_ENVS, seed=SEED)
    model = PPO(
        policy="MlpPolicy",  # actor-critic
        policy_kwargs=dict(net_arch=dict(pi=NET_ARCH, vf=NET_ARCH)),
        env=env,
        learning_rate=params["learning_rate"],
        n_steps=params["n_steps"],
        batch_size=params["batch_size"],
        n_epochs=params["n_epochs"],
        clip_range=CLIP_RANGE,
        gamma=params["gamma"],
        gae_lambda=GAE_LAMBDA,
        ent_coef=params["ent_coef"],
        device=DEVICE,
        seed=SEED,
        tensorboard_log=LOG_DIR,
        verbose=0,
    )

    start = time.time()
    model.learn(total_timesteps=timesteps, tb_log_name=run_id)
    train_seconds = time.time() - start
    model.save(os.path.join(MODEL_DIR, run_id))
    env.close()

    # evaluation - new environment
    eval_env = Monitor(gym.make(ENV_ID))
    mean_reward, std_reward = evaluate_policy(
        model, eval_env, n_eval_episodes=20, deterministic=True
    )
    eval_env.close()

    return {
        "run_id": run_id,
        **params,
        "timesteps": timesteps,
        "mean_reward": round(float(mean_reward), 2),
        "std_reward": round(float(std_reward), 2),
        "train_seconds": round(train_seconds, 1),
    }


def append_result(result):
    is_new = not os.path.exists(RESULTS_PATH)
    with open(RESULTS_PATH, "a", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=RESULT_FIELDS)
        if is_new:
            writer.writeheader()
        writer.writerow(result)


def print_ranking(top_n=10):
    if not os.path.exists(RESULTS_PATH):
        return
    with open(RESULTS_PATH, newline="") as f:
        rows = list(csv.DictReader(f))
    rows.sort(key=lambda r: float(r["mean_reward"]), reverse=True)

    print(f"\nTOP {top_n} OF {len(rows)} MODELS (by mean reward)")
    for rank, row in enumerate(rows[:top_n], start=1):
        params = ", ".join(f"{k}={row[k]}" for k in BASELINE)
        print(
            f"{rank:>2}. {row['run_id']}  "
            f"{row['mean_reward']} +/- {row['std_reward']}  [{params}]"
        )


def main():
    parser = argparse.ArgumentParser(description="PPO experiment sweep for LunarLander-v3")
    parser.add_argument(
        "--timesteps", type=int, default=TOTAL_TIMESTEPS,
        help="training timesteps per combination",
    )
    parser.add_argument(
        "--dry-run", action="store_true",
        help="list the combinations without training",
    )
    args = parser.parse_args()

    runs = build_runs()
    print(f"Device: {DEVICE} | Combinations: {len(runs)} | Timesteps each: {args.timesteps}")

    if args.dry_run:
        for run_id, params in runs:
            print(run_id, params)
        return

    done = load_done_ids()
    for run_id, params in runs:
        if run_id in done:
            print(f"[skip] {run_id} already in {RESULTS_PATH}")
            continue

        print(f"[train] {run_id} {params}")
        result = train_and_evaluate(run_id, params, args.timesteps)
        append_result(result)
        print(
            f"[done] {run_id} mean={result['mean_reward']} "
            f"+/- {result['std_reward']} ({result['train_seconds']}s)"
        )

    print_ranking()


if __name__ == "__main__":
    main()
