# Breakout DQN — Atari Deep Q-Network with Stable-Baselines3

This repository provides a single, self-contained script to train, evaluate
and compare Deep Q-Network (DQN) agents on Atari games supported by the
Arcade Learning Environment (ALE). The implementation uses Stable-Baselines3
and the Gymnasium Atari wrappers to apply the standard preprocessing pipeline
and frame-stacking used in classic DQN experiments.

Project files provided:

- `breakout_dqn.py` — Main script implementing train, play, sweep and
  inspect modes.
- `sweep_configs.json` — JSON array of ten named hyperparameter experiments
  used by the sweep runner.
- `pyproject.toml` — Project metadata and macOS dependency specifications.

Generated at runtime:

- `models/` — Saved model archives (`.zip`).
- `logs/breakout_dqn/` — TensorBoard event files for monitoring training.

Prerequisites

The code targets Python 3.11 and relies on a standard scientific Python
tooling stack. The macOS dependencies are declared in `pyproject.toml`. A
separate `requirements-linux.txt` is used on Linux to account for platform
differences (for example, use of `opencv-python-headless` on headless Linux
servers and pinning `ale-py` to remain compatible with the Stable-Baselines3
release used here).

Installation (macOS)

Use Poetry from the this current directory to install the declared dependencies:

```bash
poetry env use $(pyenv which python)
poetry install
```

On Linux, prefer a dedicated virtual environment and install the Linux
requirements file:

```bash
pyenv virtualenv 3.11.10 ml_old
pyenv activate ml_old
pip install -r requirements-linux.txt
```

Core usage

All commands must be executed from the directory containing
`breakout_dqn.py`.

- Train a default run (saves to `models/breakout_dqn.zip`):

```bash
python breakout_dqn.py --mode train --model-path models/breakout_dqn
```

- Train a named experiment from the sweep file:

```bash
python breakout_dqn.py --mode train --experiment exp_02_lr_high \
    --model-path models/breakout_exp02
```

- Watch a saved model play (requires a display):

```bash
python breakout_dqn.py --mode play --model-path models/breakout_dqn --episodes 3
```

- Run the full sweep and keep the best model:

```bash
python breakout_dqn.py --mode sweep --sweep-file sweep_configs.json \
    --model-path models/breakout_best
```

- Inspect a saved model's constructor parameters:

```bash
python breakout_dqn.py --mode inspect --model-path models/breakout_dqn
```

Monitoring

Start TensorBoard to view training metrics and compare sweep runs:

```bash
python -m tensorboard.main --logdir logs/breakout_dqn --port 6006
python -m tensorboard.main --logdir logs/breakout_dqn/sweep --port 6006
```

Key scalars emitted by the script:

- `rollout/ep_rew_mean`: Rolling mean episode reward (last 100 episodes).
- `training/episode_reward`: Per-episode total reward.
- `training/epsilon`: Exploration (ε) scheduled over time.
- `train/loss`: Temporal-difference loss during learning.

Hyperparameter summary

The default configuration is tuned for a 300k-step budget and provides the
following representative values (see `sweep_configs.json` for variations):

- `learning_rate`: 1e-4
- `buffer_size`: 50_000
- `learning_starts`: 10_000
- `batch_size`: 64
- `gamma`: 0.99
- `train_freq`: 4
- `target_update_interval`: 1_000
- `exploration_fraction`: 0.15
- `exploration_final_eps`: 0.01

The `sweep_configs.json` file contains ten experiments that systematically
vary these parameters to identify configurations that perform best under the
specified timestep budget.

Modifying the environment

To run a different Atari game, edit the `ENV_ID` constant in
`breakout_dqn.py` (examples include `ALE/Pong-v5`, `ALE/SpaceInvaders-v5`,
`ALE/MsPacman-v5`). A complete list of ALE environments is available at
https://ale.farama.org/environments/.

Author and license

Prof. Carlos Andrés Sierra — cavirguezs@udistrital.edu.co

