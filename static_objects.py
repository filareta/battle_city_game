from settings import SIZE_X, SIZE_Y, TILE_SIZE, BULLET_RELATIVE_SPEED
from vector import Vec2D


class Wall:
    def __init__(self, coords, breakable=False):
        self.coords = coords
        self.breakable = breakable

    def __eq__(self, other):
        return self.coords == other.coords

    def is_breakable(self):
        return breakable


class Bullet:
    def __init__(self, coords, direction, angle, owner):
        self.pos = coords
        self.direction = direction
        self.angle = angle
        self.owner = owner
        self.active = True

    def flight(self, world, delta):
        move = self.pos + self.direction * TILE_SIZE * delta * BULLET_RELATIVE_SPEED

        if move.x >= 0 and move.x < SIZE_X * TILE_SIZE and move.y >= 0 and move.y < SIZE_Y * TILE_SIZE:
            self.pos = move
        else:
            self.active = False
