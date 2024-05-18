"""
Chaotic patterns refer to complex and unpredictable patterns that emerge from simple and 
deterministic systems. These patterns are characterized by their sensitivity to initial 
conditions, meaning that small changes in the starting conditions can lead to significantly 
different outcomes. 

Chaotic systems often exhibit a high degree of randomness and irregularity, making them 
difficult to predict or control. In the context of the provided code, the placeholder could 
be filled with a description of how the Game of Life simulation can produce chaotic patterns 
through the interaction of cells based on certain rules.
"""

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation


# Function to initialize the game grid
def initialize_grid(size_: int) -> np.ndarray:
    """
    Initialize the game grid with random values.

    Parameters:
    - size (int): The size of the grid (size x size).

    Returns:
    - grid (numpy.ndarray): The initialized game grid.
    """
    grid = np.zeros((size_, size_), dtype=int)
    grid[0] = np.random.choice([0, 1], size=(1, size_), p=[0.3, 0.7])
    return grid


def update_grid(grid: np.ndarray, rule: dict, size_: int) -> np.ndarray:
    """
    Update the game grid based on the rules of generating chaotic systems.

    Parameters:
    - grid (numpy.ndarray): The current game grid.

    Returns:
    - numpy.ndarray: The updated game grid.
    """
    for i in range(1, grid.shape[0]):
        for j in range(grid.shape[1]):
            grid[i, j] = rule[
                (
                    grid[i - 1, (j - 1 + size_) % size_],
                    grid[i - 1, j],
                    grid[i - 1, (j + 1) % size_],
                )
            ]
    grid[0] = grid[-1]
    return grid


def visualize_grid(grid: np.ndarray) -> None:
    """
    Visualize the siulation grid using matplotlib.

    Parameters:
    - grid (numpy.ndarray): The simulation grid to visualize.
    """
    plt.imshow(grid, cmap="binary")
    plt.axis("off")
    plt.show()


def run_game(size: int, generations: int):
    """
    Run the Chaotic System simulation.

    Parameters:
    - size (int): The size of the grid (size x size).
    - generations (int): The number of generations to simulate.
    """
    grid = initialize_grid(size)
    fig = plt.figure(figsize=(12, 12))
    ims = []

    # next rule 01110110 in binary is 127 in decimal
    rule = {
        (0, 0, 0): 0,
        (0, 0, 1): 1,
        (0, 1, 0): 1,
        (0, 1, 1): 1,
        (1, 0, 0): 0,
        (1, 0, 1): 1,
        (1, 1, 0): 1,
        (1, 1, 1): 0,
    }

    for _ in range(generations):
        ims.append([plt.imshow(grid, cmap="binary")])
        grid = update_grid(grid, rule, size)
    _ = animation.ArtistAnimation(fig, ims, interval=250, blit=True, repeat_delay=1000)
    plt.show()


if __name__ == "__main__":
    SIZE = 100
    GENERATIONS = 100
    run_game(SIZE, GENERATIONS)
