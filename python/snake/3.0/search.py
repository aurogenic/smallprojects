# from snake import Snake
# from field import Field
from copy import deepcopy
import random

class Node:
    def __init__(self, parent, head = None):
        if not isinstance(parent, Node):
            self.walls = deepcopy(parent.body)
            self.walls.pop(0)
            self.head = parent.head
            self.path = []

        else:
            self.walls = deepcopy(parent.walls)
            self.walls.pop(0)
            self.walls.append(parent.head)
            self.head = head
            self.path = deepcopy(parent.path)
            self.path.append(parent.head)
    
    def __eq__(self, other):
        return self.head == other.head and self.walls == other.walls
    

def get_valid_moves(point, rows, columns, walls = []):
    x, y = point
    cells = []
    if x > 0 and (x-1, y) not in walls:
        cells.append((x-1,  y))
    if x < columns - 1 and (x+1, y) not in walls:
        cells.append((x+1, y))
    if y > 0 and (x, y-1) not in walls:
        cells.append((x, y-1))
    if y < rows -1 and (x, y+1) not in walls:
        cells.append((x, y+1))
        # print("vc: ", cells)
        random.shuffle(cells)
    return cells

def depth_first_search(snake):
    row, column = snake.get_atr()
    target = snake.food
    node = Node(snake)
    Frontier = [node]
    Explored = [node]
    print("start: ", snake.head, "    target: ", target)
    while Frontier:
        node = Frontier.pop()
        for cell in get_valid_moves(node.head, row, column, node.walls):
            cellNode = Node(node, cell)
            if cellNode not in Explored:
                Explored.append(cellNode)
                if cell == target:
                    node.path.append(node.head)
                    node.path.append(cell)
                    node.path.pop(0)
                    return node.path
                Frontier.append(cellNode)
    # print("Explored: ", len(set(Explored)))
    # print(Explored)
    # print(snake.length)
    # print(target in Explored)
    return []
