from pygame import image, Rect
from pygame.sprite import Group, spritecollide, collide_rect

from world import World
from collider import rect_collision, reactor
from vector import to_coords, to_pixels
from objects_wrapper import PlayerWrapper, EnemyWrapper, WallWrapper
from settings import TILE_SIZE, SIZE_X, SIZE_Y
from vector import Vec2D

import math


class WorldWrapper(World):
    player_sprites = {'1': None, '2': None}
    enemy_sprites = set()
    wall_rects = []
    unbreakable_wall_rects = []
    bullets = set()

    game_over = False

    def __init__(self, world_map, multiplayer):
        World.__init__(self, world_map, multiplayer)
        self._create_sprites()
        self._set_walls()
        self.update_aim_lines()

    def _set_walls(self):
        wall_pic = image.load("assets/brick.png")
        for wall in self.walls:
            x, y = to_pixels(wall.coords)
            wall_rect = WallWrapper(wall, (x, y), wall_pic.get_size())

            self.wall_rects.append(wall_rect)

    def _create_sprites(self):
        for key, player in self.players.items():
            if player:
                self.player_sprites[key] = PlayerWrapper(player)
        for enemy in self.enemies:
            new_enemy = EnemyWrapper(enemy, len(self.enemy_sprites) % 2)
            self.enemy_sprites.add(new_enemy)

    def draw(self, screen):
        for key, player in self.player_sprites.items():
            if player:
                player.draw(screen)
        for enemy in self.enemy_sprites:
            enemy.draw(screen)
        for bullet_sprite in self.bullets:
            bullet_sprite.draw(screen)
        self.draw_walls(screen)
        self.draw_phoenix(screen)

    def draw_phoenix(self, screen):
        phoenix = image.load("assets/phoenix.png")
        x, y = to_pixels(self.phoenix[0])
        position = Rect((x, y), phoenix.get_size())
        screen.blit(phoenix, (position.x, position.y))

    def draw_walls(self, screen):
        wall_pic = image.load("assets/brick.png")
        unbreakable_wall_pic = image.load("assets/wall.png")

        for wall in self.wall_rects:
            if wall.wall.breakable:
                screen.blit(wall_pic, (wall.x, wall.y))
            else:
                screen.blit(unbreakable_wall_pic, (wall.x, wall.y))

    def is_over(self):
        if self.multiplayer:
            if self.player_sprites['1'].player.dead and \
                    self.player_sprites['2'].player.dead:
                self.game_over = True
        elif self.player_sprites['1'].player.dead:
            self.game_over = True

    def update(self, delta):
        for key, sprite in self.player_sprites.items():
            if sprite and not sprite.player.dead:
                sprite.update(delta, self, self.wall_rects)
                if sprite.bullet:
                    self.bullets.add(sprite.bullet)
                    sprite.bullet = None

        for index, enemy in enumerate(self.enemy_sprites):
            enemy.update(delta, self)

            if enemy.bullet:
                self.bullets.add(enemy.bullet)
                enemy.bullet = None

        for bullet_sprite in self.bullets:
            if bullet_sprite.bullet.active:
                bullet_sprite.update(self, delta)

                tile = self.get_block_coords(bullet_sprite.bullet.pos.x, bullet_sprite.bullet.pos.y)
                if self[tile.x][tile.y].is_brick():
                    bullet_sprite.bullet.active = False
                    self[tile.x][tile.y].content = '0'

                    self.wall_rects = [
                        wall for wall in self.wall_rects if wall.x != tile.x * TILE_SIZE or wall.y != tile.y * TILE_SIZE
                    ]

                    self.update_aim_lines()
                elif self[tile.x][tile.y].is_wall():
                    bullet_sprite.bullet.active = False

                if bullet_sprite.bullet.owner == "player":
                    enemy_hit = self.enemy_hit(bullet_sprite.bullet.pos)

                    if enemy_hit:
                        bullet_sprite.bullet.active = False
                        enemy_hit.bullet_hit()

                        if not enemy_hit.enemy.alive:
                            self.enemy_sprites.remove(enemy_hit)
                else:
                    player_hit = self.player_hit(bullet_sprite.bullet.pos)

                    if player_hit:
                        bullet_sprite.bullet.active = False
                        player_hit.bullet_hit()
                        self.update_aim_lines()

        self.bullets = {bullet for bullet in self.bullets if bullet.bullet.active}

        # self.kill()
        self.is_over()
