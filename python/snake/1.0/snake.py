from field import Field
from search import *
from astar import *
from constants import *
import random

import pygame





class Snake:
    def __init__(self, field:Field, cell, color, length=3):
        self.color = color
        self.length = length
        x, y = cell
        if x < length:
            y = length
        self.head = (x, y)
        field.add((x, y))
        self.body = []
        self.last_direction = EAST
        self.width = field.cellwidth
        for i in range(x-length, x):
            self.body.append((i, y))
            field.add((i, y))
        field.snakes.append(self)
        self.field = field
        self.living = True
    


    def move(self, direction):
        if direction in [EAST, WEST]:
            new_head = (self.head[0] + direction,  self.head[1] )
        elif direction in [NORTH, SOUTH]:
            new_head = (self.head[0],  self.head[1] + int(direction/2))
        else: 
            raise ValueError("Invalid Direction")
        return self.move_to_cell(new_head)
        

    def move_to_cell(self, new_head):
        try:
            if not self.field.at(new_head):
                self.body.append(self.head)
                self.head = new_head
                self.field.add(new_head)
                if new_head == self.field.food:
                    self.field.spawn_food()
                    self.length+= 1
                    return True
                else:
                    old_tail = self.body.pop(0)
                    self.field.remove(old_tail)
                    return False
            else:
                print("self ate", new_head)
                print("body:",  self.body)
                raise IndexError
        except IndexError:
            self.die()
            print("out of bonds", new_head)

    def move_by_DFS(self, step = False):
        if not self.field.food:
            self.field.spawn_food()

        path=depth_first_search(self, self.field)
        while path:
            for cell in path:
                self.move_to_cell(cell)
                if step:
                    yield
            path = depth_first_search(self, self.field)
            # print(path)
        yield

    def move_by_Astar(self, step = False):
        if not self.field.food:
            self.field.spawn_food()

        path=a_star(self, self.field)
        while path:
            for cell in path:
                self.move_to_cell(cell)
                if step:
                    yield
            path = a_star(self, self.field)
            # print(path)
        yield

    def test(self):
        move = self.move_by_DFS(10)
        cell = move.next()

    def die(self):
        self.color = RED
        self.living = False

    def draw_cell(self, screen , x,  y):
        cell = pygame.Rect(x*self.width, y*self.width, self.width, self.width)
        pygame.draw.rect(screen, self.color, cell)

    def draw(self, screen):
        x, y = self.head
        self.draw_cell(screen, x, y)
        eye = pygame.Rect(x*self.width+2, y*self.width+2, self.width-4, self.width-4)
        pygame.draw.rect(screen, LGREEN, eye)
        for cell in self.body:   
            self.draw_cell(screen, *cell)
    
