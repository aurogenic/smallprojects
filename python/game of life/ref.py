import pygame
import numpy as np

# Initialize Pygame
pygame.init()

# Screen dimensions
width, height = 800, 800
screen = pygame.display.set_mode((width, height))

# Colors
black = (0, 0, 0)
white = (255, 255, 255)
gray = (128, 128, 128)

# Grid settings
cols, rows = 50, 50
cell_width = width // cols
cell_height = height // rows

# Create grid
grid = np.zeros((cols, rows), dtype=int)

def draw_grid(surface):
    for i in range(cols):
        for j in range(rows):
            x = i * cell_width
            y = j * cell_height
            rect = pygame.Rect(x, y, cell_width, cell_height)
            if grid[i, j] == 1:
                pygame.draw.rect(surface, white, rect)
            else:
                pygame.draw.rect(surface, black, rect)
            pygame.draw.rect(surface, gray, rect, 1)

def update_grid():
    global grid
    new_grid = grid.copy()
    for i in range(cols):
        for j in range(rows):
            live_neighbors = (
                grid[(i-1)%cols, (j-1)%rows] + grid[(i-1)%cols, j] + grid[(i-1)%cols, (j+1)%rows] +
                grid[i, (j-1)%rows] + grid[i, (j+1)%rows] +
                grid[(i+1)%cols, (j-1)%rows] + grid[(i+1)%cols, j] + grid[(i+1)%cols, (j+1)%rows]
            )
            if grid[i, j] == 1:
                if live_neighbors < 2 or live_neighbors > 3:
                    new_grid[i, j] = 0
            else:
                if live_neighbors == 3:
                    new_grid[i, j] = 1
    grid = new_grid

def main():
    running = True
    paused = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if paused:
                    x, y = pygame.mouse.get_pos()
                    i, j = x // cell_width, y // cell_height
                    grid[i, j] = 1 if grid[i, j] == 0 else 0
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    paused = not paused

        screen.fill(black)
        draw_grid(screen)

        if not paused:
            update_grid()

        pygame.display.flip()
        pygame.time.delay(100)

    pygame.quit()

if __name__ == "__main__":
    main()
