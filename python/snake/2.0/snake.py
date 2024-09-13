from search import *
from astar import *
from constants import *
import random
from time import time
import pygame



row = 20
col = 20
length = 20
limit = row*col
cellwidth = 20

# font = pygame.font.SysFont('comicsan', 20)



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
        self.alt_clr = alt_clr(color)
        self.length = length
        self.head = (x, y)
        self.body = []
        # self.last_direction = EAST
        for i in range(x-length, x):
            self.body.append((i, y))
        self.spawn_food()
        self.state = ALIVE
        self.score = 1
        self.timestamp = time()
    
    def spawn_food(self):
        if self.length >= limit:
            self.state = WON
            return False
        x = random.randint(0, col-1)
        y = random.randint(0, row-1)
        while self.collides((x, y)):
            x = random.randint(0, col-1)
            y = random.randint(0, row-1)
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
            self.score += 1
            self.length += 1
            if self.maxed():
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
        yield

    def update(self):
        pass

    def distances(self):
        x, y = self.head
        i, j = self.food
        lst = [0 for _ in range(8)]
        lst[0] = j - y
        lst[1] = y - j
        lst[2] = i - x
        lst[3] = x - i
        lst[4] = y
        lst[5] = row-y-1
        lst[6] = x
        lst[7] = col-x-1
        for k in range(y-1, -1, -1):
            if (x, k) in self.body:
                lst[4] = y-1-k
                break
        for k in range(y, row):
            if (x, k) in self.body:
                lst[5] = k-y-1
                break
        for k in range(x-1, -1, -1):
            if (k, y) in self.body:
                lst[6] = x-1-k
                break
        for k in range(x, col):
            if (k, y) in self.body:
                lst[6] = k-x-1
                break
        # print(lst)
        return lst

    def get_data(self):
        head_x = self.head[0] / col
        head_y = self.head[1] / row
        food_x = self.food[0] / col
        food_y = self.food[1] / row

        left_wall = self.head[0] / col
        right_wall = (col - self.head[0]) / col
        top_wall = self.head[1] / row
        bottom_wall = (row - self.head[1]) / row

        inputs = [head_x, head_y, food_x, food_y, left_wall, right_wall, top_wall, bottom_wall]
        return inputs



    def get_fitness(self):
        if self.state == ALIVE:
            distance_to_food = abs(self.food[0] - self.head[0]) + abs(self.food[1] - self.head[1])
            fitness = (self.score * 10) - distance_to_food*10
            if self.head == self.food:
                fitness += 1000  # Extra reward for eating food
        else:
            fitness = (self.score * 1000) - 100
        return fitness

    def move_by_Astar(self, step = True):
        while self.state == ALIVE:
            path = a_star(self)
            for cell in path:
                self.move_to_cell(cell)
                if step:
                    yield
        yield

    def die(self):
        self.color = RED
        self.state = DEAD

    def draw_cell(self, screen , x,  y):
        cell = pygame.Rect(x*cellwidth, y*cellwidth, cellwidth, cellwidth)
        pygame.draw.rect(screen, self.color, cell)

    def draw(self, screen):
        for x in range(col):
            for y in range(row):
                cell = pygame.Rect(x*cellwidth+5, y*cellwidth+5, cellwidth-10, cellwidth-10)
                pygame.draw.rect(screen, (50, 50, 50), cell)
        x, y = self.head
        self.draw_cell(screen, x, y)
        eye = pygame.Rect(x*cellwidth+2, y*cellwidth+2, cellwidth-4, cellwidth-4)
        pygame.draw.rect(screen, self.alt_clr, eye)
        for cell in self.body:   
            self.draw_cell(screen, *cell)
        if self.food != None:
            pygame.draw.circle(screen, WHITE, (int((self.food[0]+0.5)*cellwidth), int((self.food[1]+0.5)*cellwidth)), cellwidth*0.35)
            pygame.draw.circle(screen, self.color, (int((self.food[0]+0.5)*cellwidth), int((self.food[1]+0.5)*cellwidth)), cellwidth*0.15)
            
    

def out_of_bounds(cell):
    return any((
        cell[0] < 0, cell[0] >= col, cell[1] < 0, cell[1] >= row
    ))


def alt_clr(color):
    r, g, b = color
    return (int(r*0.8), int(g*0.8), int(b*0.8))