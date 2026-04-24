import unittest
import math
from unittest.mock import Mock
from algorithms.a_star import AStar, AStarNode


class TestAStarNode(unittest.TestCase):
    def test_node_initialization(self):
        node = AStarNode((5, 10))
        self.assertEqual(node.position, (5, 10))
        self.assertEqual(node.g_cost, 0)
        self.assertEqual(node.h_cost, 0)
        self.assertIsNone(node.parent)

    def test_node_initialization_with_costs(self):
        node = AStarNode((3, 4), g_cost=5, h_cost=10)
        self.assertEqual(node.position, (3, 4))
        self.assertEqual(node.g_cost, 5)
        self.assertEqual(node.h_cost, 10)

    def test_node_initialization_with_parent(self):
        parent_node = AStarNode((1, 1))
        child_node = AStarNode((2, 2), parent=parent_node)
        self.assertEqual(child_node.parent, parent_node)

    def test_f_cost_calculation(self):
        node = AStarNode((0, 0), g_cost=5, h_cost=10)
        self.assertEqual(node.f_cost, 15)

    def test_node_comparison(self):
        node1 = AStarNode((0, 0), g_cost=5, h_cost=10)
        node2 = AStarNode((1, 1), g_cost=10, h_cost=10)
        self.assertTrue(node1 < node2)


class TestAStarHeuristic(unittest.TestCase):
    def setUp(self):
        self.mock_pixel_map = Mock()
        self.mock_pixel_map.start = (0, 0)
        self.mock_pixel_map.end = (10, 10)
        self.algorithm = AStar(self.mock_pixel_map)

    def test_heuristic_same_position(self):
        result = self.algorithm._heuristic((10, 10))
        self.assertEqual(result, 0)

    def test_heuristic_horizontal_distance(self):
        result = self.algorithm._heuristic((0, 10))
        self.assertAlmostEqual(result, 10)

    def test_heuristic_vertical_distance(self):
        result = self.algorithm._heuristic((10, 0))
        self.assertAlmostEqual(result, 10)

    def test_heuristic_diagonal_distance(self):
        result = self.algorithm._heuristic((0, 0))
        expected = 10 * math.sqrt(2)
        self.assertAlmostEqual(result, expected, places=5)


class TestAStarInitialization(unittest.TestCase):
    def setUp(self):
        self.mock_pixel_map = Mock()
        self.mock_pixel_map.start = (0, 0)
        self.mock_pixel_map.end = (5, 5)

    def test_algorithm_initialization(self):
        algorithm = AStar(self.mock_pixel_map)
        self.assertEqual(algorithm.pixel_map, self.mock_pixel_map)
        self.assertFalse(algorithm.done)

    def test_open_set_initialization(self):
        algorithm = AStar(self.mock_pixel_map)
        self.assertEqual(len(algorithm.open_set), 1)
        start_node = algorithm.open_set[0]
        self.assertEqual(start_node.position, (0, 0))

    def test_closed_set_initialization(self):
        algorithm = AStar(self.mock_pixel_map)
        self.assertEqual(len(algorithm.closed_set), 0)

    def test_g_scores_initialization(self):
        algorithm = AStar(self.mock_pixel_map)
        self.assertEqual(algorithm.g_scores[(0, 0)], 0)


class TestAStarSearch(unittest.TestCase):
    # TEMPORARY, currently nothing similar in JPS tests, should be moved to integration tests
    def setUp(self):
        self.mock_pixel_map = Mock()
        self.mock_pixel_map.start = (0, 0)
        self.mock_pixel_map.end = (2, 0)

    def test_search_finds_direct_path(self):
        self.mock_pixel_map.is_walkable = Mock(return_value=True)
        algorithm = AStar(self.mock_pixel_map)

        # Simulate search steps until goal is found
        search_generator = algorithm.search_step()
        try:
            while not algorithm.done:
                next(search_generator)
        except StopIteration:
            pass

        self.assertTrue(algorithm.done)

    def test_search_with_unreachable_goal(self):
        def is_walkable(pos):
            if pos == (2, 0):  # Goal is not walkable
                return False
            return 0 <= pos[0] <= 2 and 0 <= pos[1] <= 0

        self.mock_pixel_map.is_walkable = is_walkable
        algorithm = AStar(self.mock_pixel_map)

        search_generator = algorithm.search_step()
        try:
            for _ in range(5):
                next(search_generator)
        except StopIteration:
            pass

        # Should not reach the goal
        self.assertFalse(algorithm.done or (2, 0) in algorithm.closed_set)

    def test_algorithm_marks_done_when_goal_reached(self):
        self.mock_pixel_map.is_walkable = Mock(return_value=True)
        algorithm = AStar(self.mock_pixel_map)

        search_generator = algorithm.search_step()
        try:
            while not algorithm.done:
                next(search_generator)
        except StopIteration:
            pass

        self.assertTrue(algorithm.done)


