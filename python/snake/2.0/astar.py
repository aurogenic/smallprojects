from copy import deepcopy
import random

class Node:
    def __init__(self, parent, cell, f):
        if isinstance(parent, Node):
            self.parent = parent
            self.cell = cell
            self.f= f
            self.cost = parent.cost +1
            self.walls = deepcopy(parent.walls)
            self.walls.append(parent.cell)
            self.walls.pop(0)
        else:
            self.parent = None
            self.cell = parent.head
            self.f = f
            self.cost = 0
            self.walls = deepcopy(parent.body)

    def __str__(self):
        return self.cell.__str__() + "      :walls: " + self.walls
    
    def __eq__(self, other):
        return self.cell == other.cell and self.walls == other.walls
    
    def iscostly(self, other):
        return self.cost > other.cost
    

class Storage:
    def __init__(self, lst = []):
        self.nodes = lst

    def __bool__(self):
        return bool(self.nodes)
    
    def add(self, node):
        self.nodes.append(node)

    def remove(self, node):
        self.nodes.remove(node)

    def pop(self):
        node = self.nodes[0]
        for other in self.nodes:
            if other.f < node.f:
                node = other
        self.nodes.remove(node)
        return node
    
    def get(self, node):
        for other in self.nodes:
            if other == node:
                return other
        return None
    
    def has(self, node):
        for other in self.nodes:
            if other == node:
                return True
        return False
    


    
def a_star(snake):
    row, col = snake.get_atr()
    target = snake.food
    print("start:",  snake.head, "  target: ", target)

    def get_valid_points(cell, walls = []):
        x, y = cell
        cells = []
        if x > 0 and (x-1, y) not in walls:
            cells.append((x-1, y))
        if x < col - 1 and (x+1, y) not in walls:
            cells.append((x+1, y))
        if y > 0 and (x, y-1) not in walls:
            cells.append((x, y-1))
        if y < row - 1 and (x, y+1) not in walls:
            cells.append((x, y+1))
        random.shuffle(cells)
        return cells

    def dist(cell):
        return abs(cell[0] - target[0]) + abs(cell[1] - target[1])
    
    start = Node(snake , snake.head, dist(snake.head))
    frontier = Storage([start])
    explored = []
    limit = (row*col)
    try:
        while frontier:
            if len(explored) > limit:
                raise Exception
            current = frontier.pop()
            explored.append(current.cell)
            next_cells = get_valid_points(current.cell,  current.walls)
            for cell in next_cells:
                if cell == target:
                    path = [cell]
                    while current is not None:
                        path.append(current.cell)
                        current = current.parent
                    path.pop(-1)
                    print("path", path[::-1])
                    return path[::-1]
                
                f = current.cost + dist(cell)
                child = Node(current, cell, f)
                if explored.__contains__(cell):
                    pass
                else:
                    other = frontier.get(child)
                    if other is not None:
                        if other.f < child.f:
                            frontier.remove(other)
                            frontier.add(child)
                    else:
                        frontier.add(child)
    except :
        print(explored)
        print("start:",  snake.head, "  target: ", target)
        print("explored: ", len(explored))
        path = []
        while current is not None:
            path.append(current.cell)
            current = current.parent
        path.pop(-1)
        print("alt path", path[::-1])
        return path[::-1]
    return []

