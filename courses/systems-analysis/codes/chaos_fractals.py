"""
Fractals from Chaos Rules
==========================
Three classical fractals generated purely from chaotic/iterated rules,
rendered with tkinter.

Fractals included
-----------------
  1. Sierpiński Triangle  – Chaos Game (random IFS)
  2. Barnsley Fern        – Iterated Function System
  3. Logistic Map         – bifurcation diagram (chaotic dynamics)

Controls
--------
  1  show Sierpiński Triangle
  2  show Barnsley Fern
  3  show Logistic Map (bifurcation)
  ESC / q  quit

Dependencies: tkinter (built-in with Python)
"""

import tkinter as tk
import random

# ---------------------------------------------------------------------------
WIDTH, HEIGHT = 900, 650
BG     = "#0c0c16"
N_PTS  = 100_000


# ---------------------------------------------------------------------------
# Build a colour map for a PhotoImage row
# ---------------------------------------------------------------------------
def _photo_from_points(width, height, points_colors):
    """Create a PhotoImage with background BG, painting given (x,y,color) list."""
    photo = tk.PhotoImage(width=width, height=height)
    # Fill background row by row
    bg_row = "{" + (BG + " ") * width + "}"
    for y in range(height):
        photo.put(bg_row, to=(0, y))
    # Paint points
    for x, y, col in points_colors:
        if 0 <= x < width and 0 <= y < height:
            photo.put(col, to=(x, y))
    return photo


# ---------------------------------------------------------------------------
# 1. Sierpiński via the Chaos Game
# ---------------------------------------------------------------------------
def sierpinski_photo(width, height):
    vertices = [(0.0, 0.0), (1.0, 0.0), (0.5, 1.0)]
    margin = 50
    w = width  - 2 * margin
    h = height - 2 * margin
    x, y = random.random(), random.random()
    pts = []
    for _ in range(N_PTS):
        vx, vy = random.choice(vertices)
        x = (x + vx) / 2.0
        y = (y + vy) / 2.0
        sx = int(margin + x * w)
        sy = int(margin + (1 - y) * h)
        pts.append((sx, sy, "#00d4a8"))
    return _photo_from_points(width, height, pts)


# ---------------------------------------------------------------------------
# 2. Barnsley Fern
# ---------------------------------------------------------------------------
_IFS = [
    (0.01,  0.00,  0.00,  0.00,  0.16,  0.00,  0.00),
    (0.85,  0.85,  0.04, -0.04,  0.85,  0.00,  1.60),
    (0.07,  0.20, -0.26,  0.23,  0.22,  0.00,  1.60),
    (0.07, -0.15,  0.28,  0.26,  0.24,  0.00,  0.44),
]
_CUM = []
acc = 0.0
for t in _IFS:
    acc += t[0]; _CUM.append(acc)


def barnsley_photo(width, height):
    margin = 40
    w = width  - 2 * margin
    h = height - 2 * margin
    x, y = 0.0, 0.0
    pts = []
    green_shades = ["#1a6b1a", "#228b22", "#2db82d", "#34e034"]
    for _ in range(N_PTS):
        r = random.random()
        for i, (_, a, b, c, d, e, f) in enumerate(_IFS):
            if r <= _CUM[i]:
                x, y = a*x + b*y + e, c*x + d*y + f
                break
        sx = int(margin + (x + 2.5) / 5.0 * w)
        sy = int(margin + (1 - y / 10.0) * h)
        col = green_shades[min(int(y / 2.5), 3)]
        pts.append((sx, sy, col))
    return _photo_from_points(width, height, pts)


# ---------------------------------------------------------------------------
# 3. Logistic Map bifurcation
# ---------------------------------------------------------------------------
def logistic_photo(width, height):
    margin_x, margin_y = 50, 30
    w = width  - 2 * margin_x
    h = height - 2 * margin_y
    r_min, r_max = 2.5, 4.0
    steps = 600
    skip  = 300
    show  = 150
    pts = []
    for i in range(steps):
        r = r_min + (r_max - r_min) * i / steps
        x = 0.5
        for _ in range(skip):
            x = r * x * (1 - x)
        for _ in range(show):
            x = r * x * (1 - x)
            sx = int(margin_x + i / steps * w)
            sy = int(margin_y + (1 - x) * h)
            pts.append((sx, sy, "#dc503c"))
    return _photo_from_points(width, height, pts)


# ---------------------------------------------------------------------------
# Application
# ---------------------------------------------------------------------------
class App:
    BUILDERS = {
        "1": ("Sierpiński Triangle — Chaos Game", sierpinski_photo),
        "2": ("Barnsley Fern — IFS",              barnsley_photo),
        "3": ("Logistic Map — bifurcation",        logistic_photo),
    }

    def __init__(self, root: tk.Tk) -> None:
        self.root = root
        root.title("Fractals from Chaos Rules")
        root.resizable(False, False)

        self.canvas = tk.Canvas(root, width=WIDTH, height=HEIGHT,
                                bg=BG, highlightthickness=0)
        self.canvas.pack()

        self.status = tk.Label(root, text="", font=("Courier", 12),
                               bg="#08080f", fg="#aaaaaa", anchor="w")
        self.status.pack(fill=tk.X)

        self._photo   = None     # keep reference to prevent GC
        self._img_id  = None
        self._current = "1"

        root.bind("<Key>", self._on_key)
        self._render("1")

    def _render(self, key: str) -> None:
        self._current = key
        title, builder = self.BUILDERS[key]
        self.status.config(text=f"  Computing {title} ...")
        self.root.update_idletasks()

        photo = builder(WIDTH, HEIGHT)
        self._photo = photo

        if self._img_id:
            self.canvas.itemconfig(self._img_id, image=photo)
        else:
            self._img_id = self.canvas.create_image(0, 0, anchor=tk.NW,
                                                    image=photo)
        self.status.config(
            text=f"  {title}  |  1=Sierpiński  2=Barnsley Fern  "
                 f"3=Logistic Map  ESC=quit"
        )

    def _on_key(self, event: tk.Event) -> None:
        if event.keysym in ("Escape", "q", "Q"):
            self.root.destroy()
        elif event.char in self.BUILDERS:
            self._render(event.char)


# ---------------------------------------------------------------------------
def main() -> None:
    root = tk.Tk()
    App(root)
    root.mainloop()


if __name__ == "__main__":
    main()
