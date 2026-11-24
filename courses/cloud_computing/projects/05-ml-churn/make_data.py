import csv
import random
from pathlib import Path

random.seed(1)
rows = []
for _ in range(500):
    a, b, c = random.random(), random.random(), random.random()
    y = 1 if a + b > 1 else 0
    rows.append([y, round(a, 6), round(b, 6), round(c, 6)])

for folder, name, part in [("train", "train.csv", rows[:400]),
                           ("validation", "validation.csv", rows[400:])]:
    Path(f"data/{folder}").mkdir(parents=True, exist_ok=True)
    with open(f"data/{folder}/{name}", "w", newline="") as f:
        csv.writer(f).writerows(part)
