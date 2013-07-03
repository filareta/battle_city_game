import unittest

import path_script
from world import Tile, World
from player import Player
from static_objects import Wall
from vector import Vec2D

class TestWorld(unittest.TestCase):
    def setUp(self):
        self.world = World("../assets/simple_map.txt", False)

    def tearDown(self):
        del self.world

    def test_create_player_1(self):
        coords = [Vec2D(40, 64), Vec2D(41, 64), Vec2D(40, 65), Vec2D(41, 65)]
        self.world._create_object('Y', coords)
        self.assertIsInstance(self.world.players['1'], Player)

    def test_without_second_player(self):
        coords = [Vec2D(38, 63), Vec2D(39, 63), Vec2D(38, 64), Vec2D(39, 64)]
        self.world._create_object('G', coords)
        self.assertIsNone(self.world.players['2'])

    def test_create_wall(self):
        coords = [Vec2D(12, 64), Vec2D(13, 64), Vec2D(12, 65), Vec2D(13, 65)]
        wall = Wall(coords)
        self.world._create_object('B', coords)
        self.assertIn(wall, self.world.walls)

    def test_extend_map(self):
        extended = [Vec2D(38, 63), Vec2D(39, 63), Vec2D(40, 63), Vec2D(41, 63),
                    Vec2D(38, 64), Vec2D(39, 64), Vec2D(40, 64), Vec2D(41, 64),
                    Vec2D(38, 65), Vec2D(39, 65), Vec2D(40, 65), Vec2D(41, 65),
                    Vec2D(38, 66), Vec2D(39, 66), Vec2D(40, 66), Vec2D(41, 66)]
        wall = Wall(extended)
        self.world._extend_map(63, 38, 'B')
        self.assertIn(wall, self.world.walls)

    def test_set_bounds(self):
        self.world._extend_map(65, 0, '#')
        self.assertIn(Vec2D(0, 65), self.world.bounds)
        self.assertNotIn(Vec2D(1, 65), self.world.bounds)


if __name__ == '__main__':
    unittest.main()