from vector import Vec2D
from settings import TILE_SIZE, SIZE_X, SIZE_Y, PLAYER_HEALTH
from static_objects import Bullet


class Player:
    def __init__(self, coords, turn):
        self.angle = 0
        self.health = PLAYER_HEALTH
        self.dead = False

        self.turn = turn
        self.coords = coords

    def move(self, direction, world):
        if not self.dead:
            self.coords = self.coords + direction

    def create_bullet(self):
        if self.angle == 0:
            start = self.coords + Vec2D(TILE_SIZE/2 - 2, 0)
            return Bullet(start, Vec2D(0, -1), self.angle, "player")
        elif self.angle == -180:
            start = self.coords + Vec2D(TILE_SIZE/2 - 4, TILE_SIZE - 4)
            return Bullet(start, Vec2D(0, 1), self.angle, "player")
        elif self.angle == 90:
            start = self.coords + Vec2D(4, TILE_SIZE/2 - 4)
            return Bullet(start, Vec2D(-1, 0), self.angle, "player")
        elif self.angle == -90:
            start = self.coords + Vec2D(TILE_SIZE - 8, TILE_SIZE/2 - 4)
            return Bullet(start, Vec2D(1, 0), self.angle, "player")

    def bullet_hit(self):
        self.health -= 1
        if self.health <= 0:
            self.dead = True
