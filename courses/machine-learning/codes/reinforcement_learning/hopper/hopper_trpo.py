"""
Solve Hopper problem using Trust Region Policy Optimization (TRPO).

Experiment sweep: 20 configurations (a baseline plus 19 variants) are trained,
evaluated and saved. Results are appended to RESULTS_PATH and ranked by mean reward.
"""

import argparse
import csv
import os
import time

import gymnasium as gym
import torch
from sb3_contrib import TRPO
from stable_baselines3.common.env_util import make_vec_env
from stable_baselines3.common.evaluation import evaluate_policy
from stable_baselines3.common.monitor import Monitor
from stable_baselines3.common.utils import set_random_seed
from stable_baselines3.common.vec_env import VecNormalize, DummyVecEnv

# Environment Setup
ENV_ID = "Hopper-v5"
SEED = 42
TOTAL_TIMESTEPS = 1_000_000
MODEL_DIR = "models"
LOG_DIR = "logs"
RESULTS_PATH = os.path.join(LOG_DIR, "trpo_hopper_sweep.csv")

os.makedirs(MODEL_DIR, exist_ok=True)
os.makedirs(LOG_DIR, exist_ok=True)
set_random_seed(SEED)

# Parallel Environments
N_ENVS = 8

# Model Setup - baseline values (the original single-run config)
BASELINE = {
    "n_steps": 2_048,
    "batch_size": 128,
    "gamma": 0.99,
    "target_kl": 0.02,  # delta
    "cg_damping": 0.01,  # gradient conjugate
    "net_arch": [256, 256],  # same size for pi (actor) and vf (critic)
}

# Variants on top of BASELINE: one change at a time, plus the most relevant pairs
VARIANTS = [
    # one change
    {"n_steps": 1_024},
    {"batch_size": 64},
    {"gamma": 0.999},
    {"target_kl": 0.01},
    {"target_kl": 0.03},
    {"cg_damping": 0.1},
    {"net_arch": [64, 64]},
    # combinations
    {"target_kl": 0.01, "cg_damping": 0.1},
    {"target_kl": 0.03, "cg_damping": 0.1},
    {"net_arch": [64, 64], "target_kl": 0.01},
    {"net_arch": [64, 64], "target_kl": 0.03},
    {"n_steps": 1_024, "batch_size": 64},
    {"gamma": 0.999, "target_kl": 0.03},
    {"gamma": 0.999, "net_arch": [64, 64]},
    {"net_arch": [64, 64], "cg_damping": 0.1},
    {"n_steps": 1_024, "target_kl": 0.01},
    {"batch_size": 64, "target_kl": 0.03},
    {"n_steps": 1_024, "net_arch": [64, 64]},
    {"gamma": 0.999, "target_kl": 0.01},
]

# Fixed values shared by every combination
GAE_LAMBDA = 0.95
CG_MAX_STEPS = 25
LINE_SEARCH_SHRINKING_FACTOR = 0.8
LINE_SEARCH_MAX_ITER = 10
N_CRITIC_UPDATES = 10
NORMALIZE_ADVANTAGE = True

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
    return [(f"trpo_{idx:02d}", params) for idx, params in enumerate(configs)]


def load_done_ids():
    """Run ids already present in the results file, so an interrupted sweep can resume."""
    if not os.path.exists(RESULTS_PATH):
        return set()
    with open(RESULTS_PATH, newline="") as f:
        return {row["run_id"] for row in csv.DictReader(f)}


def train_and_evaluate(run_id, params, timesteps):
    venv = make_vec_env(ENV_ID, n_envs=N_ENVS, seed=SEED)
    venv = VecNormalize(venv, norm_obs=True, norm_reward=True, clip_obs=10.0)

    model = TRPO(
        policy="MlpPolicy",
        policy_kwargs=dict(
            net_arch=dict(pi=params["net_arch"], vf=params["net_arch"])
        ),
        env=venv,
        n_steps=params["n_steps"],
        batch_size=params["batch_size"],
        gamma=params["gamma"],
        gae_lambda=GAE_LAMBDA,
        target_kl=params["target_kl"],
        cg_max_steps=CG_MAX_STEPS,
        cg_damping=params["cg_damping"],
        line_search_shrinking_factor=LINE_SEARCH_SHRINKING_FACTOR,
        line_search_max_iter=LINE_SEARCH_MAX_ITER,
        n_critic_updates=N_CRITIC_UPDATES,
        normalize_advantage=NORMALIZE_ADVANTAGE,
        device=DEVICE,
        tensorboard_log=LOG_DIR,
        seed=SEED,
        verbose=0,
    )

    start = time.time()
    model.learn(total_timesteps=timesteps, tb_log_name=run_id)
    train_seconds = time.time() - start
    model.save(os.path.join(MODEL_DIR, run_id))
    stats_path = os.path.join(MODEL_DIR, f"{run_id}_vecnorm.pkl")
    venv.save(stats_path)  # transition stats needed to evaluate the model
    venv.close()

    # evaluation
    eval_env = DummyVecEnv([lambda: Monitor(gym.make(ENV_ID))])
    eval_env = VecNormalize.load(stats_path, eval_env)
    eval_env.training = False
    eval_env.norm_reward = False

    mean_reward, std_reward = evaluate_policy(
        model, eval_env, n_eval_episodes=10, deterministic=True
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
    parser = argparse.ArgumentParser(description="TRPO experiment sweep for Hopper-v5")
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
