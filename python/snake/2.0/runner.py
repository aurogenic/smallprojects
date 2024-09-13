import pygame
import random
from constants import *
from snake import Snake, set_atr
import neat
import os
import sys

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

font = pygame.font.SysFont("Arial", 10)
font2 = pygame.font.SysFont("Arial", 20)

running = True
paussed = False
generation = 0

def random_color():
    return (random.randint(0,255), random.randint(0,255), random.randint(0,255))

def event_handler():
    global running, paussed, FPS
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            sys.exit()
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

def run_snake(genomes, config):
    nets = []
    snakes= []
    for genome_id,  genome in genomes:
        global running, paused
        net = neat.nn.FeedForwardNetwork.create(genome, config)
        nets.append(net)
        genome.fitness = 0
        snakes.append(Snake())

        global generation
        generation += 1

        while True:
            event_handler()
            if not paussed:
                for i, snake in enumerate(snakes):
                    inputs = snake.distances()
                    output = nets[i].activate(inputs)
                    direction = get_action_from_outputs(output)
                    snake.move(direction)
                    # snake.draw(screen)

                left = 0
                for i,snake in enumerate(snakes):
                    if snake.state == ALIVE:
                        left +=1
                        genomes[i][1].fitness = snake.get_fitness()
                        print(genomes[i][1].fitness)

                if left == 0:
                    break

                screen.fill(BACKGROUND)
                for snake in snakes:
                    if snake.state ==ALIVE:
                        snake.draw(screen)

                text = font2.render("Generation : " + str(generation), True, (255, 255, 0))
                text_rect = text.get_rect()
                text_rect.center = (WIDTH/2, 100)
                screen.blit(text, text_rect)

                text = font.render("remain snakes : " + str(left), True, WHITE)
                text_rect = text.get_rect()
                text_rect.center = (WIDTH/2, 200)
                screen.blit(text, text_rect)

                
                pygame.display.flip()
                clock.tick(FPS)

                



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
    config = neat.config.Config(neat.DefaultGenome, neat.DefaultReproduction, neat.DefaultSpeciesSet, neat.DefaultStagnation, config_path)

    p = neat.Population(config)
    p.add_reporter(neat.StdOutReporter(True))
    stats = neat.StatisticsReporter()
    p.add_reporter(stats)

    winner = p.run(run_snake, 2000)

    print("\n Best Geonome:\n", str(winner))

if __name__ == "__main__":
    start()