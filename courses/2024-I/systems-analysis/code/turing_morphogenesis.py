"""

"""

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

# Parameters for the Turing model
Da = 0.16  # Diffusion rate of activator
Di = 0.08  # Diffusion rate of inhibitor
f = 0.035  # Feed rate
k = 0.06  # Kill rate

# Function to initialize the game grid
def initialize_grid(size_: int) -> np.ndarray:
    """
    Initialize the game grid with random values.

    Parameters:
    - size (int): The size of the grid (size x size).

    Returns:
    - grid (numpy.ndarray): The initialized game grid.
    """
    activator = np.random.normal(1, 0.05, (size_, size_))
    inhibitor = np.random.normal(0, 0.05, (size_, size_))
    return activator, inhibitor

def laplacian(grid):
    """
    Compute the Laplacian of a grid.
    """
    return (
        -grid[2:, 1:-1]
        - grid[:-2, 1:-1]
        - grid[1:-1, 2:]
        - grid[1:-1, :-2]
        + 4*grid[1:-1, 1:-1]
    )

def update_grid(activator, inhibitor):
    """
    Update the game grid based on the rules of the Turing model.

    Parameters:
    - activator (numpy.ndarray): The current activator grid.
    - inhibitor (numpy.ndarray): The current inhibitor grid.

    Returns:
    - numpy.ndarray: The updated activator and inhibitor grids.
    """
    activator_new = activator + Da * laplacian(activator) - activator * inhibitor**2 + f * (1 - activator)
    inhibitor_new = inhibitor + Di * laplacian(inhibitor) + activator * inhibitor**2 - (k + f) * inhibitor
    return activator_new, inhibitor_new

def visualize_grid(activator, inhibitor):
    """
    Visualize the game grid using matplotlib.

    Parameters:
    - activator (numpy.ndarray): The activator grid to visualize.
    - inhibitor (numpy.ndarray): The inhibitor grid to visualize.
    """
    plt.imshow(activator - inhibitor, cmap="seismic")
    plt.axis("off")
    plt.show()

def run_game(size: int, generations: int):
    """
    Run the Turing model simulation.

    Parameters:
    - size (int): The size of the grid (size x size).
    - generations (int): The number of generations to simulate.
    """
    activator, inhibitor = initialize_grid(size)
    fig = plt.figure(figsize=(12, 12))
    ims = []
    for _ in range(generations):
        ims.append([plt.imshow(activator - inhibitor, cmap="seismic")])
        activator, inhibitor = update_grid(activator, inhibitor)
    _ = animation.ArtistAnimation(fig, ims, interval=250, blit=True, repeat_delay=1000)
    plt.show()

if __name__ == "__main__":
    SIZE = 100
    GENERATIONS = 200
    run_game(SIZE, GENERATIONS)
