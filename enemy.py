from collections import defaultdict, deque
from vector import Vec2D
from static_objects import Bullet
from settings import TILE_SIZE, ENEMIES, SIZE_X, SIZE_Y, ENEMY_HEALTH


class Enemy():
    coords = []
    direction = Vec2D(0, 0)
    angle = 0
    turn = 0
    alive = True
    health = ENEMY_HEALTH
    target = None
    bullet = None

    def __init__(self, coords):
        self.coords = coords

    def create_bullet(self):
        start = self.coords[2] + self.direction
        self.bullet = Bullet(start, self.direction, self.angle, "enemy")

    def bullet_hit(self):
        self.health -= 1
        if self.health <= 0:
            self.alive = False

    def move(self, world, direction):
        if self.alive:
            self.coords = self.coords + direction
