import unittest
from pixel_map import PixelMap


class TestPixelMap(unittest.TestCase):
    def setUp(self):
        self.pixel_map = PixelMap("tests/maps/10x10-white.png", (0, 0), (9, 9))

    def test_initialization(self):
        self.assertEqual(self.pixel_map.start, (0, 0))
        self.assertEqual(self.pixel_map.end, (9, 9))
        self.assertEqual(self.pixel_map.width, 10)
        self.assertEqual(self.pixel_map.height, 10)

    def test_is_walkable(self):

        for x in range(10):
            for y in range(10):
                print(f"Testing walkability of ({x}, {y})")
                self.assertTrue(self.pixel_map.is_walkable((x, y)))

    def test_not_walkable(self):
        black_map = PixelMap("tests/maps/10x10-black.png", (0, 0), (9, 9))

        for x in range(10):
            for y in range(10):
                self.assertFalse(black_map.is_walkable((x, y)))

        self.assertFalse(self.pixel_map.is_walkable((-1, 0)))
        self.assertFalse(self.pixel_map.is_walkable((0, -1)))
        self.assertFalse(self.pixel_map.is_walkable((10, 0)))
        self.assertFalse(self.pixel_map.is_walkable((0, 10)))
