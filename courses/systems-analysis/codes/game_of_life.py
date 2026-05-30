"""
Conway's Game of Life
======================
Interactive tkinter visualisation of Conway's Game of Life.

Rules (from the slides)
-----------------------
  Live cell, < 2 live neighbours  → dies  (underpopulation)
  Live cell, 2 or 3 live neighbours → survives
  Live cell, > 3 live neighbours  → dies  (overpopulation)
  Dead cell, exactly 3 live neighbours → born (reproduction)

Controls
--------
  Space        start / pause evolution
  n            advance one generation (when paused)
  r            randomise grid
  c            clear grid
  Left-click   toggle a cell on/off
  +/-          increase / decrease simulation speed

Dependencies: tkinter (built-in with Python)
"""

import tkinter as tk
import random

# ---------------------------------------------------------------------------
WIDTH, HEIGHT = 900, 600
CELL     = 10
COLS     = WIDTH  // CELL
ROWS     = HEIGHT // CELL
DELAY_MS = 100     # milliseconds between frames

COLOR_ALIVE = "#50dc78"
COLOR_DEAD  = "#0f0f1e"
COLOR_GRID  = "#1e1e32"
FONT        = ("Courier", 12)


# ---------------------------------------------------------------------------
# Grid logic
# ---------------------------------------------------------------------------
def empty_grid() -> list:
    return [[0] * COLS for _ in range(ROWS)]


def random_grid(density: float = 0.25) -> list:
    return [[1 if random.random() < density else 0
             for _ in range(COLS)]
            for _ in range(ROWS)]


def count_neighbours(grid: list, row: int, col: int) -> int:
    total = 0
    for dr in (-1, 0, 1):
        for dc in (-1, 0, 1):
            if dr == 0 and dc == 0:
                continue
            total += grid[(row + dr) % ROWS][(col + dc) % COLS]
    return total


def next_generation(grid: list) -> list:
    new = empty_grid()
    for r in range(ROWS):
        for c in range(COLS):
            n = count_neighbours(grid, r, c)
            alive = grid[r][c]
            new[r][c] = 1 if (alive and n in (2, 3)) or (not alive and n == 3) else 0
    return new



# ---------------------------------------------------------------------------
# Application
# ---------------------------------------------------------------------------
class App:
    def __init__(self, root: tk.Tk) -> None:
        self.root = root
        root.title("Conway's Game of Life")
        root.resizable(False, False)

        self.canvas = tk.Canvas(root, width=WIDTH, height=HEIGHT,
                                bg=COLOR_DEAD, highlightthickness=0)
        self.canvas.pack()

        self.status = tk.Label(root, text="", font=FONT,
                               bg="#0a0a18", fg="#c8c8c8", anchor="w")
        self.status.pack(fill=tk.X)

        self.grid       = random_grid()
        self.running    = False
        self.generation = 0
        self.delay      = DELAY_MS

        # Pre-create rectangle items (avoids create/delete overhead each frame)
        self.rects = [
            [self.canvas.create_rectangle(
                c * CELL, r * CELL,
                c * CELL + CELL - 1, r * CELL + CELL - 1,
                fill=COLOR_DEAD, outline=COLOR_GRID, width=0)
             for c in range(COLS)]
            for r in range(ROWS)
        ]

        root.bind("<Key>", self._on_key)
        self.canvas.bind("<Button-1>", self._on_click)

        self._draw()
        self._tick()

    def _draw(self) -> None:
        for r in range(ROWS):
            for c in range(COLS):
                color = COLOR_ALIVE if self.grid[r][c] else COLOR_DEAD
                self.canvas.itemconfig(self.rects[r][c], fill=color)
        state = "RUNNING" if self.running else "PAUSED"
        self.status.config(
            text=(f"  Gen {self.generation}  [{state}]  "
                  f"Space=play/pause  n=step  r=random  c=clear  "
                  f"+/-=speed  click=toggle")
        )

    def _tick(self) -> None:
        if self.running:
            self.grid = next_generation(self.grid)
            self.generation += 1
            self._draw()
        self.root.after(self.delay, self._tick)

    def _on_key(self, event: tk.Event) -> None:
        key = event.keysym
        if key == "Escape":
            self.root.destroy()
        elif key == "space":
            self.running = not self.running
        elif key in ("n", "N") and not self.running:
            self.grid = next_generation(self.grid)
            self.generation += 1
            self._draw()
        elif key in ("r", "R"):
            self.grid = random_grid()
            self.generation = 0
            self._draw()
        elif key in ("c", "C"):
            self.grid = empty_grid()
            self.generation = 0
            self.running = False
            self._draw()
        elif key in ("plus", "equal"):
            self.delay = max(self.delay - 20, 20)
        elif key == "minus":
            self.delay = min(self.delay + 20, 500)

    def _on_click(self, event: tk.Event) -> None:
        c = event.x // CELL
        r = event.y // CELL
        if 0 <= r < ROWS and 0 <= c < COLS:
            self.grid[r][c] ^= 1
            self._draw()


# ---------------------------------------------------------------------------
def main() -> None:
    root = tk.Tk()
    App(root)
    root.mainloop()


if __name__ == "__main__":
    main()
