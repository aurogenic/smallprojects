import pygame
import numpy as np

pygame.init()

WARP = True

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)

BACKGROUNDCOLOR = WHITE
DEADCOLOR = BLACK
ALIVECOLOR = GREEN

WIDTH = 500
HEIGHT = 500

cols, rows = 50, 50

cell_width = WIDTH // cols
cell_height = HEIGHT // rows

grid = np.zeros((cols, rows), dtype=int)
screen = pygame.display.set_mode((WIDTH, HEIGHT))

def main():
    running = True
    paused = True
    pygame.display.set_caption("Game of Life")
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if paused:
                    x, y = pygame.mouse.get_pos()
                    i = x // cell_width
                    j = y // cell_height
                    grid[i, j] = 1  if grid[i, j] == 0 else 0
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    paused = not paused

            screen.fill(BACKGROUNDCOLOR)
            disp_grids(screen)

            if not paused:
                update()

            pygame.display.flip()

            pygame.time.delay(100)
    pygame.quit()

def disp_grids(screen):
    for i in range(cols):
        for j in range(rows):
            cell = pygame.Rect(i * cell_width, j * cell_height, cell_width, cell_height)
            if grid[i, j] == 1:
                pygame.draw.rect(screen, ALIVECOLOR, cell)
            else:
                pygame.draw.rect(screen, DEADCOLOR, cell)
            
            # pygame.draw.rect(screen, BACKGROUNDCOLOR, cell, 1)


def update():
    global grid
    new_grid = grid.copy()
    for i in range(cols):
        for j in range(rows):
            count =  (
                grid[(i-1)%cols, (j-1)%rows] + grid[(i-1)%cols, j] + grid[(i-1)%cols, (j+1)%rows] +
                grid[i, (j-1)%rows] + grid[i, (j+1)%rows] +
                grid[(i+1)%cols, (j-1)%rows] + grid[(i+1)%cols, j] + grid[(i+1)%cols, (j+1)%rows]
            )
            if grid[i, j] == 1:
                if count < 2 or count > 3:
                    new_grid[i, j] = 0
            else:
                if count == 3:
                    new_grid[i, j] = 1
    grid = new_grid

            
if __name__ == "__main__":
    main()
