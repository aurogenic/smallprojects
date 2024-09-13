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

def random_color():
    return (random.randint(0,255), random.randint(0,255), random.randint(0,255))

def event_handler():
    global running, paussed, FPS
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if not paussed:
                if event.key == pygame.K_UP:
                    move_all(NORTH)
                if event.key == pygame.K_DOWN:
                    move_all(SOUTH)
                if event.key == pygame.K_LEFT:
                    move_all(WEST)
                if event.key == pygame.K_RIGHT:
                    move_all(EAST)
            if event.key == pygame.K_RCTRL:
                FPS = 140
            if event.key == pygame.K_SPACE:
                paussed = not (paussed)

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_RCTRL:
                FPS = 5

set_atr(ROWS, COLUMNS, CELLWIDTH, LENGTH)

field = []
field.append(Snake())
def move_all(direction):
    for snake in field:
        snake.move(direction)
while running:
    event_handler()
    screen.fill(BACKGROUND)
    if not paussed:
        pass
    for snake in field:
        snake.draw(screen)

    pygame.display.flip()
    clock.tick(FPS)
