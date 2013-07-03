import unittest

import path_script
from vector import Vec2D, to_pixels, to_coords


class TestVec2D(unittest.TestCase):
    def test_zero(self):
        self.assertTrue(Vec2D(0, 0).zero())
        self.assertFalse(Vec2D(0, 3).zero())

    def test_rotate(self):
        self.assertEqual(Vec2D(-3, 5).rotate(), Vec2D(5, -3))

    def test_distance(self):
        self.assertEqual(Vec2D(5, 3).distance(Vec2D(2, -1)), 5.0)

    def test_multiplication(self):
        self.assertEqual(Vec2D(3, -2) * 3, Vec2D(9, -6))

    def test_addition(self):
        self.assertEqual(Vec2D(1, -4) + Vec2D(3, 2), Vec2D(4, -2))

    def test_subtraction(self):
        self.assertEqual(Vec2D(3, 8) - Vec2D(4, 3), Vec2D(-1, 5))

    def test_floordivision(self):
        self.assertEqual(Vec2D(4, 7) // 2, Vec2D(2, 3))

    def test_negation(self):
        self.assertEqual(-Vec2D(2, -4), Vec2D(-2, 4))

    def test_equation(self):
        self.assertTrue(Vec2D(4, 1) == Vec2D(4, 1))
        self.assertFalse(Vec2D(0, 3) == Vec2D(-2, 3))

    def test_not_equal(self):
        self.assertTrue(Vec2D(-1, 4) != Vec2D(1, 4))
        self.assertFalse(Vec2D(1, 2) != Vec2D(1, 2))

    def test_get_item(self):
        example = Vec2D(4, 3)
        self.assertEqual(example[0], 4)
        self.assertEqual(example[1], 3)
        with self.assertRaises(StopIteration):
            example[3]

    def test_same_direction(self):
        self.assertTrue(Vec2D(2, 0).same_direction(Vec2D(5, 0)))
        self.assertTrue(Vec2D(0, -3).same_direction(Vec2D(0, -6)))
        self.assertFalse(Vec2D(-2, 0).same_direction(Vec2D(5, 0)))
        self.assertFalse(Vec2D(2, 0).same_direction(Vec2D(0, 3)))

class TestConverFunctions(unittest.TestCase):
    def test_to_pixels(self):
        self.assertEqual(to_pixels(Vec2D(2, 3)), Vec2D(20, 30))

    def test_to_coords(self):
        self.assertEqual(to_coords(Vec2D(200, 150)), Vec2D(20, 15))


if __name__ == '__main__':
    unittest.main()