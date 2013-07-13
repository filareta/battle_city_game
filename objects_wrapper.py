from pygame import image, display, key, transform
from pygame import K_UP, K_DOWN, K_LEFT, K_RIGHT, K_SPACE, \
    K_TAB, K_w, K_s, K_a, K_d
from pygame.sprite import Sprite, collide_rect
from pygame.rect import Rect

from vector import Vec2D, to_pixels, to_coords
from settings import ENEMIES, TILE_SIZE, SIZE_X, SIZE_Y, SCREEN_SIZE, RELOAD_TIME

import math


class PlayerWrapper(Sprite):
    bullet = None
    reload_time = 0

    def __init__(self, player):
        super(PlayerWrapper, self).__init__()
        self.player = player
        self.convert(to_pixels)
        self.image = image.load("assets/player{}.png".format(player.turn))

    def has_hit(self, position):
        return self.player.coords.x < position.x < self.player.coords.x + TILE_SIZE and \
            self.player.coords.y < position.y < self.player.coords.y + TILE_SIZE

    def convert(self, function):
        self.player.coords = function(self.player.coords)

    def shoot(self):
        if self.reload_time > 0:
            return

        self.reload_time = RELOAD_TIME
        self.bullet = BulletSprite(self.player.create_bullet())

    def update(self, delta, world, walls):
        if not self.player.dead:
            choice = key.get_pressed()
            if self.player.turn == 1:
                control = (K_UP, K_DOWN, K_LEFT, K_RIGHT, K_SPACE)
                sign = 'Y'
            else:
                control = (K_w, K_s, K_a, K_d, K_TAB)
                sign = 'G'

            direction = Vec2D(0, 0)
            if choice[control[0]]:
                direction = Vec2D(0, -1)
                self.player.angle = 0
            if choice[control[1]]:
                direction = Vec2D(0, 1)
                self.player.angle = -180
            if choice[control[2]]:
                direction = Vec2D(-1, 0)
                self.player.angle = 90
            if choice[control[3]]:
                direction = Vec2D(1, 0)
                self.player.angle = -90

            direction = direction * TILE_SIZE * delta

            if world.enemy_hit_tile(self.player.coords + direction):
                return

            direction = world.validify_direction(self.player.coords, direction)

            # if world.valid_direction(direction, world):
            self.player.move(direction, world.world)

            if not direction.zero():
                world.update_aim_lines()

            if self.reload_time > 0:
                self.reload_time -= delta

            if choice[control[4]]:
                self.shoot()

    def draw(self, screen):
        if not self.player.dead:
            origin = self.image.convert_alpha()
            r = transform.rotate(origin, self.player.angle)
            x, y = self.player.coords.x, self.player.coords.y
            screen.blit(r, (x, y))


class EnemyWrapper(Sprite):
    def __init__(self, enemy, pic):
        super(EnemyWrapper, self).__init__()
        self.enemy = enemy
        self.enemy.turn = pic
        self.convert(to_pixels)
        self.image = image.load("assets/" + ENEMIES[pic])

    def has_hit(self, position):
        return self.enemy.coords.x < position.x < self.enemy.coords.x + TILE_SIZE and \
            self.enemy.coords.y < position.y < self.enemy.coords.y + TILE_SIZE

    def convert(self, function):
        self.enemy.coords = function(self.enemy.coords)

    def bullet(self):
        if self.enemy.bullet:
            return BulletSprite(self.enemy.bullet)

    def bullet_hit(self):
        return self.enemy.bullet_hit()

    def update(self, delta, world):
        direction, player_name = world.get_next_direction(self.enemy.coords)
        direction = direction * delta
        newpos = self.enemy.coords + direction

        if world.player_hit_tile(newpos) or world.enemy_hit_tile(newpos, except_for=self):
            return

        if direction.y > 0:
            self.enemy.angle = 0
        if direction.y < 0:
            self.enemy.angle = -180
        if direction.x > 0:
            self.enemy.angle = 90
        if direction.x < 0:
            self.enemy.angle = -90

        if direction.zero():
            # Look at player
            player_direction = world.players[player_name].coords - self.enemy.coords

            if abs(player_direction.x) > abs(player_direction.y):
                if player_direction.x > 0:
                    self.enemy.angle = 90
                else:
                    self.enemy.angle = -90
            else:
                if player_direction.y > 0:
                    self.enemy.angle = 0
                else:
                    self.enemy.angle = 180

        self.enemy.move(world, direction)

    def draw(self, screen):
        origin = self.image.convert_alpha()
        r = transform.rotate(origin, self.enemy.angle)
        screen.blit(r, (self.enemy.coords.x, self.enemy.coords.y))


class BulletSprite(Sprite):
    def __init__(self, bullet):
        super(BulletSprite, self).__init__()
        self.bullet = bullet
        self.image = image.load("assets/bullet.png")

    def update(self, world, delta):
        self.bullet.flight(world, delta)

    def draw(self, screen):
        origin = self.image.convert_alpha()
        rotated = transform.rotate(origin, self.bullet.angle)
        screen.blit(rotated, (self.bullet.pos.x, self.bullet.pos.y))
