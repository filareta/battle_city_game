from settings import SIZE_X, SIZE_Y
from vector import Vec2D


class Wall:
    def __init__(self, coords):
        self.coords = coords

    def __eq__(self, other):
        return self.coords == other.coords


class Bullet:
    ttl = 100

    def __init__(self, coords, direction, angle, owner):
        self.pos = coords
        self.direction = direction
        self.angle = angle
        self.owner = owner

    def flight(self, world, alpha):
        move = self.pos + self.direction
        if move[0] >= 0 and move[0] < SIZE_X and \
           move[1] >= 0 and move[1] < SIZE_Y:
            self.pos = move
            self.ttl -= 10
