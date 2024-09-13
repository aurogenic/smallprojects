import pygame
import random
from field import Field
from constants import *
from snake import Snake

pygame.init()
clock = pygame.time.Clock()

FPS = 5
ROWS = 20
COLUMNS = 25
CELLWIDTH = 30

WIDTH = COLUMNS*CELLWIDTH
HIEGHT = ROWS*CELLWIDTH

screen = pygame.display.set_mode((WIDTH,HIEGHT))
pygame.display.set_caption("Snake Game")

running = True
paussed = False

def event_handler():
    global running, paussed, FPS
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if not paussed:
                if event.key == pygame.K_UP:
                    snake.move(NORTH)
                if event.key == pygame.K_DOWN:
                    snake.move(SOUTH)
                if event.key == pygame.K_LEFT:
                    snake.move(WEST)
                if event.key == pygame.K_RIGHT:
                    snake.move(EAST)
            if event.key == pygame.K_RCTRL:
                FPS = 140
            if event.key == pygame.K_SPACE:
                paussed = not (paussed)

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_RCTRL:
                FPS = 5




field = Field(ROWS, COLUMNS, CELLWIDTH, BLACK)
snake = Snake(field, (5, 5), GREEN, 3)
field.start()
mover = snake.move_by_Astar(True)

while running:
    event_handler()
    if not paussed:
        try:
            next(mover)
        except StopIteration:
            mover = snake.move_by_DFS(True)
        if not snake.living:
            field = Field(ROWS, COLUMNS, CELLWIDTH, BLACK)
            field.snakes.clear()
            snake = Snake(field, (5, 5), GREEN, 3)
            field.start()
            mover = snake.move_by_Astar(True)
    field.draw(screen)

    pygame.display.flip()
    clock.tick(FPS)

