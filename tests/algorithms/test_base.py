import unittest
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
