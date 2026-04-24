import unittest
from unittest.mock import Mock

from algorithms.a_star import AStar
from algorithms.jump_point_search import JumpPointSearch


class TestIntegration(unittest.TestCase):
    def setUp(self):
        self.mock_pixel_map = Mock()
        self.mock_pixel_map.start = (0, 0)
        self.mock_pixel_map.end = (15, 9)
        self.mock_pixel_map.is_walkable = Mock(return_value=True)

        self.astar = AStar(self.mock_pixel_map)
        self.jps = JumpPointSearch(self.mock_pixel_map)

    def test_astar_and_jps_have_same_heuristic_values(self):
        test_positions = [
            (0, 0),
            (1, 0),
            (0, 1),
            (3, 4),
            (7, 2),
            (10, 10),
            (15, 9),
        ]

        for position in test_positions:
            with self.subTest(position=position):
                self.assertEqual(
                    self.astar._heuristic(position), self.jps._heuristic(position)
                )
