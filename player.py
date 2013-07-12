from vector import Vec2D
from settings import TILE_SIZE, SIZE_X, SIZE_Y
from static_objects import Bullet


class Player:
    coords = None
    angle = 0
    health = 100
    dead = False

    def __init__(self, coords, turn):
        self.coords = coords
        self.turn = turn

    def valid_direction(self, direction, world):
        return True
        # return self.valid(self.coords[0] + direction, world) and self.valid(self.coords[-1] + direction, world)

    def valid(self, cell, world):
        return True
        # return cell[0] >= 0 and cell[0] < SIZE_X and cell[1] >= 0 and cell[1] < SIZE_Y and world[cell[0]][cell[1]].passable()

    def move(self, direction, world):
        if not self.dead:
            if self.valid_direction(direction, world):
                self.coords = self.coords + direction

    def create_bullet(self):
        if self.angle == 0:
            start = self.coords[2] + Vec2D(0, -1)
            return Bullet(start, Vec2D(0, -1), self.angle, "player")
        elif self.angle == -180:
            start = self.coords[2] + Vec2D(0, 1)
            return Bullet(start, Vec2D(0, 1), self.angle, "player")
        elif self.angle == 90:
            start = self.coords[2] + Vec2D(-1, 2)
            return Bullet(start, Vec2D(-1, 0), self.angle, "player")
        elif self.angle == -90:
            start = self.coords[2] + Vec2D(1, 2)
            return Bullet(start, Vec2D(1, 0), self.angle, "player")

    def check_health(self, decrease):
        self.health -= decrease
        if self.health <= 0:
            self.dead = True
