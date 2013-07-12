from pygame import image, Rect
from pygame.sprite import Group, spritecollide, collide_rect

from world import World
from collider import rect_collision, reactor
from vector import to_coords, to_pixels
from objects_wrapper import PlayerWrapper, EnemyWrapper
from settings import TILE_SIZE


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

    def draw_phoenix(self, screen):
        phoenix = image.load("assets/phoenix.png")
        x, y = to_pixels(self.phoenix[0])
        position = Rect((x, y), phoenix.get_size())
        screen.blit(phoenix, (position.x, position.y))

    def draw_walls(self, screen):
        wall_pic = image.load("assets/brick.png")
        for wall in self.wall_rects:
            screen.blit(wall_pic, (wall.x, wall.y))

    def convert(self, function):
        for key, sprite in self.player_sprites.items():
            if sprite:
                sprite.convert(function)
        for enemy in self.enemy_sprites:
            enemy.convert(function)

    def is_over(self):
        if self.multiplayer:
            if self.player_sprites['1'].player.dead and \
                    self.player_sprites['2'].player.dead:
                self.game_over = True
        elif self.player_sprites['1'].player.dead:
            self.game_over = True

    def update(self, delta):
        self.convert(to_coords)
        for key, sprite in self.player_sprites.items():
            pass
            # if sprite:
                # sprite.update(delta, self, self.wall_rects)
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
