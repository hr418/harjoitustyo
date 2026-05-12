import unittest
from unittest.mock import Mock
import random

from algorithms.a_star import AStar
from algorithms.jump_point_search import JumpPointSearch
from pixel_map import PixelMap


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

    def test_astar_and_jps_find_same_path_length(self):
        for iteration in range(10):
            with self.subTest(iteration=iteration):
                mock_pixel_map = Mock()

                start = (random.randint(0, 49), random.randint(0, 49))
                end = (random.randint(0, 49), random.randint(0, 49))

                while start == end:
                    end = (random.randint(0, 49), random.randint(0, 49))

                mock_pixel_map.start = start
                mock_pixel_map.end = end

                def is_walkable(pos):
                    return 0 <= pos[0] < 50 and 0 <= pos[1] < 50

                mock_pixel_map.is_walkable = is_walkable

                astar = AStar(mock_pixel_map)
                jps = JumpPointSearch(mock_pixel_map)

                for _ in astar.search_step():
                    pass

                for _ in jps.search_step():
                    pass

                self.assertTrue(astar.done)
                self.assertTrue(jps.done)
                self.assertAlmostEqual(astar.path_length, jps.path_length, places=5)


class TestAlgorithmsSearch(unittest.TestCase):
    def setUp(self):
        self.mock_pixel_map = Mock()
        self.mock_pixel_map.start = (0, 0)
        self.mock_pixel_map.end = (2, 0)

    def test_search_finds_direct_path(self):
        def is_walkable(pos):
            return 0 <= pos[0] <= 2 and pos[1] == 0

        self.mock_pixel_map.is_walkable = is_walkable

        for AlgorithmClass in [AStar, JumpPointSearch]:
            with self.subTest(algorithm=AlgorithmClass.__name__):
                algorithm = AlgorithmClass(self.mock_pixel_map)
                search_generator = algorithm.search_step()
                try:
                    while not algorithm.done:
                        next(search_generator)
                except StopIteration:
                    pass

                self.assertTrue(algorithm.done)

    def test_search_with_unreachable_goal(self):
        def is_walkable(pos):
            if pos == (2, 0):
                return False
            return 0 <= pos[0] <= 2 and 0 <= pos[1] <= 0

        self.mock_pixel_map.is_walkable = is_walkable

        for AlgorithmClass in [AStar, JumpPointSearch]:
            with self.subTest(algorithm=AlgorithmClass.__name__):
                algorithm = AlgorithmClass(self.mock_pixel_map)
                search_generator = algorithm.search_step()
                try:
                    for _ in range(5):
                        next(search_generator)
                except StopIteration:
                    pass

                self.assertFalse(
                    algorithm.done or (2, 0) in getattr(algorithm, "closed_set", set())
                )

    def test_algorithm_marks_done_when_goal_reached(self):
        def is_walkable(pos):
            return 0 <= pos[0] <= 2 and pos[1] == 0

        self.mock_pixel_map.is_walkable = is_walkable

        for AlgorithmClass in [AStar, JumpPointSearch]:
            with self.subTest(algorithm=AlgorithmClass.__name__):
                algorithm = AlgorithmClass(self.mock_pixel_map)

                search_generator = algorithm.search_step()
                try:
                    while not algorithm.done:
                        next(search_generator)
                except StopIteration:
                    pass

                self.assertTrue(algorithm.done)
