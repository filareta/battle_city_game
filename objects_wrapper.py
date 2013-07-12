from pygame import image, display, key, transform
from pygame import K_UP, K_DOWN, K_LEFT, K_RIGHT, K_SPACE, \
    K_TAB, K_w, K_s, K_a, K_d
from pygame.sprite import Sprite, collide_rect
from pygame.rect import Rect

from vector import Vec2D, to_pixels, to_coords
from settings import ENEMIES, TILE_SIZE, SIZE_X, SIZE_Y, SCREEN_SIZE


class PlayerWrapper(Sprite):
    bullet = None

    def __init__(self, player):
        super(PlayerWrapper, self).__init__()
        self.player = player
        self.convert(to_pixels)
        self.image = image.load("assets/player{}.png".format(player.turn))
        x, y = player.coords[0], player.coords[1]

    def convert(self, function):
        self.player.coords = function(self.player.coords)

    def shoot(self):
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

            # for wall in walls:
            #     if self.rect.colliderect(wall):
            #         direction = Vec2D(0, 0)
            #         self.rect.left -= x
            #         self.rect.top -= y

            self.player.move(direction * TILE_SIZE * delta, world.world)

            # if choice[control[4]]:
            #     self.shoot()

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
        x, y = self.enemy.coords[0][0], self.enemy.coords[0][1]
        self.rect = Rect((x, y), self.image.get_size())

    def convert(self, function):
        self.enemy.coords = [function(tile) for tile in self.enemy.coords]

    def bullet(self):
        if self.enemy.bullet:
            return BulletSprite(self.enemy.bullet)

    def update(self, direction, world, index, cls, player):
        if self.enemy.direction.zero():
            self.enemy.direction = -direction
        cls.clear_content(self.enemy.coords[0], 'E')
        self.enemy.find_neighbours(self.enemy.coords[0], index, world, player)
        self.enemy.move(world)
        cls.set_content('E', self.enemy.coords)
        cls.set_energy('E', self.enemy.coords)
        x, y = self.enemy.direction * TILE_SIZE
        self.rect.left += x
        self.rect.top += y

    def draw(self, screen):
        origin = self.image.convert_alpha()
        r = transform.rotate(origin, self.enemy.angle)
        screen.blit(r, (self.enemy.coords[0][0], self.enemy.coords[0][1]))


class BulletSprite(Sprite):
    active = True

    def __init__(self, bullet):
        super(BulletSprite, self).__init__()
        self.bullet = bullet
        self.image = image.load("assets/bullet.png")
        x, y = to_pixels(self.bullet.pos)
        self.rect = Rect((x, y), self.image.get_size())

    def update(self, world, alpha):
        if self.active:
            self.bullet.flight(world, alpha)
            x, y = self.bullet.direction * self.bullet.ttl
            self.rect.left += x
            self.rect.top += y
            if self.rect.left < 0 or self.rect.top < 0 or \
                    self.rect.left > SCREEN_SIZE[0] or \
                    self.rect.top > SCREEN_SIZE[1]:
                self.active = False

    def draw(self, screen):
        if self.active:
            origin = self.image.convert_alpha()
            rotated = transform.rotate(origin, self.bullet.angle)
            screen.blit(rotated, (self.rect.left, self.rect.top))
