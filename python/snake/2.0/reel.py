import pygame
import random
import time

pygame.init()

WIDTH, HEIGHT = 480, 640
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Recursive Backtracking Maze Generation")

BACKGROUND_COLOR = (20, 20, 20) 
WALL_COLOR = (255, 255, 255)  
PATH_COLOR = (0, 255, 0)  
GRID_COLOR = (50, 50, 50) 

cell_size = 20
cols = WIDTH // cell_size
rows = HEIGHT // cell_size

grid = [[0 for _ in range(cols)] for _ in range(rows)]

def draw_grid():
    for y in range(rows):
        for x in range(cols):
            rect = pygame.Rect(x * cell_size, y * cell_size, cell_size, cell_size)
            if grid[y][x] == 1:
                pygame.draw.rect(screen, PATH_COLOR, rect)
            else:
                pygame.draw.rect(screen, BACKGROUND_COLOR, rect)
            # pygame.draw.rect(screen, GRID_COLOR, rect, 1)  # Grid lines

def get_neighbors(x, y):
    neighbors = []
    for dx, dy in [(0, -2), (2, 0), (0, 2), (-2, 0)]:
        nx, ny = x + dx, y + dy
        if 0 <= nx < cols and 0 <= ny < rows and grid[ny][nx] == 0:
            wall_x, wall_y = x + dx // 2, y + dy // 2
            neighbors.append((nx, ny, wall_x, wall_y))
    return neighbors

def recursive_backtracking(x, y):
    grid[y][x] = 1
    draw_grid()
    pygame.display.flip()
    pygame.time.delay(50) 

    neighbors = get_neighbors(x, y)
    random.shuffle(neighbors)
    for nx, ny, wx, wy in neighbors:
        if grid[ny][nx] == 0:
            grid[wy][wx] = 1
            recursive_backtracking(nx, ny)

def start():
    global start_x, start_y, grid
    start_x, start_y = random.randint(0, cols - 1) * 2, random.randint(0, rows - 1) * 2
    start_x = min(max(start_x, 0), cols - 1)
    start_y = min(max(start_y, 0), rows - 1)
    grid[start_y][start_x] = 1
    recursive_backtracking(start_x, start_y)

started = False
paussed = True
running = True
clock = pygame.time.Clock()

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                paussed = not paussed

    if not paussed:
        if not started:
            start()
            started = True
        screen.fill(BACKGROUND_COLOR)
        draw_grid()
        pygame.display.flip()
        clock.tick(30)

pygame.quit()
