# PPO — LunarLander-v2

Proximal Policy Optimization from scratch using **PyTorch** + **Gymnasium**.

## Files

| File | Purpose |
|------|---------|
| `ppo_agent.py` | `ActorCritic` network, `RolloutBuffer`, `PPOAgent` class |
| `train.py` | Training loop with logging and checkpointing |
| `evaluate.py` | Load a checkpoint and run / record evaluation episodes |
| `pyproject.toml` | Project metadata and dependency list for Poetry |

## Quick start

```bash
# 1. Create and activate a virtual environment
python3 -m venv .venv
source .venv/bin/activate

# 2. Install dependencies from pyproject.toml with Poetry
pip install poetry
poetry install

# 3. Train (≈ 1 M steps, ~15–25 min on CPU)
poetry run python train.py

# 4. Evaluate with rendering
poetry run python evaluate.py

# 5. Run headless benchmark (20 episodes)
poetry run python evaluate.py --n-episodes 20 --no-render

# 6. Record a video
poetry run python evaluate.py --record
```

## Key hyperparameters

| Parameter | Default | Notes |
|-----------|---------|-------|
| `--total-steps` | 1 000 000 | Increase for better performance |
| `--horizon` | 2048 | Steps per update (T) |
| `--n-epochs` | 10 | Gradient passes per horizon |
| `--batch-size` | 64 | Mini-batch size |
| `--lr` | 3e-4 | Adam learning rate |
| `--gamma` | 0.99 | Discount factor |
| `--gae-lambda` | 0.95 | GAE smoothing |
| `--clip-eps` | 0.2 | PPO surrogate clip |
| `--ent-coef` | 0.01 | Entropy bonus |

## Algorithm summary

```bash
for each horizon T:
    collect T transitions using current policy π_θ
    compute advantages via GAE(γ, λ)
    for n_epochs:
        for each mini-batch:
            r_t(θ) = π_θ(a|s) / π_θ_old(a|s)  # probability ratio
            L_CLIP = E[min(r_t · Â, clip(r_t, 1±ε) · Â)]
            L_VF = E[(V_θ(s) - R_t)²]
            L_ENT = E[H(π_θ(·|s))]
            L = -L_CLIP + c₁·L_VF - c₂·L_ENT
            gradient step on L
```

## Environment

**LunarLander-v2** (Gymnasium)  

- Observation: 8-dim continuous vector (position, velocity, angle, leg contacts)  
- Actions: 4 discrete (0 = do nothing, 1 = left engine, 2 = main engine, 3 = right engine)  
- Solved: mean reward ≥ 200 over 100 consecutive episodes

## Outputs

After training you will find:

```bash
checkpoints/
    ppo_lunarlander_best.pt    ← best mean-reward checkpoint
    ppo_lunarlander_final.pt   ← last checkpoint
results/
    training_curve.png         ← reward & episode-length curves
    ppo_lunarlander-*.mp4      ← recorded video (if --record used)
```
