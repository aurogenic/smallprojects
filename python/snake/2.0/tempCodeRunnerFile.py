import pygame
import random
from constants import *
from snake import Snake, set_atr
import neat
import os

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
            if event.key == pygame.K_RCTRL:
                FPS = 140
            if event.key == pygame.K_SPACE:
                paussed = not (paussed)

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_RCTRL:
                FPS = 5

def fitness_funct(snake):
    return snake.fitness()



set_atr(ROWS, COLUMNS, CELLWIDTH, LENGTH)


def game():
    while running:
        event_handler()
        screen.fill(BACKGROUND)
        if not paussed:
            pass
        for snake in field:
            if snake.state == DEAD:
                field.remove(snake)
            snake.draw(screen)

        pygame.display.flip()
        clock.tick(FPS)



# snake = Snake()
# mover = snake.move_by_Astar()
# while running:
#     event_handler()
#     screen.fill(BACKGROUND)
#     if not paussed:
#         if not snake.state == DEAD:
#             try:
#                 next(mover)
#             except StopIteration:
#                 mover = snake.move_by_Astar()
#             pass
        
#     snake.draw(screen)

#     pygame.display.flip()
#     clock.tick(FPS)

def eval_genomes(genomes, config):
    for genome_id,  genome in genomes:
        global running, paused
        net = neat.nn.FeedForwardNetwork.create(genome, config)

        snake = Snake()

        fitness = 0

        while snake.state == ALIVE:
            event_handler()
            if not paussed:
                inputs = get_inp(snake)
                output = net.activate(inputs)
                direction = get_action_from_outputs(output)
                snake.move(direction)
                snake.draw(screen)
                fitness = snake.get_fitness()
        genome.fitness = fitness


def get_inp(snake):
    head_x = snake.head[0] / COLUMNS
    head_y = snake.head[1] /ROWS
    food_x = snake.food[0] / COLUMNS
    food_y = snake.food[1] / ROWS

    # body_x = [segment[0] / COLUMNS for segment in snake.body]
    # body_y = [segment[1] / ROWS for segment in snake.body]

    # max_body_length = ROWS * COLUMNS - 1
    # body_x += [0] * (max_body_length - len(body_x))
    # body_y += [0] * (max_body_length - len(body_y))
    inputs = [head_x, head_y, food_x, food_y]
    return inputs

def get_action_from_outputs(outputs):
    max_index = outputs.index(max(outputs))
    if max_index == 0:
        return EAST
    elif max_index == 1:
        return WEST
    elif max_index == 2:
        return NORTH
    elif max_index == 3:
        return SOUTH
    

def start():
    config_path = "./config-feedforward.txt"
    # config_path = os.path.join(os.path.dirname(__file__), 'config-feedforward.txt')
    config = neat.config.Config(neat.DefaultGenome, neat.DefaultReproduction, neat.DefaultSpeciesSet, neat.DefaultSpeciesSet, config_path)

    p = neat.Population(config)
    p.add_reporter(neat.StdOutReporter(True))
    stats = neat.StatisticsReporter()
    p.add_reporter(stats)

    winner = p.run(eval_genomes, 300)

    print("\n Best Geonome:\n", str(winner))

if __name__ == "__main__":
    start()