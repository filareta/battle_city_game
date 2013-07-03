from pygame import image, Rect
from pygame.sprite import Group, spritecollide, collide_rect

from world import World
from vector import to_coords, to_pixels
from objects_wrapper import PlayerWrapper, EnemyWrapper
from settings import TILE_SIZE


class WorldWrapper(World):
    player_sprites = {'1': None, '2': None}
    enemy_sprites = []
    wall_pics = []
    bullets = []

    def __init__(self, world_map, multiplayer):
        World.__init__(self, world_map, multiplayer)
        self._create_sprites()
        self.brick_energy()
        self.set_bounds_energy()
        self.set_dynamics_energy()
        self._set_walls()

    def _set_walls(self):
        wall_pic = image.load("assets/brick.png")
        for wall in self.walls:
            x, y = to_pixels(wall.coords[0])
            self.wall_pics.append(Rect((x, y), wall_pic.get_size()))

    def _create_sprites(self):
        for key, player in self.players.items():
            if player:
                self.player_sprites[key] = PlayerWrapper(player)
        for enemy in self.enemies:
            self.enemy_sprites.append(EnemyWrapper(enemy, len(self.enemy_sprites) % 2))

    def draw(self, screen):
        for key, player in self.player_sprites.items():
            if player:
                player.draw(screen)
        for enemy in self.enemy_sprites:
            enemy.draw(screen)
        for bullet_sprite in self.bullets:
            if bullet_sprite.bullet.ttl:
                bullet_sprite.draw(screen)
        self.draw_walls(screen)

    def draw_walls(self, screen):
        wall_pic = image.load("assets/brick.png")
        for wall in self.wall_pics:
            screen.blit(wall_pic, (wall.x, wall.y))

    def convert(self, function):
        for key, sprite in self.player_sprites.items():
            if sprite:
                sprite.convert(function)
        for enemy in self.enemy_sprites:
            enemy.convert(function)

    def update(self, delta):
        self.convert(to_coords)
        for key, sprite in self.player_sprites.items():
            if sprite:
                sprite.update(delta, self, self.wall_pics)
                if sprite.bullet:
                    self.bullets.append(sprite.bullet)
        for index, enemy in enumerate(self.enemy_sprites):
            if self.player_sprites['2']:
                dir1 = self.player_sprites['1'].player.direction
                if not dir1.zero():
                    enemy.update(dir1, delta, self.world, index, self)
                else:
                    dir2 = self.player_sprites['2'].player.direction
                    enemy.update(dir2, delta, self.world, index, self)
            else:
                enemy.update(self.player_sprites['1'].player.direction, delta, self.world, index, self)
            bullet = enemy.bullet()
            if bullet:
                self.bullets.append(bullet)
        for key, sprite in self.player_sprites.items():
            for enemy_sprite in self.enemy_sprites:
                if sprite and collide_rect(enemy_sprite, sprite):
                    sprite.player.check_health(10)
        for key, sprite in self.player_sprites.items():
            for bullet_sprite in self.bullets:
                if sprite and bullet_sprite.bullet.owner == "enemy" \
                   and collide_rect(bullet_sprite, sprite):
                    sprite.player.check_health(20)
        for enemy_sprite in self.enemy_sprites:
            for sprite in self.bullets:
                if sprite.bullet.owner == "player" and \
                   collide_rect(sprite, enemy_sprite):
                    enemy_sprite.enemy.check_health()
        self.convert(to_pixels)
        for bullet_sprite in self.bullets:
            if bullet_sprite.bullet.ttl:
                bullet_sprite.update(self.world, delta)
            else:
                bullet_sprite.active = False
        self.bullets = [bullet for bullet in self.bullets if bullet.active]
        self.enemy_sprites = \
        [sprite for sprite in self.enemy_sprites if sprite.enemy.alive]