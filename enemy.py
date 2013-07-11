from collections import defaultdict, deque
from vector import Vec2D
from static_objects import Bullet
from settings import TILE_SIZE, ENEMIES, SIZE_X, SIZE_Y


class Enemy():
    coords = []
    direction = Vec2D(0, 0)
    angle = 0
    turn = 0
    alive = True
    health = 100
    target = None
    bullet = None

    def __init__(self, coords):
        self.coords = coords

    def create_bullet(self):
        start = self.coords[2] + self.direction
        self.bullet = Bullet(start, self.direction, self.angle, "enemy")

    def check_health(self):
        self.health -= 30
        if self.health <= 0:
            self.alive = False

    def move(self, world):
        for i, position in enumerate(self.coords):
            ind1, ind2 = self.coords[i]
            move = position + self.direction
            world[move[0]][move[1]].energy += world[ind1][ind2].energy
            self.coords[i] = move
        if self.direction[0] == 0 and self.direction[1] < 0:
            self.angle = -180
        elif self.direction[0] == 0 and self.direction[1] > 0:
            self.angle = 0
        elif self.direction[1] == 0 and self.direction[0] < 0:
            self.angle = -90
        elif self.direction[1] == 0 and self.direction[0] > 0:
            self.angle = 90

    def valid_moves(self, cell):
        directions = [Vec2D(4, 0), Vec2D(0, -4), Vec2D(-4, 0), Vec2D(0, 4)]
        cells = [(direction + cell, direction) for direction in directions]
        check = lambda c: c[0][0] >= 0 and c[0][0] < SIZE_X and \
            c[0][1] >= 0 and c[0][1] < SIZE_Y
        return filter(check, cells)

    def check_by_cell(self, direction, world):
        return all(map(lambda tile:
                   self.check_direction(tile, direction, world),
                   self.coords))

    def find_neighbours(self, cell, index, world, player):
        valid = self.valid_moves(cell)
        neigh_dict = defaultdict(list)
        for next, direction in valid:
            if self.check_by_cell(direction // 4, world):
                key = world[next[0]][next[1]].energy
                neigh_dict[key].append(direction // 4)
        self.direction = self.find_next(neigh_dict, index, world, player)

    def check_direction(self, cell, direction, world):
        p = cell + direction
        return \
            p[0] >= 0 and p[0] < SIZE_X and \
            p[1] >= 0 and p[1] < SIZE_Y and \
            world[p[0]][p[1]].empty()

    def check_for_player(self, cell, direction, world):
        p = cell + direction
        return \
            p[0] >= 0 and p[0] < SIZE_X and \
            p[1] >= 0 and p[1] < SIZE_Y and \
            (world[p[0]][p[1]].empty() or \
             world[p[0]][p[1]].content == 'G' or \
             world[p[0]][p[1]].content == 'Y')

    def detect_collision(self, direction, world):
        cells = [cell + direction for cell in self.coords
                 if self.check_for_player(cell, direction, world)]
        return any([world[x][y].content == 'Y' or
                    world[x][y].content == 'G' for x, y in cells])

    def find_next(self, neighbour_dirs, index, world, player):
        if player.distance(self.coords[0]) <= 10:
            self.create_bullet()
        keys = neighbour_dirs.keys()
        next_dir = None
        if keys:
            max_energy = max(keys)
            valid_dirs = neighbour_dirs[max_energy]
            for direction in valid_dirs:
                if self.detect_collision(direction, world):
                    self.create_bullet()
            for direction in valid_dirs:
                if self.direction.same_direction(direction):
                    return direction
            for direction in valid_dirs:
                if self.direction.same_direction(-direction):
                    return direction
            if index < len(valid_dirs):
                self.create_bullet()
                return valid_dirs[index]
            elif valid_dirs:
                return valid_dirs[len(valid_dirs)-self.turn-1]
        else:
            self.create_bullet()
            return self.direction.rotate()
