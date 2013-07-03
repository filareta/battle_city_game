import pygame
from collections import deque

from settings import SIZE_X, SIZE_Y, TILE_SIZE, MAPS, CONTENT
from vector import Vec2D
from player import Player
from enemy import Enemy
from static_objects import Wall


class Tile:
    energy = 0

    def __init__(self, x, y, content):
        self.position = Vec2D(x, y)
        self.content = content
        self._set_content(content)

    def _set_content(self, content):
       self.content = CONTENT[content]

    def empty(self):
        return self.content == '0'

    def no_energy(self):
        return self.content == '0' and self.energy == 0

    def __str__(self):
        return self.content + str(self.energy)


class World:
    players = {'1': None, '2': None}
    enemies = []
    walls = []
    bounds = []
    multiplayer = False

    def __init__(self, map_file, multiplayer):
        self.multiplayer = multiplayer
        self.world = [[None for y in range(SIZE_Y)] for x in range(SIZE_X)]
        self._read_map(map_file)

    def _read_map(self, map_file):
        with open(map_file) as file_map:
            for i, line in enumerate(file_map):
                for j, item in enumerate(line):
                    if item != ' ' and item != '\n':
                        self._extend_map(i * 4, j * 2, item)

    def _create_object(self, item, coords):
        if item == 'Y':
            self.players['1'] = Player(coords, 1)
        elif item == 'G' and self.multiplayer:
            self.players['2'] = Player(coords, 2)
        # elif item == 'F':
        #     self.fenix = Fenix(coords)
        elif item == 'E':
            new_enemy = Enemy(coords)
            self.enemies.append(Enemy(coords))
            if (len(self.enemies) + 1) % 3 == 0:
                new_enemy.target = "fenix"
        elif item == 'B' or item == 'W':
            self.walls.append(Wall(coords))
        elif item == '#':
            self.bounds = coords

    def _extend_map(self, i, j, item):
        coords = []
        for k in range(4):
            for l in range(4):
                if item != '#':
                    self.world[j+l][i+k] = Tile(j+l, i+k, item)
                elif j + l == 0 or j + l == SIZE_X or i + k == 0 or i + k == SIZE_Y:
                    self.world[j+l][i+k] = Tile(j+l, i+k, item)
                else:
                    self.world[j+l][i+k] = Tile(j+l, i+k, '0')
                if item != '0':
                    coords.append(Vec2D(j+l, i+k))
        if coords:
            if item == '#':
                coords = [c for c in coords if c[0] == 0 or c[0] - 1 == SIZE_X or c[1] == 0 or c[1] - 1 == SIZE_Y]
            self._create_object(item, coords)
            self.set_energy(item, coords)

    def set_energy(self, item, coords):
        for tile in coords:
            if item == 'Y' or item == 'G':
                self.world[tile[0]][tile[1]].energy = 5
            elif item == 'F':
                self.world[tile[0]][tile[1]].energy = 4
            elif item == 'E':
                self.world[tile[0]][tile[1]].energy = -5
            elif item == 'B':
                self.world[tile[0]][tile[1]].energy = -15

    def set_content(self, item, coords):
        for tile in coords:
            self.world[tile[0]][tile[1]].content = item

    def clear_content(self, start, item):
        for i in range(4):
            for j in range(4):
                x = i + start[0]
                y = j + start[1]
                if self.in_range(x, y):
                    self.world[x][y].content = '0'
                if self.in_range(x, y) and self.world[x][y].empty() and item == 'E':
                    self.world[x][y].energy = 0

    def in_range(self, x, y):
        return x >= 0 and x < SIZE_X and y >= 0 and y < SIZE_Y

    def brick_energy(self):
        for wall in self.walls:
            self.spread(4, wall.coords[0])
            self.spread(4, wall.coords[3])
            self.spread(4, wall.coords[-1])
            self.spread(4, wall.coords[-4])

    def set_bounds_energy(self):
        for bounds in self.bounds:
            for cell in bounds:
                self.world[cell[0]][cell[1]].energy = -20
                self.spread(3, cell)

    def set_dynamics_energy(self):
        for key, player in self.players.items():
            if player:
                self.spread(9, player.coords[0])
                self.spread(9, player.coords[3])
                self.spread(9, player.coords[-1])
                self.spread(9, player.coords[-4])

    def spread(self, steps, cell):
        queue = deque()
        queue.append(cell)
        for step in range(steps):
            if queue:
                cell = queue.popleft()
                neighbours = self.neighbours(cell)
                for n in neighbours:
                    self.world[n[0]][n[1]].energy = self.world[cell[0]][cell[1]].energy + 1
                    queue.append(n)

    def neighbours(self, cell):
        dirs = [Vec2D(1, 0), Vec2D(0, -1), Vec2D(-1, 0), Vec2D(0, 1)]
        cells = [direction + cell for direction in dirs]
        return filter((lambda c: self.in_range(c[0], c[1]) and self.world[c[0]][c[1]].no_energy()), cells)

    def __getitem__(self, index):
        return self.world[index]


# w = World("assets/simple_map.txt", False)
# w.brick_energy()
# w.set_dynamics_energy()
# w.set_bounds_energy()
# for wall in w.walls:
#     print(wall.coords)
# print(w)
# print(w.players['1'].coords)
# print(w.enemies)
# for i in range(100):
#     for j in range(72):
#         print(w[i][j])
#print(w.player.coords[0])
#w.load_world()
# print(w[2][4])
# t = w[63][8]
# print(t.position)