"""
The Game of Life is a cellular automaton devised by the 
British mathematician John Horton Conway in 1970. 
It is a zero-player game, meaning that its evolution is 
determined by its initial state, requiring no further input. 
The game is played on a grid of cells, where each cell can be either alive or dead. 
The cells evolve over time based on a set of rules, 
creating various patterns and behaviors.

This code implements the Game of Life using Python. 
It provides functions to initialize the game grid, update the grid based on the rules,
and visualize the grid. The main function runs the game loop, allowing the user to interact 
with the game by toggling cells on or off.
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
    grid = np.random.choice([0, 1], size=(size_, size_), p=[0.4, 0.6])
    return grid


def update_grid(grid: np.ndarray) -> np.ndarray:
    """
    Update the game grid based on the rules of the Game of Life.

    Parameters:
    - grid (numpy.ndarray): The current game grid.

    Returns:
    - numpy.ndarray: The updated game grid.
    """
    new_grid = grid.copy()  # make a copy to avoid reference value
    for i in range(grid.shape[0]):
        for j in range(grid.shape[1]):
            neighbors = (
                np.sum(
                    grid[
                        max(0, i - 1) : min(i + 2, grid.shape[0]),
                        max(0, j - 1) : min(j + 2, grid.shape[1]),
                    ]
                )
                - grid[i, j]
            )
            if grid[i, j] == 1:
                if neighbors < 2 or neighbors > 3:
                    new_grid[i, j] = 0
            else:
                if neighbors == 3:
                    new_grid[i, j] = 1
    return new_grid


def visualize_grid(grid: np.ndarray) -> None:
    """
    Visualize the game grid using matplotlib.

    Parameters:
    - grid (numpy.ndarray): The game grid to visualize.
    """
    plt.imshow(grid, cmap="binary")
    plt.axis("off")
    plt.show()


def run_game(size: int, generations: int):
    """
    Run the Game of Life simulation.

    Parameters:
    - size (int): The size of the grid (size x size).
    - generations (int): The number of generations to simulate.
    """
    grid = initialize_grid(size)
    fig = plt.figure(figsize=(12, 12))
    ims = []
    for _ in range(generations):
        ims.append([plt.imshow(grid, cmap="binary")])
        grid = update_grid(grid)
    _ = animation.ArtistAnimation(fig, ims, interval=250, blit=True, repeat_delay=1000)
    plt.show()


if __name__ == "__main__":
    SIZE = 100
    GENERATIONS = 200
    run_game(SIZE, GENERATIONS)
