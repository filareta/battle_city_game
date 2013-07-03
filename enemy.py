from pygame import image, display
from pygame.sprite import Sprite
from pygame.rect import Rect

from collections import defaultdict, deque
from vector import Vec2D
from static_objects import Bullet
from settings import TILE_SIZE, ENEMIES, SIZE_X, SIZE_Y


class Enemy():
    SPEED = 20
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
        self.bullet = Bullet(self.coords[2] + self.direction, self.direction, self.angle, "enemy")

    def check_health(self):
        if self.health <= 0:
            self.alive = False
        else:
            self.health -= 10

    def move(self, world, alpha):
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
        directions = [Vec2D(1, 0), Vec2D(0, -1), Vec2D(-1, 0), Vec2D(0, 1)]
        cells = [(direction + cell, direction) for direction in directions]
        check = lambda c: c[0][0] >= 0 and c[0][0] < SIZE_X \
                          and c[0][1] >= 0 and c[0][1] < SIZE_Y
        return filter(check, cells)

    def check_by_cell(self, direction, world):
        check = lambda tile: self.check_direction(tile, direction, world)
        return all(map(check, self.coords))

    def find_neighbours(self, cell, index, world):
        valid = self.valid_moves(cell)
        neigh_dict = defaultdict(list)
        for n, direct in valid:
            if self.check_by_cell(direct, world):
                key = world[n[0]][n[1]].energy
                neigh_dict[key].append(direct)
        self.direction = self.find_next(neigh_dict, index, world)

    def check_direction(self, cell, direction, world):
        p = cell + direction
        valid = p[0] >= 0 and p[0] < SIZE_X and p[1] >= 0 and p[1] < SIZE_Y and \
                (world[p[0]][p[1]].empty() or world[p[0]][p[1]].content == 'Y' or \
                 world[p[0]][p[1]].content == 'G')
        return valid

    def collision(self, direction, world):
        cells = [cell + direction for cell in self.coords if self.check_direction(cell, direction, world)]
        return all([world[x][y].content == 'Y' or world[x][y].content == 'G' for x, y in cells])


    def partial_collision(self, direction, world):
        cells = [cell + direction for cell in self.coords if self.check_direction(cell, direction, world)]
        return any([world[x][y].content == 'Y' or world[x][y].content == 'G' for x, y in cells])

    def find_next(self, neighbour_dirs, index, world):
        keys = neighbour_dirs.keys()
        next_dir = None
        if keys:
            max_energy = max(keys)
            valid_dirs = neighbour_dirs[max_energy]
            for direction in valid_dirs:
                if self.partial_collision(direction, world):
                    self.create_bullet()
            for direction in valid_dirs:
                if self.direction.same_direction(direction):
                    return direction
            for direction in valid_dirs:
                if self.direction.same_direction(-direction):
                    return direction
            if index < len(valid_dirs):
                return valid_dirs[index]
            elif valid_dirs:
                return valid_dirs[len(valid_dirs)-self.turn-1]
        else:
            self.roam(world)

    def roam(self, world):
        if self.check_direction(self.coords[0], self.direction, world) and \
            self.check_direction(self.coords[-1], self.direction, world):
            return self.direction
        elif self.check_direction(self.coords[0], self.direction.rotate(), world) and \
            self.check_direction(self.coords[-1], self.direction.rotate(), world):
            return self.direction.rotate()
        elif self.check_direction(self.coords[0], -self.direction.rotate(), world) and \
            self.check_direction(self.coords[-1], -self.direction.rotate(), world):
            return -self.direction.rotate()
        elif self.check_direction(self.coords[0], -self.direction, world) and \
            self.check_direction(self.coords[-1], -self.direction, world):
            return -self.direction

