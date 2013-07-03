from math import sqrt
from settings import TILE_SIZE


class Vec2D():
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def to_int(self):
        return Vec2D(int(self.x), int(self.y))

    def zero(self):
        return self.x == self.y == 0

    def rotate(self):
        return Vec2D(self.y, self.x)

    def distance(self, other):
        return sqrt(pow((self.x - other.x), 2) + pow((self.y - other.y), 2))

    def __mul__(self, value):
        return Vec2D(self.x * value, self.y * value)

    def __floordiv__(self, value):
        return Vec2D(self.x // value, self.y // value)

    def __add__(self, other):
        return Vec2D(self.x + other.x, self.y + other.y)

    def __sub__(self, other):
        return Vec2D(self.x - other.x, self.y - other.y)

    def __neg__(self):
        return Vec2D(- self.x, - self.y)

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def __ne__(self, other):
        return not self.__eq__(other)

    def __getitem__(self, key):
        if key == 0:
            return self.x
        elif key == 1:
            return self.y
        else:
            raise StopIteration

    def __setitem__(self, key, value):
        if key == 0:
            self.x = value
        elif key == 1:
            self.y = value
        else:
            raise StopIteration

    def same_direction(self, other):
        return (self.x * other.x > 0 and self.y * other.y == 0) or \
               (self.y * other.y > 0 and self.x * other.x == 0)

    def __repr__(self):
        return "v(" + str(self.x) + "," + str(self.y) + ")"


def to_pixels(position):
    return Vec2D(position[0] * TILE_SIZE, position[1] * TILE_SIZE)

def to_coords(position):
    return Vec2D(position[0] // TILE_SIZE, position[1] // TILE_SIZE)