import unittest

from world import World
from player import Player
from vector import Vec2D
from static_objects import Bullet


class TestPlayer(unittest.TestCase):
    def setUp(self):
        self.world = World("./assets/simple_map.txt", False)
        self.player = Player([Vec2D(40, 64), Vec2D(41, 64),
                              Vec2D(40, 65), Vec2D(41, 65)], 1)

    def tearDown(self):
        del self.world
        del self.player

    def test_valid(self):
        self.assertFalse(self.player.valid(Vec2D(7, 102), self.world.world))
        self.assertFalse(self.player.valid(Vec2D(-2, 62), self.world.world))
        self.assertTrue(self.player.valid(Vec2D(89, 65), self.world.world))

    def test_valid_direction(self):
        result1 = self.player.valid_direction(Vec2D(4, 0), self.world.world)
        result2 = self.player.valid_direction(Vec2D(-8, 0), self.world.world)
        self.assertFalse(result1)
        self.assertTrue(result2)

    def test_valid_move(self):
        answer = [Vec2D(36, 64), Vec2D(37, 64), Vec2D(36, 65), Vec2D(37, 65)]
        self.player.move(Vec2D(-4, 0), self.world.world)
        self.assertEqual(self.player.coords, answer)
        self.assertEqual(self.player.angle, 0)

    def test_unvalid_move(self):
        answer = [Vec2D(40, 64), Vec2D(41, 64), Vec2D(40, 65), Vec2D(41, 65)]
        self.player.move(Vec2D(-48, 0), self.world.world)
        self.assertEqual(self.player.coords, answer)
        self.assertEqual(self.player.angle, 0)

    def test_create_bullet(self):
        bullet = self.player.create_bullet()
        self.assertIsInstance(bullet, Bullet)
        self.assertEqual(bullet.owner, "player")

    def test_check_health(self):
        self.player.check_health(40)
        self.assertEqual(self.player.health, 60)
        self.assertFalse(self.player.dead)
        self.player.check_health(70)
        self.assertEqual(self.player.health, -10)
        self.assertTrue(self.player.dead)

    def test_dead_player(self):
        self.player.check_health(100)
        self.assertTrue(self.player.dead)
        answer = [Vec2D(40, 64), Vec2D(41, 64), Vec2D(40, 65), Vec2D(41, 65)]
        self.player.move(Vec2D(3, 0), self.world.world)
        self.assertEqual(self.player.coords, answer)
        self.assertEqual(self.player.angle, 0)


if __name__ == '__main__':
    unittest.main()
