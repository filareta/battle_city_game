import pygame
from pygame import image, rect, display, key, K_UP, K_DOWN, K_SPACE, K_LSHIFT

from settings import SCREEN_SIZE, MAPS
from player import Player
from world import Tile, World
from vector import Vec2D
from world_wrapper import WorldWrapper


class Game:
    running = True
    start = False
    game_over = False
    restart = False
    multiplayer = False
    world = None
    quit = False

    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode(SCREEN_SIZE)
        self.clock = pygame.time.Clock()
        self.buttons = (K_DOWN, K_UP, K_SPACE, K_LSHIFT)
        self.background = image.load("assets/start.png")
        self.pointer = image.load("assets/pointer.png")
        self.over_screen = image.load("assets/game_over.png")
        self.back = rect.Rect((0, 0), self.background.get_size())
        self.over = rect.Rect((0, 0), self.over_screen.get_size())
        self.point = rect.Rect((250, 370), self.pointer.get_size())
        self._init_screen()

    def _init_screen(self):
        self.level = 1
        self.point.left = 250
        self.point.top = 370
        self.screen.blit(self.background, (self.back.x, self.back.y))
        self.screen.blit(self.pointer, (self.point.x, self.point.y))

    def _game_over(self):
        self.game_over = True
        self.point.top = 480
        self.point.left = 310
        self.screen.blit(self.over_screen, (self.over.x, self.over.y))
        self.screen.blit(self.pointer, (self.point.x, self.point.y))

    def init_game(self):
        move = key.get_pressed()
        if move[self.buttons[0]] and self.point.top == 370:
            self.point.top += 60
            self.multiplayer = True
        elif move[self.buttons[1]] and self.point.top == 430:
            self.point.top -= 60
            self.multiplayer = False
        if move[self.buttons[2]]:
            self.start = True
            self.world = WorldWrapper(MAPS[self.level], self.multiplayer)
        self.screen.blit(self.background, (self.back.x, self.back.y))
        self.screen.blit(self.pointer, (self.point.x, self.point.y))

    def restart_game(self):
        move = key.get_pressed()
        if move[self.buttons[0]] and self.point.top == 480:
            self.point.top += 60
            self.restart = False
        elif move[self.buttons[1]] and self.point.top == 540:
            self.point.top -= 60
            self.restart = True
        elif move[self.buttons[3]]:
            self.quit = True
            if self.restart:
                Game().game_loop(30)
        self.screen.blit(self.over_screen, (self.over.x, self.over.y))
        self.screen.blit(self.pointer, (self.point.x, self.point.y))

    def game_loop(self, fps):
        while self.running:
            dt = self.clock.tick(fps)
            for event in pygame.event.get():
                if event.type == pygame.QUIT or self.quit:
                    return
            if not self.game_over:
                if self.start:
                    self.world.update(dt / 100)
                    self.screen.fill((0, 0, 0))
                    self.world.draw(self.screen)
                    if self.world.game_over:
                        self._game_over()
                else:
                    self.init_game()
            else:
                self.restart_game()
            pygame.display.flip()


Game().game_loop(30)
