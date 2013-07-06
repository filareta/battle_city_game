import unittest

from enemy import Enemy
from player import Player
from vector import Vec2D
from world import World
from static_objects import Bullet


class TestEnemy(unittest.TestCase):
    def setUp(self):
        self.world = World("./assets/simple_map.txt", False)
        self.enemy = Enemy([Vec2D(40, 64), Vec2D(41, 64),
                            Vec2D(40, 65), Vec2D(41, 65)])

    def tearDown(self):
        del self.world
        del self.enemy

    def test_create_bullet(self):
        self.enemy.create_bullet()
        self.assertIsInstance(self.enemy.bullet, Bullet)
        self.assertEqual(self.enemy.bullet.owner, "enemy")

    def test_must_be_still_alive(self):
        for _ in range(2):
            self.enemy.check_health()
        self.assertTrue(self.enemy.alive)

    def test_must_be_dead(self):
        for _ in range(4):
            self.enemy.check_health()
        self.assertFalse(self.enemy.alive)

    def test_check_direction(self):
        s = Vec2D(23, 34)
        result = self.enemy.check_direction(s, Vec2D(-1, 0), self.world.world)
        self.assertTrue(result)

    def test_detect_player_direction(self):
        self.world.set_content('Y', [Vec2D(14, 34), Vec2D(15, 34)])
        s = Vec2D(13, 34)
        answer = self.enemy.check_direction(s, Vec2D(1, 0), self.world.world)
        self.assertTrue(answer)

    def test_avoid_other_enemy_directio(self):
        self.world.set_content('E', [Vec2D(14, 34), Vec2D(15, 34)])
        s = Vec2D(13, 34)
        answer = self.enemy.check_direction(s, Vec2D(1, 0), self.world.world)
        self.assertFalse(answer)

    def test_in_collision_with_player(self):
        self.world.set_content('Y', [Vec2D(41, 64), Vec2D(42, 64),
                                     Vec2D(41, 65), Vec2D(42, 65)])
        answer = self.enemy.detect_collision(Vec2D(1, 0),
                                             self.world.world, all)
        self.assertTrue(answer)

    def test_in_partial_collision_with_player(self):
        self.world.set_content('Y', [Vec2D(37, 64), Vec2D(38, 64),
                                     Vec2D(37, 65), Vec2D(38, 65)])
        answer = self.enemy.detect_collision(Vec2D(-2, 0),
                                             self.world.world, any)
        self.assertTrue(answer)

    def check_next_position_cell_by_cell(self):
        self.assertTrue(self.world.check_by_cell(Vec2D(-1, 0)))
        result = self.world.set_content('B', [Vec2D(38, 64), Vec2D(39, 64),
                                              Vec2D(38, 65), Vec2D(39, 65)])
        self.assertFalse(result)

    def test_find_next_direction(self):
        coords = [Vec2D(43, 64), Vec2D(44, 64), Vec2D(43, 65), Vec2D(44, 65)]
        self.world.set_content('Y', coords)
        self.world.set_energy('Y', coords)
        self.world.spread(9, coords[0])
        self.world.spread(9, coords[3])
        self.world.spread(9, coords[-1])
        self.world.spread(9, coords[-4])
        self.world.clear_content(self.enemy.coords[0], 'E')
        self.enemy.find_neighbours(self.enemy.coords[0], 2, self.world)
        self.assertEqual(self.enemy.direction, Vec2D(1, 0))

    def test_make_move(self):
        coords = [Vec2D(36, 64), Vec2D(37, 64), Vec2D(36, 65), Vec2D(37, 65)]
        self.world.clear_content(self.enemy.coords[0], 'E')
        self.world.set_energy('Y', coords)
        self.enemy.direction = Vec2D(-4, 0)
        self.enemy.move(self.world)
        self.assertEqual(self.enemy.coords, coords)
        for x, y in coords:
            self.assertEqual(self.world[x][y].energy, 5)
        self.world.set_energy('E', self.enemy.coords)
        for x, y in coords:
            self.assertEqual(self.world[x][y].energy, 0)


if __name__ == '__main__':
    unittest.main()
