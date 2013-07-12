from pygame import image, Rect
from pygame.sprite import Group, spritecollide, collide_rect

from world import World
from collider import rect_collision, reactor
from vector import to_coords, to_pixels
from objects_wrapper import PlayerWrapper, EnemyWrapper
from settings import TILE_SIZE, SIZE_X, SIZE_Y
from vector import Vec2D

import math


class WorldWrapper(World):
    player_sprites = {'1': None, '2': None}
    enemy_sprites = []
    wall_rects = []
    bullets = []
    game_over = False

    def __init__(self, world_map, multiplayer):
        World.__init__(self, world_map, multiplayer)
        self._create_sprites()
        self._set_walls()

    def _set_walls(self):
        wall_pic = image.load("assets/brick.png")
        for wall in self.walls:
            x, y = to_pixels(wall.coords)
            self.wall_rects.append(Rect((x, y), wall_pic.get_size()))

    def _create_sprites(self):
        for key, player in self.players.items():
            if player:
                self.player_sprites[key] = PlayerWrapper(player)
        for enemy in self.enemies:
            new_enemy = EnemyWrapper(enemy, len(self.enemy_sprites) % 2)
            self.enemy_sprites.append(new_enemy)

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
        self.draw_phoenix(screen)

    def get_all_block_coords(self, pixels_x, pixels_y):
        blocks = []

        blocks.append(self.get_block_coords(pixels_x, pixels_y))
        if pixels_x % TILE_SIZE != 0:
            blocks.append(self.get_block_coords(pixels_x + TILE_SIZE, pixels_y))

        if pixels_y % TILE_SIZE != 0:
            blocks.append(self.get_block_coords(pixels_x, pixels_y + TILE_SIZE))

        if pixels_x % TILE_SIZE != 0 and pixels_y % TILE_SIZE != 0:
            blocks.append(self.get_block_coords(pixels_x + TILE_SIZE, pixels_y + TILE_SIZE))

        return blocks

    def get_block_coords(self, pixels_x, pixels_y):
        return Vec2D(math.floor(math.floor(pixels_x) / TILE_SIZE), math.floor(math.floor(pixels_y) / TILE_SIZE))

    def valid_position(self, position):
        blocks = self.get_all_block_coords(position.x, position.y)

        for tile in blocks:
            if not self.is_inside(tile) or not self[tile.x][tile.y].passable():
                return False

        return True

    def _tile_size_if_0(self, value):
        return value if value > 0 else TILE_SIZE

    def validify_direction(self, current_position, direction):
        """ Works only when direction is not diagonal """
        newpos = current_position + direction

        if self.valid_position(newpos):
            return direction

        if direction.x > 0:
            next_block = self.get_block_coords(current_position.x + direction.x + TILE_SIZE, current_position.y)
            direction.x = TILE_SIZE - self._tile_size_if_0(current_position.x % TILE_SIZE)
        elif direction.x < 0:
            next_block = self.get_block_coords(current_position.x + direction.x, current_position.y)
            direction.x = -(current_position.x % TILE_SIZE)
        elif direction.y > 0:
            next_block = self.get_block_coords(current_position.x, current_position.y + direction.y + TILE_SIZE)
            direction.y = TILE_SIZE - self._tile_size_if_0(current_position.y % TILE_SIZE)
        elif direction.y < 0:
            next_block = self.get_block_coords(current_position.x, current_position.y + direction.y)
            direction.y = -(current_position.y % TILE_SIZE)

        return direction

    def is_inside(self, position):
        return 0 <= position.x < SIZE_X and 0 <= position.y < SIZE_Y

    def draw_phoenix(self, screen):
        phoenix = image.load("assets/phoenix.png")
        x, y = to_pixels(self.phoenix[0])
        position = Rect((x, y), phoenix.get_size())
        screen.blit(phoenix, (position.x, position.y))

    def draw_walls(self, screen):
        wall_pic = image.load("assets/brick.png")
        for wall in self.wall_rects:
            screen.blit(wall_pic, (wall.x, wall.y))

    def is_over(self):
        if self.multiplayer:
            if self.player_sprites['1'].player.dead and \
                    self.player_sprites['2'].player.dead:
                self.game_over = True
        elif self.player_sprites['1'].player.dead:
            self.game_over = True

    def update(self, delta):
        for key, sprite in self.player_sprites.items():
            if sprite:
                sprite.update(delta, self, self.wall_rects)
        #         if sprite.bullet:
        #             self.bullets.append(sprite.bullet)

        # for index, enemy in enumerate(self.enemy_sprites):
        #     if self.player_sprites['2']:
        #         dir1 = self.player_sprites['1'].player.direction
        #         if not dir1.zero():
        #             enemy.update(dir1,
        #                          self.world, index, self,
        #                          self.player_sprites['1'].player.coords[0])
        #         elif self.multiplayer:
        #             dir2 = self.player_sprites['2'].player.direction
        #             enemy.update(dir2, self.world, index, self,
        #                          self.player_sprites['2'].player.coords[0])
        #     else:
        #         enemy.update(self.player_sprites['1'].player.direction,
        #                      self.world, index, self,
        #                      self.player_sprites['1'].player.coords[0])
        #     bullet = enemy.bullet()
        #     if bullet:
        #         self.bullets.append(bullet)

        # for key, sprite in self.player_sprites.items():
        #     for enemy_sprite in self.enemy_sprites:
        #         if sprite:
        #             side = rect_collision(enemy_sprite.rect, sprite.rect)
        #             if side:
        #                 reactor(side, enemy_sprite.rect)

        # for key, sprite in self.player_sprites.items():
        #     for bullet_sprite in self.bullets:
        #         if sprite and bullet_sprite.bullet.owner == "enemy" and rect_collision(bullet_sprite.rect, sprite.rect):
        #             sprite.player.check_health(10)

        # for enemy_sprite in self.enemy_sprites:
        #     for sprite in self.bullets:
        #         if sprite.bullet.owner == "player" and rect_collision(enemy_sprite.rect, sprite.rect):
        #             enemy_sprite.enemy.check_health()

        # for bullet_sprite in self.bullets:
        #     if bullet_sprite.bullet.ttl:
        #         bullet_sprite.update(self.world, delta)
        #     else:
        #         bullet_sprite.active = False

        # self.kill()
        # self.bullets = [bullet for bullet in self.bullets if bullet.active]
        # [sprite for sprite in self.enemy_sprites if sprite.enemy.alive]
        # self.is_over()
        # self.convert(to_pixels)
