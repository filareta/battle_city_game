from collections import defaultdict, deque
from vector import Vec2D
from static_objects import Bullet
from settings import TILE_SIZE, ENEMIES, SIZE_X, SIZE_Y, ENEMY_HEALTH


class Enemy():
    coords = None
    direction = Vec2D(0, 0)
    angle = 0
    turn = 0
    alive = True
    health = ENEMY_HEALTH
    bullet = None

    def __init__(self, coords):
        self.coords = coords

    def create_bullet(self):
        print(self.angle)
        if self.angle == 180:
            start = self.coords + Vec2D(TILE_SIZE/2 - 2, 0)
            return Bullet(start, Vec2D(0, -1), self.angle, "enemy")
        elif self.angle == 0:
            start = self.coords + Vec2D(TILE_SIZE/2 - 4, TILE_SIZE - 4)
            return Bullet(start, Vec2D(0, 1), self.angle, "enemy")
        elif self.angle == -90:
            start = self.coords + Vec2D(4, TILE_SIZE/2 - 4)
            return Bullet(start, Vec2D(-1, 0), self.angle, "enemy")
        elif self.angle == 90:
            start = self.coords + Vec2D(TILE_SIZE - 8, TILE_SIZE/2 - 4)
            return Bullet(start, Vec2D(1, 0), self.angle, "enemy")

    def bullet_hit(self):
        self.health -= 1
        if self.health <= 0:
            self.alive = False

    def move(self, world, direction):
        if self.alive:
            self.coords = self.coords + direction
