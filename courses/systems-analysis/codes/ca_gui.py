"""
Wolfram Elementary Cellular Automaton – GUI
============================================
Visualises 1-D cellular automata (Wolfram's 256 rules) row by row.

Controls
--------
  Space         reset grid with a single seed cell in the centre
  r             reset with a random initial row
  Up / Down     change the rule number (+/- 1)
  0-9 + Return  type a rule number then Enter

Dependencies: tkinter (built-in with Python)
"""

import tkinter as tk
import random

# ---------------------------------------------------------------------------
WIDTH, HEIGHT = 900, 570
CELL  = 3
COLS  = WIDTH  // CELL
ROWS  = HEIGHT // CELL
C_ON  = "#00dcb2"
C_OFF = "#0f0f1e"
FONT  = ("Courier", 12)


# ---------------------------------------------------------------------------
# Wolfram rule engine
# ---------------------------------------------------------------------------
def rule_table(n: int) -> dict:
    bits = format(n & 0xFF, "08b")
    return {p: int(b) for p, b in zip(
        ["111","110","101","100","011","010","001","000"], bits)}


def next_row(row, table):
    n = len(row)
    return [table[f"{row[(i-1)%n]}{row[i]}{row[(i+1)%n]}"] for i in range(n)]


def seed_centre():
    r = [0] * COLS; r[COLS//2] = 1; return r


def build_grid(first_row, rule_n):
    t = rule_table(rule_n); g = [first_row]
    for _ in range(ROWS - 1):
        g.append(next_row(g[-1], t))
    return g


# ---------------------------------------------------------------------------
# Render grid to PhotoImage
# ---------------------------------------------------------------------------
def render(photo: tk.PhotoImage, grid: list) -> None:
    for r, row in enumerate(grid):
        row_str = " ".join(C_ON if c else C_OFF for c in row)
        # expand each logical cell to CELL pixel rows
        tk_row = "{" + row_str + "}"
        for pr in range(CELL):
            photo.put(tk_row, to=(0, r * CELL + pr))


# ---------------------------------------------------------------------------
# Application
# ---------------------------------------------------------------------------
class App:
    def __init__(self, root):
        self.root = root
        root.title("Wolfram Cellular Automaton")
        root.resizable(False, False)

        self.canvas = tk.Canvas(root, width=WIDTH, height=HEIGHT,
                                bg=C_OFF, highlightthickness=0)
        self.canvas.pack()
        self.status = tk.Label(root, font=FONT, bg="#0a0a18",
                               fg="#c8c8c8", anchor="w")
        self.status.pack(fill=tk.X)

        self.photo  = tk.PhotoImage(width=WIDTH, height=HEIGHT)
        self.canvas.create_image(0, 0, anchor=tk.NW, image=self.photo)

        self.rule   = 30
        self.row    = seed_centre()
        self.grid   = build_grid(self.row, self.rule)
        self.typing = ""

        root.bind("<Key>", self._key)
        self._refresh()

    def _refresh(self):
        render(self.photo, self.grid)
        hint = f"  [{self.typing}_]" if self.typing else ""
        self.status.config(
            text=(f"  Rule {self.rule}  |  Space=seed  r=random  "
                  f"Up/Down=±1  type rule+Enter{hint}")
        )

    def _key(self, e):
        k = e.keysym
        if k == "Escape":
            self.root.destroy()
        elif k == "space":
            self.row = seed_centre(); self.typing = ""
            self.grid = build_grid(self.row, self.rule); self._refresh()
        elif k in ("r","R"):
            self.row = [random.randint(0,1) for _ in range(COLS)]
            self.typing = ""
            self.grid = build_grid(self.row, self.rule); self._refresh()
        elif k == "Up":
            self.rule = (self.rule+1)%256; self.typing = ""
            self.grid = build_grid(self.row, self.rule); self._refresh()
        elif k == "Down":
            self.rule = (self.rule-1)%256; self.typing = ""
            self.grid = build_grid(self.row, self.rule); self._refresh()
        elif k == "Return" and self.typing:
            self.rule = int(self.typing)%256; self.typing = ""
            self.grid = build_grid(self.row, self.rule); self._refresh()
        elif k == "BackSpace":
            self.typing = self.typing[:-1]; self._refresh()
        elif e.char.isdigit() and len(self.typing) < 3:
            self.typing += e.char; self._refresh()


def main():
    root = tk.Tk()
    App(root)
    root.mainloop()


if __name__ == "__main__":
    main()