class TestAStarPathReconstruction(unittest.TestCase):
    def setUp(self):
        self.mock_pixel_map = Mock()
        self.mock_pixel_map.start = (0, 0)
        self.mock_pixel_map.end = (2, 0)

    def test_reconstruct_path(self):
        # Manual node chain
        node1 = AStarNode((0, 0), g_cost=0, h_cost=2, parent=None)
        node2 = AStarNode((1, 0), g_cost=1, h_cost=1, parent=node1)
        node3 = AStarNode((2, 0), g_cost=2, h_cost=0, parent=node2)

        self.mock_pixel_map.is_walkable = Mock(return_value=True)
        algorithm = AStar(self.mock_pixel_map)
        algorithm.current_node = node3

        path = list(algorithm.reconstruct_step())
        self.assertEqual(path, [(2, 0), (1, 0), (0, 0)])

    def test_reconstruct_path_single_node(self):
        node = AStarNode((0, 0), g_cost=0, h_cost=0, parent=None)

        self.mock_pixel_map.is_walkable = Mock(return_value=True)
        algorithm = AStar(self.mock_pixel_map)
        algorithm.current_node = node

        path = list(algorithm.reconstruct_step())
        self.assertEqual(path, [(0, 0)])


class TestAStarNeighborExploration(unittest.TestCase):
    def setUp(self):
        self.mock_pixel_map = Mock()
        self.mock_pixel_map.start = (5, 5)
        self.mock_pixel_map.end = (10, 10)

    def test_horizontal_neighbor_exploration(self):
        walkable_positions = {(5, 5), (6, 5), (4, 5)}

        def is_walkable(pos):
            return pos in walkable_positions

        self.mock_pixel_map.is_walkable = is_walkable
        algorithm = AStar(self.mock_pixel_map)

        search_generator = algorithm.search_step()
        positions_added, positions_closed = next(search_generator)

        # Should have explored horizontal neighbors
        self.assertIn((6, 5), positions_added)
        self.assertIn((4, 5), positions_added)

    def test_diagonal_cost_calculation(self):
        self.mock_pixel_map.is_walkable = Mock(return_value=True)
        algorithm = AStar(self.mock_pixel_map)

        search_generator = algorithm.search_step()
        next(search_generator)

        # Check that diagonal g_scores are approximately sqrt(2)
        for pos, g_cost in algorithm.g_scores.items():
            if pos != (5, 5):  # Skip start position
                # Diagonal movement should cost sqrt(2)
                dx = abs(pos[0] - 5)
                dy = abs(pos[1] - 5)
                if dx == 1 and dy == 1:
                    self.assertAlmostEqual(g_cost, math.sqrt(2), places=5)

    def test_orthogonal_cost_calculation(self):
        self.mock_pixel_map.is_walkable = Mock(return_value=True)
        algorithm = AStar(self.mock_pixel_map)

        search_generator = algorithm.search_step()
        next(search_generator)

        # Check that orthogonal g_scores are 1
        for pos, g_cost in algorithm.g_scores.items():
            if pos != (5, 5):  # Skip start position
                # Orthogonal movement should cost 1
                dx = abs(pos[0] - 5)
                dy = abs(pos[1] - 5)
                if (dx == 1 and dy == 0) or (dx == 0 and dy == 1):
                    self.assertAlmostEqual(g_cost, 1, places=5)


class TestAStarEdgeCases(unittest.TestCase):
    def test_start_equals_end(self):
        mock_pixel_map = Mock()
        mock_pixel_map.start = (5, 5)
        mock_pixel_map.end = (5, 5)
        mock_pixel_map.is_walkable = Mock(return_value=True)

        algorithm = AStar(mock_pixel_map)
        search_generator = algorithm.search_step()
        try:
            while not algorithm.done:
                next(search_generator)
        except StopIteration:
            pass

        self.assertTrue(algorithm.done)

    def test_algorithm_with_no_walkable_neighbors(self):
        mock_pixel_map = Mock()
        mock_pixel_map.start = (5, 5)
        mock_pixel_map.end = (10, 10)

        def is_walkable(pos):
            return pos == (5, 5)  # Only start is walkable

        mock_pixel_map.is_walkable = is_walkable
        algorithm = AStar(mock_pixel_map)

        search_generator = algorithm.search_step()
        try:
            next(search_generator)
        except StopIteration:
            pass

        # Only start should be in closed set
        self.assertIn((5, 5), algorithm.closed_set)
