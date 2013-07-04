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

    def test_set_wall_energy(self):
        coords = [Vec2D(12, 64), Vec2D(13, 64), Vec2D(12, 65), Vec2D(13, 65)]
        self.world.set_energy('B', coords)
        for x, y in coords:
            self.assertEqual(self.world.world[x][y].energy, -15)

    def test_set_player_energy(self):
        coords = [Vec2D(12, 64), Vec2D(13, 64), Vec2D(12, 65), Vec2D(13, 65)]
        self.world.set_energy('Y', coords)
        for x, y in coords:
            self.assertEqual(self.world.world[x][y].energy, 5)

    def test_set_enemy_energy(self):
        coords = [Vec2D(12, 64), Vec2D(13, 64), Vec2D(12, 65), Vec2D(13, 65)]
        self.world.set_energy('E', coords)
        for x, y in coords:
            self.assertEqual(self.world.world[x][y].energy, -5)

    def test_set_content(self):
        coords = [Vec2D(12, 64), Vec2D(13, 64), Vec2D(12, 65), Vec2D(13, 65)]
        self.world.set_content('E', coords)
        for x, y in coords:
            self.assertEqual(self.world.world[x][y].content, 'E')

    def test_clear_player(self):
        coords = [Vec2D(12, 64), Vec2D(13, 64), Vec2D(12, 65), Vec2D(13, 65)]
        self.world.set_content('Y', coords)
        self.world.set_energy('Y', coords)
        self.world.clear_content(Vec2D(12, 64), 'Y')
        for x, y in coords:
            self.assertEqual(self.world.world[x][y].content, '0')
            self.assertEqual(self.world.world[x][y].energy, 5)

    def test_clear_enemy_with_energy(self):
        coords = [Vec2D(12, 64), Vec2D(13, 64), Vec2D(12, 65), Vec2D(13, 65)]
        self.world.set_content('E', coords)
        self.world.set_energy('E', coords)
        self.world.clear_content(Vec2D(12, 64), 'E')
        for x, y in coords:
            self.assertEqual(self.world.world[x][y].content, '0')
            self.assertEqual(self.world.world[x][y].energy, 0)

    def test_in_range(self):
        self.assertTrue(self.world.in_range(45, 71))
        self.assertFalse(self.world.in_range(45, 73))
        self.assertFalse(self.world.in_range(101, 71))
        self.assertFalse(self.world.in_range(-1, 71))

    def test_neighbours(self):
        coords = [Vec2D(12, 64), Vec2D(13, 64), Vec2D(12, 65), Vec2D(13, 65)]
        self.world.set_energy('E', coords)
        filtered = self.world.neighbours(Vec2D(11, 64))
        answer = [Vec2D(10, 64), Vec2D(11, 63), Vec2D(11, 65)]
        for cell in filtered:
            self.assertIn(cell, answer)

    def test_spread_energy(self):
        coords = [Vec2D(12, 64), Vec2D(13, 64), Vec2D(12, 65), Vec2D(13, 65)]
        self.world.set_energy('Y', coords)
        self.world.spread(3, Vec2D(12, 64))
        self.assertEqual(self.world.world[11][64].energy, 6)
        self.assertEqual(self.world.world[13][64].energy, 5)
        self.assertEqual(self.world.world[10][64].energy, 7)
        self.assertEqual(self.world.world[11][63].energy, 7)








if __name__ == '__main__':
    unittest.main()