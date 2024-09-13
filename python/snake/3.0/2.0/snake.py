from search import *
from astar import *
from constants import *
import random

import pygame

row = 20
col = 20
length = 20
limit = row*col
cellwidth = 20



def set_atr(r=20, c=20, w=20, l=3):
    global row, col, length, cellwidth, limit
    row = r
    col = c
    limit = r * c
    cellwidth = w
    length = l



class Snake:
    def __init__(self, cell=None, color=GREEN):
        if cell is None:
            x = random.randint(length, col - 1)
            y = random.randint(0, row - 1)
            cell = (x, y)
        elif cell[0] < length:
            cell[0] = length

        self.color = color
        self.length = length
        self.head = (x, y)
        self.body = []
        # self.last_direction = EAST
        for i in range(x-length, x):
            self.body.append((i, y))
        self.spawn_food()
        self.state = ALIVE
        self.score = 0
    
    def spawn_food(self):
        if self.length >= limit:
            print("filled")
            self.state = WON
            return False
        x = random.randint(0, row-1)
        y = random.randint(0, col-1)
        while self.collides((x, y)):
            x = random.randint(0, self.rows-1)
            y = random.randint(0, self.columns-1)
        self.food = (x, y)
        return True
    
    def maxed(self):
        return self.length >= limit
    
    def get_atr(self):
        return row, col

    def move(self, direction):
        if self.state != ALIVE:
            return
        if direction in [EAST, WEST]:
            new_head = (self.head[0] + direction,  self.head[1] )
        elif direction in [NORTH, SOUTH]:
            new_head = (self.head[0],  self.head[1] + int(direction/2))
        else: 
            raise ValueError("Invalid Direction")
        return self.move_to_cell(new_head)
        
    def collides(self, cell):
        return ((cell == self.head) or (cell in self.body))
     
    def move_to_cell(self, cell):
        if self.collides(cell) or out_of_bounds(cell):
            self.die()
            return False
        self.body.append(self.head)
        self.head = cell
        if cell == self.food:
            score += 1
            length += 1
            if self.maxed:
                self.state = WON
            else:
                self.spawn_food()
        else:
            self.body.pop(0)
        return True

    def move_by_DFS(self, step = False):

        path=depth_first_search(self)
        while path:
            for cell in path:
                self.move_to_cell(cell)
                if step:
                    yield
            path = depth_first_search(self)
            # print(path)
        yield

    def move_by_Astar(self, step = True):
        while self.state == ALIVE:
            path = a_star(self)
            for cell in path:
                self.move_to_cell(cell)
                if step:
                    yield
            # print(path)
        yield

    def die(self):
        self.color = RED
        self.state = DEAD

    def draw_cell(self, screen , x,  y):
        cell = pygame.Rect(x*cellwidth, y*cellwidth, cellwidth, cellwidth)
        pygame.draw.rect(screen, self.color, cell)

    def draw(self, screen):
        x, y = self.head
        self.draw_cell(screen, x, y)
        eye = pygame.Rect(x*cellwidth+2, y*cellwidth+2, cellwidth-4, cellwidth-4)
        pygame.draw.rect(screen, LGREEN, eye)
        for cell in self.body:   
            self.draw_cell(screen, *cell)
    

def out_of_bounds(cell):
    return any((
        cell[0] < 0, cell[0] >= col, cell[1] < 0, cell[1] >= row
    ))