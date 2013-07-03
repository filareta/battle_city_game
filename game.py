import pygame
from pygame import image, rect, display, key, K_UP, K_DOWN, K_SPACE

from settings import SCREEN_SIZE, MAPS
from player import Player
from world import Tile, World
from vector import Vec2D
from world_wrapper import WorldWrapper


class Game:
    running = True
    start = False
    level = 1
    multiplayer = False
    world = None

    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode(SCREEN_SIZE)
        self.clock = pygame.time.Clock()
        self._init_screen()


    def _init_screen(self):
        self.background = image.load("assets/start.png")
        self.pointer = image.load("assets/pointer.png")
        self.back = rect.Rect((0, 0), self.background.get_size())
        self.point = rect.Rect((170, 310), self.pointer.get_size())
        self.screen.blit(self.background, (self.back.x, self.back.y))
        self.screen.blit(self.pointer, (self.point.x, self.point.y))


    def init_game(self):
        init = (K_DOWN, K_UP, K_SPACE)
        move = key.get_pressed()
        if move[init[0]] and self.point.top == 310:
            self.point.top += 40
            self.multiplayer = True
        elif move[init[1]] and self.point.top == 350:
            self.point.top -= 40
            self.multiplayer = False
        if move[init[2]]:
            self.start = True
            self.world = WorldWrapper(MAPS[self.level], self.multiplayer)
        self.screen.blit(self.background, (self.back.x, self.back.y))
        self.screen.blit(self.pointer, (self.point.x, self.point.y))

    def game_loop(self, fps):
        while self.running:
            dt = self.clock.tick(fps)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                   return
            if self.start:
                self.world.update(dt / 100)
                self.screen.fill((0, 0, 0))
                self.world.draw(self.screen)
            else:
                self.init_game()
            pygame.display.flip()

Game().game_loop(30)