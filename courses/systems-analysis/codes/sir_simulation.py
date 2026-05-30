"""
SIR Epidemic Model – tkinter visualisation
===========================================
Two views of the SIR compartmental model from the slides:

  1. ODE curves  – S, I, R over time (Euler integration, drawn on Canvas)
  2. Grid sim    – spatial SIR on a 2-D grid (stochastic cellular automaton)

Controls
--------
  1         ODE curve view
  2         spatial grid simulation
  Space     pause / resume grid
  r         reset grid
  +/-       adjust β (transmission rate) in ODE view
  ESC       quit

Equations (from slides)
-----------------------
  dS/dt = -β · S · I
  dI/dt =  β · S · I  -  γ · I
  dR/dt =  γ · I

Dependencies: tkinter (built-in)
"""

import tkinter as tk
import random

# ---------------------------------------------------------------------------
WIDTH, HEIGHT = 900, 600
CELL   = 8
GCOLS  = WIDTH  // CELL
GROWS  = (HEIGHT - 30) // CELL
FONT   = ("Courier", 12)

C_S = "#3c8cdc"   # blue  – Susceptible
C_I = "#dc3c3c"   # red   – Infected
C_R = "#3cc850"   # green – Recovered
BG  = "#0c0c16"


# ---------------------------------------------------------------------------
# ODE solver (Euler)
# ---------------------------------------------------------------------------
def solve_sir(beta, gamma, S0=0.99, I0=0.01, R0=0.00,
              dt=0.1, t_max=160.0):
    S, I, R, t = S0, I0, R0, 0.0
    ts, Ss, Is, Rs = [], [], [], []
    while t <= t_max:
        ts.append(t); Ss.append(S); Is.append(I); Rs.append(R)
        dS = -beta * S * I
        dI =  beta * S * I - gamma * I
        dR =  gamma * I
        S = max(0.0, S + dS * dt)
        I = max(0.0, I + dI * dt)
        R = min(1.0, R + dR * dt)
        t += dt
    return ts, Ss, Is, Rs


def draw_ode(canvas, beta, gamma):
    canvas.delete("ode")
    _, Ss, Is, Rs = solve_sir(beta, gamma)
    mx, my = 70, 30
    w = WIDTH  - mx - 20
    h = HEIGHT - my - 50

    # Box
    canvas.create_rectangle(mx, my, mx + w, my + h,
                             outline="#505070", fill="#1e1e32", tags="ode")

    # Curves
    n = len(Ss)
    def pts(vals):
        return [
            coord
            for i, v in enumerate(vals)
            for coord in (mx + int(i / (n-1) * w),
                          my + h - int(v * h))
        ]

    for vals, col in ((Ss, C_S), (Is, C_I), (Rs, C_R)):
        p = pts(vals)
        if len(p) >= 4:
            canvas.create_line(p, fill=col, width=2, tags="ode")

    # Legend
    for i, (label, col) in enumerate([
            ("Susceptible (S)", C_S),
            ("Infected    (I)", C_I),
            ("Recovered   (R)", C_R)]):
        canvas.create_rectangle(mx+10, my+10+i*22, mx+22, my+22+i*22,
                                 fill=col, outline="", tags="ode")
        canvas.create_text(mx+30, my+16+i*22, text=label,
                           fill="#c8c8c8", font=FONT, anchor="w", tags="ode")

    canvas.create_text(mx + w//2, my + h + 15,
                       text=f"Time →  β={beta:.3f}  γ={gamma:.3f}  "
                            f"R₀={beta/gamma:.2f}  (+/- adjust β)",
                       fill="#aaaaaa", font=FONT, tags="ode")


# ---------------------------------------------------------------------------
# Spatial SIR grid
# ---------------------------------------------------------------------------
STATE_S, STATE_I, STATE_R = 0, 1, 2
S_COLOR = {STATE_S: C_S, STATE_I: C_I, STATE_R: C_R}


def seed_grid():
    g = [[STATE_S] * GCOLS for _ in range(GROWS)]
    cr, cc = GROWS // 2, GCOLS // 2
    for dr in range(-3, 4):
        for dc in range(-3, 4):
            g[cr + dr][cc + dc] = STATE_I
    return g


