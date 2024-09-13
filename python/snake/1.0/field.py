import pygame
import random
from constants import *



class Field:
    def __init__(self, rows=20, columns=None, cellwidth=20, color=GREEN, snakes=[]):
        self.rows = int(rows)
        if columns  is None:
            columns = rows
        self.columns = int(columns)
        self.cellwidth = int(cellwidth)
        self.color = color
        self.snakes = snakes
        self.cells = [[False for _ in range(self.rows)] for _ in range(self.columns)]
        self.food = None
        
    def start(self):
        self.spawn_food()
        

    def is_filled(self):
        for row in self.cells:
            for cell in row:
                if not cell:
                    return False
        return True

    def spawn_food(self):
        if self.is_filled() :
            print("filled")
        else:
            row = random.randint(0, self.rows-1)
            column = random.randint(0, self.columns-1)
            while self.cells[column][row] == True:  
                row = random.randint(0, self.rows-1)
                column = random.randint(0, self.columns-1)
            self.food = (column, row)
            return True
                
    def remove(self, cell):
        self.cells[cell[0]][cell[1]] = False

    def add(self, cell):
        self.cells[cell[0]][cell[1]] = True

    def at(self, cell):
        x, y = cell
        if x < 0 or y < 0:
            raise IndexError
        else:
            return self.cells[x][y] 

    def draw_cell(self, screen , x,  y):
        cell = pygame.Rect(x*self.cellwidth + 2, y*self.cellwidth + 2, self.cellwidth - 4, self.cellwidth -4)
        pygame.draw.rect(screen, RED, cell)

    def draw(self, screen):
        rectangle = pygame.Rect(0, 0, self.columns * self.cellwidth, self.rows * self.cellwidth)
        pygame.draw.rect(screen, self.color, rectangle)

        for snake in self.snakes:
            snake.draw(screen)

        if self.food != None:
            pygame.draw.circle(screen, WHITE, (int((self.food[0]+0.5)*self.cellwidth), int((self.food[1]+0.5)*self.cellwidth)), self.cellwidth*0.35)
            
        # for i in range(self.columns):
        #     for j  in range(self.rows):
        #         if self.cells[i][j]:
        #             self.draw_cell(screen, i, j)

        

    