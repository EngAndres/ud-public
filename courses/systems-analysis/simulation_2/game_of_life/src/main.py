"""
This module has a simple implementation 
of the Conway's game of life.

Author: Carlos Andrés Sierra <cavirguezs@udistrital.edu.co>
"""

import sys
import pygame

# setup
CELL_SIZE = 20
WIDTH, HEIGHT = 600, 400
COLS = WIDTH // CELL_SIZE
ROWS = HEIGHT // CELL_SIZE
CELL_COLOR = (0, 0, 0)
GRID_COLOR = (150, 150, 150)
BACKGROUND_COLOR = (250, 250, 250)

# init
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("UD - Game of Life")
clock = pygame.time.Clock()

# start board
# range(WIDTH) = [0, 1, 2, ..., WIDTH-1]
# for(int i = 0; i < WIDTH; i++)
grid = [[0 for _ in range(WIDTH)] for _ in range(HEIGHT)]
running = False

def count_neighbors(x, y):
    acum = 0
    positions = (-1, 0, 1)
    for dx in positions:
        for dy in positions:
            if dx == 0 and dy == 0:
                continue # current cell

            neig_x = x + dx
            neig_y = y + dy
            if 0 <= neig_x < COLS and 0 <= neig_y < ROWS:
                acum += grid[neig_x][neig_y]
    return acum 

def draw_grid():
    screen.fill(BACKGROUND_COLOR)
    for x in range(COLS):
        for y in range(ROWS):
            rect = pygame.Rect(x * CELL_SIZE, 
                               y * CELL_SIZE, 
                               CELL_SIZE, 
                               CELL_SIZE)
            color = CELL_COLOR if grid[x][y] == 1 else BACKGROUND_COLOR
            pygame.draw.rect(screen, color, rect)
            pygame.draw.rect(screen, GRID_COLOR, rect, 1)
    pygame.display.flip()

def update_grid():
    new_grid = [[0 for _ in range(WIDTH)] for _ in range(HEIGHT)]
    for x in range(COLS):
        for y in range(ROWS):
            alive_neighbors = count_neighbors(x, y)
            if grid[x][y] == 1 and (alive_neighbors in (2, 3)):  
                new_grid[x][y] = 1
            elif grid[x][y] == 0 and alive_neighbors == 3:
                new_grid[x][y] = 1
    return new_grid

# GAME LOOP
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.MOUSEBUTTONDOWN and not running:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            x = mouse_x // CELL_SIZE
            y = mouse_y // CELL_SIZE
            grid[x][y] = 1 - grid[x][y]
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                running = not running
            elif event.key == pygame.K_s:
                grid = [[0 for _ in range(WIDTH)] for _ in range(HEIGHT)]
                running = False

    if running:
        grid = update_grid()

    draw_grid()
    clock.tick(20) # FPS