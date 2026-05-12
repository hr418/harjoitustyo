import unittest
from unittest.mock import Mock
from algorithms.base import PathfindingAlgorithm


class TestPathfindingAlgorithm(unittest.TestCase):
    def setUp(self):
        self.algorithm = PathfindingAlgorithm(None)

    def test_initialization(self):
        self.assertIsInstance(self.algorithm, PathfindingAlgorithm)

    def test_search_step_not_implemented(self):
        with self.assertRaises(NotImplementedError):
            self.algorithm.search_step()

    def test_reconstruct_step_not_implemented(self):
        with self.assertRaises(NotImplementedError):
            self.algorithm.reconstruct_step()


class TestMeasurePerformance(unittest.TestCase):
    def setUp(self):
        class Algorithm(PathfindingAlgorithm):
            def search_step(self):
                yield ([], [])

            def reconstruct_step(self):
                return None

        self.mock_pixel_map = Mock()
        self.algorithm = Algorithm(self.mock_pixel_map)

    def test_measure_performance_integration(self):
        result = self.algorithm.measure_performance()

        self.assertIsInstance(result, float)
        self.assertGreater(result, 0)