def step_grid(g, beta=0.30, gamma=0.05):
    ng = [row[:] for row in g]
    for r in range(GROWS):
        for c in range(GCOLS):
            if g[r][c] == STATE_S:
                ni = sum(
                    g[(r+dr) % GROWS][(c+dc) % GCOLS] == STATE_I
                    for dr in (-1,0,1) for dc in (-1,0,1)
                    if not (dr == dc == 0)
                )
                if ni > 0 and random.random() < 1 - (1 - beta) ** ni:
                    ng[r][c] = STATE_I
            elif g[r][c] == STATE_I:
                if random.random() < gamma:
                    ng[r][c] = STATE_R
    return ng


# ---------------------------------------------------------------------------
# Application
# ---------------------------------------------------------------------------
class App:
    def __init__(self, root: tk.Tk) -> None:
        self.root = root
        root.title("SIR Epidemic Simulation")
        root.resizable(False, False)

        self.canvas = tk.Canvas(root, width=WIDTH, height=HEIGHT,
                                bg=BG, highlightthickness=0)
        self.canvas.pack()

        self.status = tk.Label(root, text="", font=FONT,
                               bg="#08080f", fg="#aaaaaa", anchor="w")
        self.status.pack(fill=tk.X)

        self.mode       = 1
        self.beta_ode   = 0.30
        self.gamma_ode  = 0.05
        self.grid       = seed_grid()
        self.generation = 0
        self.paused     = False

        # Pre-create spatial cell rects
        self.rects = [
            [self.canvas.create_rectangle(
                c * CELL, r * CELL,
                c * CELL + CELL - 1, r * CELL + CELL - 1,
                fill=C_S, outline="", state="hidden")
             for c in range(GCOLS)]
            for r in range(GROWS)
        ]

        root.bind("<Key>", self._on_key)
        self._show_ode()
        self._loop()

    # --- ODE view ---------------------------------------------------------
    def _show_ode(self) -> None:
        self._hide_grid()
        draw_ode(self.canvas, self.beta_ode, self.gamma_ode)
        self.status.config(
            text="  SIR ODE  |  1=ODE  2=spatial  +/-=β  ESC=quit"
        )

    # --- Spatial view -----------------------------------------------------
    def _show_grid(self) -> None:
        self.canvas.delete("ode")
        for r in range(GROWS):
            for c in range(GCOLS):
                self.canvas.itemconfig(
                    self.rects[r][c],
                    fill=S_COLOR[self.grid[r][c]],
                    state="normal"
                )
        flat = [cell for row in self.grid for cell in row]
        total = len(flat)
        ns = flat.count(STATE_S)
        ni = flat.count(STATE_I)
        nr = flat.count(STATE_R)
        self.status.config(
            text=(f"  Gen {self.generation}  "
                  f"S={ns/total*100:.0f}%  I={ni/total*100:.0f}%  R={nr/total*100:.0f}%  "
                  f"|  1=ODE  2=spatial  Space=pause  r=reset  ESC=quit")
        )

    def _hide_grid(self) -> None:
        for row in self.rects:
            for item in row:
                self.canvas.itemconfig(item, state="hidden")

    # --- Main loop --------------------------------------------------------
    def _loop(self) -> None:
        if self.mode == 2 and not self.paused:
            self.grid = step_grid(self.grid)
            self.generation += 1
            self._show_grid()
        self.root.after(60, self._loop)

    # --- Key handler ------------------------------------------------------
    def _on_key(self, event: tk.Event) -> None:
        key = event.keysym
        if key == "Escape":
            self.root.destroy()
        elif key == "1":
            self.mode = 1
            self._show_ode()
        elif key == "2":
            self.mode = 2
            self._show_grid()
        elif key == "space" and self.mode == 2:
            self.paused = not self.paused
        elif key in ("r", "R") and self.mode == 2:
            self.grid = seed_grid()
            self.generation = 0
        elif key in ("plus", "equal"):
            self.beta_ode = min(self.beta_ode + 0.01, 1.0)
            if self.mode == 1:
                self._show_ode()
        elif key == "minus":
            self.beta_ode = max(self.beta_ode - 0.01, 0.01)
            if self.mode == 1:
                self._show_ode()


# ---------------------------------------------------------------------------
def main() -> None:
    root = tk.Tk()
    App(root)
    root.mainloop()


if __name__ == "__main__":
    main()
