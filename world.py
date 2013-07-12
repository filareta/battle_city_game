from collections import deque

from settings import SIZE_X, SIZE_Y, TILE_SIZE, MAPS, CONTENT
from vector import Vec2D
from player import Player
from enemy import Enemy
from static_objects import Wall


class Tile:
    def __init__(self, x, y, content):
        self.position = Vec2D(x, y)
        self.content = content
        self._set_content(content)

    def _set_content(self, content):
        self.content = CONTENT[content]

    def empty(self):
        return self.content == '0'

    def passable(self):
        return self.content != 'B' and self.content != 'W' and self.content != 'F'

    def __str__(self):
        return self.content


class World:
    players = {'1': None, '2': None}
    enemies = []
    walls = []
    bounds = []
    phoenix = []
    multiplayer = False

    def __init__(self, map_file, multiplayer):
        self.multiplayer = multiplayer
        self.world = [[None for y in range(SIZE_Y)] for x in range(SIZE_X)]
        self._read_map(map_file)

    def _read_map(self, map_file):
        with open(map_file) as file_map:
            for i, line in enumerate(file_map):
                for j, item in enumerate(item for item in line if item != ' ' and item != '\n'):
                    if item != ' ' and item != '\n':
                        self._extend_map(i, j, item)

        self.print_world()

    def print_world(self):
        for y in range(SIZE_Y):
            for x in range(SIZE_X):
                print(self.world[x][y], end=" ")

            print()

    def _create_object(self, item, position):
        if item == 'Y':
            self.players['1'] = Player(position, 1)
        elif item == 'G' and self.multiplayer:
            self.players['2'] = Player(position, 2)
        elif item == 'F':
            self.phoenix.append(position)
        elif item == 'E':
            new_enemy = Enemy(position)
            self.enemies.append(Enemy(position))
            if (len(self.enemies) + 1) % 3 == 0:
                new_enemy.target = "phoenix"
        elif item == 'B' or item == 'W':
            self.walls.append(Wall(position))
        elif item == '#':
            self.bounds = position

    def _extend_map(self, i, j, item):

        if item != '#':
            self.world[j][i] = Tile(j, i, item)

        elif j == 0 or j == SIZE_X - 1 or i == 0 or i == SIZE_Y - 1:
            print(j, i)
            self.world[j][i] = Tile(j, i, item)

        else:
            self.world[j][i] = Tile(j, i, '0')

        self._create_object(item, Vec2D(j, i))

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
                if self.in_range(x, y) and self.world[x][y].empty() and \
                   item == 'E':
                    self.world[x][y].energy = 0

    def in_range(self, x, y):
        return x >= 0 and x < SIZE_X and y >= 0 and y < SIZE_Y

    def spread(self, steps, cell):
        queue = deque()
        queue.append(cell)
        for step in range(steps):
            if queue:
                cell = queue.popleft()
                neighbours = self.neighbours(cell)
                for n in neighbours:
                    self.world[n[0]][n[1]].energy = \
                        self.world[cell[0]][cell[1]].energy + 1
                    queue.append(n)

    def neighbours(self, cell):
        dirs = [Vec2D(1, 0), Vec2D(0, -1), Vec2D(-1, 0), Vec2D(0, 1)]
        cells = [direction + cell for direction in dirs]
        return filter((lambda c: self.in_range(c[0], c[1]) and
                       self.world[c[0]][c[1]].no_energy()), cells)

    def kill(self):
        for i, enemy in enumerate(self.enemies):
            if not enemy.alive:
                self.clear_content(enemy.coords[0], 'E')
        self.enemies = [enemy for enemy in self.enemies if enemy.alive]
        if self.players['1'].dead:
            self.clear_content(self.players['1'].coords[0], 'Y')
        if self.multiplayer and self.players['2'].dead:
            self.clear_content(self.players['2'].coords[0], 'G')

    def __getitem__(self, index):
        return self.world[index]
