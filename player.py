from pygame import image, display, key, transform
from pygame import K_UP, K_DOWN, K_LEFT, K_RIGHT, K_w, K_s, K_a, K_d
from pygame.sprite import Sprite
from pygame.rect import Rect

from vector import Vec2D
from settings import TILE_SIZE, SIZE_X, SIZE_Y
from static_objects import Bullet


class Player(Sprite):
    coords = []
    direction = Vec2D(0, 0)
    last_dir = Vec2D(0, -1)
    angle = 0
    health = 100
    dead = False

    def __init__(self, coords, turn):
        self.coords = coords
        self.turn = turn

    def valid_direction(self, direction, world):
        return self.valid(self.coords[0] + direction, world) and \
               self.valid(self.coords[-1] + direction, world)

    def valid(self, cell, world):
        return cell[0] >= 0 and cell[0] < SIZE_X and cell[1] >= 0 and cell[1] < SIZE_Y and \
               world[cell[0]][cell[1]].empty()

    def move(self, direction, world):
        if not self.dead:
            if self.valid_direction(direction, world):
                self.direction = direction
                self.last_dir = direction
                for i, position in enumerate(self.coords):
                    ind1, ind2 = self.coords[i]
                    move = position + direction
                    world[move[0]][move[1]].energy += world[ind1][ind2].energy
                    self.coords[i] = move

    def create_bullet(self):
        if self.direction.zero():
            return Bullet(self.coords[2] + self.last_dir * 4, self.last_dir, self.angle, "player")
        else:
            return Bullet(self.coords[2] + self.direction * 4, self.direction, self.angle, "player")

    def check_health(self, decrease):
        self.health -= decrease
        if self.health <= 0:
            self.dead = True
