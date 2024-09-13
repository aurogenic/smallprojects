import pygame
import random
from constants import *
from snake import Snake, set_atr

pygame.init()
clock = pygame.time.Clock()

FPS = 5
ROWS = 20
COLUMNS = 25
LENGTH = 3
CELLWIDTH = 30
BACKGROUND = BLACK
SNAKE_COLOR = GREEN

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

set_atr(ROWS, COLUMNS, CELLWIDTH, LENGTH)


field = []
snake = Snake()
# mover = []
# for snake in field:
#     mover.append(snake.move_by_Astar(True))
mover = snake.move_by_Astar()
while running:
    event_handler()
    screen.fill(BACKGROUND)
    if not paussed:
        if not snake.state == DEAD:
            try:
                next(mover)
            except StopIteration:
                mover = snake.move_by_Astar()
            # snake = Snake()
            # mover = snake.move_by_Astar()
        
    snake.draw(screen)

    pygame.display.flip()
    clock.tick(FPS)

