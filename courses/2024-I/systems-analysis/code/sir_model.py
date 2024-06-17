"""
The SIR model is a mathematical model used to study the spread of infectious diseases in a 
population. It divides the population into three groups: susceptible (S), infected (I), and 
recovered (R).

Cellular automata, such as the Game of Life, are computational models that simulate the behavior
of a grid of cells based on simple rules. In the Game of Life, each cell can be in one of two 
states: alive or dead. 
The state of each cell is updated based on the states of its neighboring cells.

To apply the SIR model using cellular automata, we can represent the population as a grid of cells. 
Each cell can be in one of three states: susceptible, infected, or recovered. The state of each cell
is updated based on the states of its neighboring cells, following the rules of the SIR model.

The code that would fit at $PLACEHOLDER$ is the implementation of the SIR model using cellular
automata. It includes functions to initialize the grid, update the grid based on the SIR model
rules, and visualize the grid using matplot
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
    grid = np.random.choice([0, 1, 2], size=(size_, size_), p=[0.7, 0.2, 0.1])
    return grid

def update_grid(grid: np.ndarray) -> np.ndarray:
    """
    Update the game grid based on the rules of the SIR model.

    Parameters:
    - grid (numpy.ndarray): The current game grid.

    Returns:
    - numpy.ndarray: The updated game grid.
    """
    new_grid = grid.copy()  # make a copy to avoid reference value
    for i in range(grid.shape[0]):
        for j in range(grid.shape[1]):
            if grid[i, j] == 0:  # If the cell is susceptible
                # Check the neighbors for infection
                infected_neighbors = (
                    np.sum(
                        grid[
                            max(0, i - 1) : min(i + 2, grid.shape[0]),
                            max(0, j - 1) : min(j + 2, grid.shape[1]),
                        ]
                    )
                    == 1
                )
                # If any of the neighbors is infected, the cell gets infected
                if infected_neighbors > 0:
                    new_grid[i, j] = 1
            elif grid[i, j] == 1:  # If the cell is infected
                # The cell becomes recovered
                new_grid[i, j] = 2
    return new_grid

def visualize_grid(grid: np.ndarray) -> None:
    """
    Visualize the game grid using matplotlib.

    Parameters:
    - grid (numpy.ndarray): The game grid to visualize.
    """
    plt.imshow(grid, cmap="viridis")
    plt.axis("off")
    plt.show()

def run_game(size: int, generations: int):
    """
    Run the SIR model simulation.

    Parameters:
    - size (int): The size of the grid (size x size).
    - generations (int): The number of generations to simulate.
    """
    grid = initialize_grid(size)
    fig = plt.figure(figsize=(12, 12))
    ims = []
    for _ in range(generations):
        ims.append([plt.imshow(grid, cmap="viridis")])
        grid = update_grid(grid)
    _ = animation.ArtistAnimation(fig, ims, interval=250, blit=True, repeat_delay=1000)
    # S-0 = Purple         I-1 = Yellow         R-2 = Green  
    plt.show()

if __name__ == "__main__":
    SIZE = 100
    GENERATIONS = 1000
    run_game(SIZE, GENERATIONS)
