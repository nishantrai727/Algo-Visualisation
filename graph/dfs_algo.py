import math
import pygame
from queue import PriorityQueue

WIDTH = 800
WIN = pygame.display.set_mode((WIDTH, WIDTH))
pygame.display.set_caption("DFS ALGORITHM")


RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0,255) 
YELLOW = (255, 255, 0)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
PURPLE = (128, 0, 128)
ORANGE = (255, 165, 0)
GREY = (128, 128, 128)
RANDOM = (64, 224, 208)


class Spot:
    def __init__(self, row, col, width, tot_rows):
        self.row = row
        self.col = col
        self.x = row * width
        self.y = col * width
        self.color = WHITE
        self.neighbors = []
        self.width = width
        self.tot_rows = tot_rows

    def get_pos(self):
        return self.row, self.col

    def is_closed(self):
        return self.color == RED

    def is_open(self):
        return self.color == GREEN

    def is_barrier(self):
        return self.color == BLACK

    def is_start(self):
        return self.color == ORANGE

    def is_end(self):
        return self.color == RANDOM

    def reset(self):
        self.color = WHITE

    def make_start(self):
        self.color = ORANGE

    def make_closed(self):
        self.color = RED

    def make_open(self):
        self.color = GREEN

    def make_barrier(self):
        self.color = BLACK

    def make_end(self):
        self.color = RANDOM

    def make_path(self):
        self.color = PURPLE

    def draw(self, win):
        pygame.draw.rect(
            win, self.color, (self.x, self.y, self.width, self.width))

    def update_neighbors(self, grid):
        self.neighbors = []
        dx, dy = [1, 0, -1, 0], [0, 1, 0, -1]
        for i in range(0, 4):
            X = self.row+dx[i]
            Y = self.col+dy[i]
            if X >= self.tot_rows or Y >= self.tot_rows or X < 0 or Y < 0 or grid[X][Y].is_barrier():
                continue
            self.neighbors.append(grid[X][Y])

    def __lt__(self, other):
        return False


def h(p1, p2):  # guess
    x1, y1 = p1
    x2, y2 = p2
    return abs(x1 - x2) + abs(y1 - y2)


def make_grid(rows, width):
    grid = []
    gap = width // rows
    for i in range(rows):
        grid.append([])
        for j in range(rows):
            spot = Spot(i, j, gap, rows)
            grid[i].append(spot)
    return grid


def draw_grid(win, rows, width):
    gap = width//rows
    for i in range(rows):
        pygame.draw.line(win, GREY, (0, i * gap), (width, i * gap))
        for j in range(rows):
            pygame.draw.line(win, GREY, (j * gap, 0), (j * gap, width))


def draw(win, grid, rows, width):
    win.fill(WHITE)
    for row in grid:
        for spot in row:
            spot.draw(win)
    draw_grid(win, rows, width)
    pygame.display.update()


def get_clicked_pos(pos, rows, width):
    gap = width // rows
    y, x = pos
    row = y // gap
    col = x // gap
    return row, col


def reconstruct_path(parent, current, draw):
    while current in parent:
        current = parent[current]
        current.make_path()
        draw()

def dfs(node,par,draw,grid,start,end,parent,vis):

    vis[node] = True
    parent[node] = par
    node.make_open()
    draw()
    if(node==end):
        return True
    for event in pygame.event.get():
        if event.type==pygame.QUIT:
            pygame.quit();

    for child in node.neighbors:
        if(child not in vis):
            if(dfs(child,node,draw,grid,start,end,parent,vis)):
                return True
    node.make_closed()
    return False;
def algo(draw, grid, start, end):

    q = []
    q.append([start, 0])
    vis = {}
    vis[start] = True
    count = 0
    parent = {}

    if(dfs(start,start,draw,grid,start,end,parent,vis)):
        reconstruct_path(parent, end, draw)
        return True
    
    for event in pygame.event.get():
        if event.type==pygame.QUIT:
            pygame.quit();


    return False


def main(win, width):

    ROWS = 50
    grid = make_grid(ROWS, width)
    start, end, run = None, None, True

    while run:
        draw(win, grid, ROWS, width)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            if pygame.mouse.get_pressed()[0]:
                pos = pygame.mouse.get_pos()
                row, col = get_clicked_pos(pos, ROWS, width)
                spot = grid[row][col]

                if not start and spot != start:
                    start = spot
                    start.make_start()
                elif not end and spot != start:
                    end = spot
                    end.make_end()
                elif spot != start and spot != end:
                    spot.make_barrier()
            elif pygame.mouse.get_pressed()[2]:
                pos = pygame.mouse.get_pos()
                row, col = get_clicked_pos(pos, ROWS, width)
                spot = grid[row][col]
                spot.reset()
                if spot == start:
                    start = None
                elif spot == end:
                    end = None
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and start and end:
                    for x in grid:
                        for spot in x:
                            spot.update_neighbors(grid)
                    algo(lambda: draw(win, grid, ROWS, width), grid, start, end)

                if event.key == pygame.K_c:
                    start = None
                    end = None
                    grid = make_grid(ROWS, width)
    pygame.quit()


main(WIN, WIDTH)
