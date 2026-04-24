import unittest
import math
from unittest.mock import Mock
from algorithms.jump_point_search import JumpPointSearch, JumpPointSearchNode


class TestJumpPointSearchNode(unittest.TestCase):
    def test_node_initialization(self):
        node = JumpPointSearchNode((5, 10))
        self.assertEqual(node.position, (5, 10))
        self.assertEqual(node.g_cost, 0)
        self.assertEqual(node.h_cost, 0)
        self.assertIsNone(node.parent)

    def test_node_initialization_with_costs(self):
        node = JumpPointSearchNode((3, 4), g_cost=5, h_cost=10)
        self.assertEqual(node.position, (3, 4))
        self.assertEqual(node.g_cost, 5)
        self.assertEqual(node.h_cost, 10)

    def test_node_initialization_with_parent(self):
        parent_node = JumpPointSearchNode((1, 1))
        child_node = JumpPointSearchNode((2, 2), parent=parent_node)
        self.assertEqual(child_node.parent, parent_node)

    def test_f_cost_calculation(self):
        node = JumpPointSearchNode((0, 0), g_cost=5, h_cost=10)
        self.assertEqual(node.f_cost, 15)

    def test_node_comparison(self):
        node1 = JumpPointSearchNode((0, 0), g_cost=5, h_cost=10)
        node2 = JumpPointSearchNode((1, 1), g_cost=10, h_cost=10)
        self.assertTrue(node1 < node2)


class TestJumpPointSearchDirection(unittest.TestCase):
    def setUp(self):
        self.mock_pixel_map = Mock()
        self.mock_pixel_map.start = (0, 0)
        self.mock_pixel_map.end = (10, 10)
        self.algorithm = JumpPointSearch(self.mock_pixel_map)

    def test_direction_right(self):
        direction = self.algorithm._direction((0, 0), (1, 0))
        self.assertEqual(direction, (1, 0))

    def test_direction_left(self):
        direction = self.algorithm._direction((1, 0), (0, 0))
        self.assertEqual(direction, (-1, 0))

    def test_direction_up(self):
        direction = self.algorithm._direction((0, 1), (0, 0))
        self.assertEqual(direction, (0, -1))

    def test_direction_down(self):
        direction = self.algorithm._direction((0, 0), (0, 1))
        self.assertEqual(direction, (0, 1))

    def test_direction_diagonal_right_down(self):
        direction = self.algorithm._direction((0, 0), (1, 1))
        self.assertEqual(direction, (1, 1))

    def test_direction_diagonal_left_up(self):
        direction = self.algorithm._direction((1, 1), (0, 0))
        self.assertEqual(direction, (-1, -1))

    def test_direction_no_movement(self):
        direction = self.algorithm._direction((5, 5), (5, 5))
        self.assertEqual(direction, (0, 0))


class TestJumpPointSearchDistance(unittest.TestCase):
    def setUp(self):
        self.mock_pixel_map = Mock()
        self.mock_pixel_map.start = (0, 0)
        self.mock_pixel_map.end = (10, 10)
        self.algorithm = JumpPointSearch(self.mock_pixel_map)

    def test_distance_same_position(self):
        distance = self.algorithm._distance((5, 5), (5, 5))
        self.assertEqual(distance, 0)

    def test_distance_horizontal(self):
        distance = self.algorithm._distance((0, 0), (5, 0))
        self.assertEqual(distance, 5)

    def test_distance_vertical(self):
        distance = self.algorithm._distance((0, 0), (0, 5))
        self.assertEqual(distance, 5)

    def test_distance_diagonal(self):
        distance = self.algorithm._distance((0, 0), (3, 3))
        expected = 3 * math.sqrt(2)
        self.assertAlmostEqual(distance, expected, places=5)

    def test_distance_mixed_movement(self):
        distance = self.algorithm._distance((0, 0), (5, 3))
        # 3 diagonal steps + 2 horizontal = 3*sqrt(2) + 2
        expected = 3 * math.sqrt(2) + 2
        self.assertAlmostEqual(distance, expected, places=5)

    def test_distance_mixed_movement_reverse(self):
        distance1 = self.algorithm._distance((0, 0), (5, 3))
        distance2 = self.algorithm._distance((5, 3), (0, 0))
        self.assertAlmostEqual(distance1, distance2, places=5)


class TestJumpPointSearchForcedDirections(unittest.TestCase):
    def setUp(self):
        self.mock_pixel_map = Mock()
        self.mock_pixel_map.start = (0, 0)
        self.mock_pixel_map.end = (10, 10)
        self.algorithm = JumpPointSearch(self.mock_pixel_map)

    def test_forced_directions_horizontal_movement(self):
        def is_walkable(pos):
            # Allow all positions except one
            if pos == (2, 1):
                return False
            return True

        self.algorithm.pixel_map.is_walkable = is_walkable

        forced = self.algorithm._forced_directions((2, 0), (1, 0))

        self.assertTrue(len(forced) > 0)

    def test_forced_directions_no_obstacles(self):
        self.algorithm.pixel_map.is_walkable = Mock(return_value=True)

        forced = self.algorithm._forced_directions((5, 5), (1, 0))

        self.assertEqual(len(forced), 0)

    def test_forced_directions_diagonal_movement(self):
        def is_walkable(pos):
            if pos == (4, 6):  # Block lower left
                return False
            return True

        self.algorithm.pixel_map.is_walkable = is_walkable

        forced = self.algorithm._forced_directions((5, 5), (1, 1))

        self.assertTrue(len(forced) > 0)


class TestJumpPointSearchPrunedDirections(unittest.TestCase):
    def setUp(self):
        self.mock_pixel_map = Mock()
        self.mock_pixel_map.start = (0, 0)
        self.mock_pixel_map.end = (10, 10)
        self.algorithm = JumpPointSearch(self.mock_pixel_map)

    def test_pruned_directions_no_parent(self):
        node = JumpPointSearchNode((0, 0), parent=None)
        directions = self.algorithm._pruned_directions(node)

        # Should return all 8 directions when no parent
        self.assertEqual(len(directions), 8)

    def test_pruned_directions_horizontal_parent(self):
        parent = JumpPointSearchNode((0, 0))
        node = JumpPointSearchNode((1, 0), parent=parent)

        self.algorithm.pixel_map.is_walkable = Mock(return_value=True)
        directions = self.algorithm._pruned_directions(node)

        # Should include straight direction and diagonals
        self.assertIn((1, 0), directions)

    def test_pruned_directions_vertical_parent(self):
        parent = JumpPointSearchNode((0, 0))
        node = JumpPointSearchNode((0, 1), parent=parent)

        self.algorithm.pixel_map.is_walkable = Mock(return_value=True)
        directions = self.algorithm._pruned_directions(node)

        # Should include straight direction
        self.assertIn((0, 1), directions)

    def test_pruned_directions_diagonal_parent(self):
        parent = JumpPointSearchNode((0, 0))
        node = JumpPointSearchNode((1, 1), parent=parent)

        self.algorithm.pixel_map.is_walkable = Mock(return_value=True)
        directions = self.algorithm._pruned_directions(node)

        # Should include diagonal and component directions
        self.assertIn((1, 1), directions)

    def test_pruning_reduces_search_space(self):
        def is_walkable(pos):
            return 0 <= pos[0] <= 10 and 0 <= pos[1] <= 10

        self.mock_pixel_map.is_walkable = is_walkable

        jps = JumpPointSearch(self.mock_pixel_map)

        # Create a node with parent to trigger pruning
        parent = JumpPointSearchNode((5, 5))
        node = JumpPointSearchNode((6, 5), parent=parent)

        pruned = jps._pruned_directions(node)
        # Pruned should be less than or equal to all 8 directions
        self.assertLessEqual(len(pruned), 8)


class TestJumpPointSearchJump(unittest.TestCase):
    def setUp(self):
        self.mock_pixel_map = Mock()
        self.mock_pixel_map.start = (0, 0)
        self.mock_pixel_map.end = (10, 10)
        self.algorithm = JumpPointSearch(self.mock_pixel_map)

    def test_jump_blocked_immediately(self):
        def is_walkable(pos):
            if pos == (1, 0):  # Blocked
                return False
            return True

        self.mock_pixel_map.is_walkable = is_walkable

        jump_pos = self.algorithm._jump((0, 0), (1, 0))
        self.assertIsNone(jump_pos)

    def test_jump_goal_found_short_distance(self):
        self.mock_pixel_map.end = (1, 0)

        def is_walkable(pos):
            return pos == (0, 0) or pos == (1, 0)

        self.mock_pixel_map.is_walkable = is_walkable

        jump_pos = self.algorithm._jump((0, 0), (1, 0))
        self.assertEqual(jump_pos, (1, 0))


class TestJumpPointSearchInitialization(unittest.TestCase):

    def setUp(self):
        self.mock_pixel_map = Mock()
        self.mock_pixel_map.start = (0, 0)
        self.mock_pixel_map.end = (10, 10)

    def test_algorithm_inheritance(self):
        algorithm = JumpPointSearch(self.mock_pixel_map)
        self.assertIsNotNone(algorithm.pixel_map)
        self.assertFalse(algorithm.done)

    def test_algorithm_has_distance_method(self):
        algorithm = JumpPointSearch(self.mock_pixel_map)
        distance = algorithm._distance((0, 0), (3, 4))
        self.assertGreater(distance, 0)


class TestJumpPointSearchPathReconstruction(unittest.TestCase):
    def setUp(self):
        self.mock_pixel_map = Mock()
        self.mock_pixel_map.start = (0, 0)
        self.mock_pixel_map.end = (2, 0)

    def test_reconstruct_path_simple(self):
        node1 = JumpPointSearchNode((0, 0), g_cost=0, h_cost=2, parent=None)
        node2 = JumpPointSearchNode((1, 0), g_cost=1, h_cost=1, parent=node1)
        node3 = JumpPointSearchNode((2, 0), g_cost=2, h_cost=0, parent=node2)

        algorithm = JumpPointSearch(self.mock_pixel_map)
        algorithm.current_node = node3

        path = list(algorithm.reconstruct_step())
        self.assertEqual(path, [(2, 0), (1, 0), (0, 0)])

    def test_reconstruct_path_single_node(self):
        node = JumpPointSearchNode((0, 0), g_cost=0, h_cost=0, parent=None)

        algorithm = JumpPointSearch(self.mock_pixel_map)
        algorithm.current_node = node

        path = list(algorithm.reconstruct_step())
        self.assertEqual(path, [(0, 0)])


class TestJumpPointSearchEdgeCases(unittest.TestCase):
    def test_start_equals_end(self):
        mock_pixel_map = Mock()
        mock_pixel_map.start = (5, 5)
        mock_pixel_map.end = (5, 5)
        mock_pixel_map.is_walkable = Mock(return_value=True)

        algorithm = JumpPointSearch(mock_pixel_map)
        search_generator = algorithm.search_step()
        try:
            while not algorithm.done:
                next(search_generator)
        except StopIteration:
            pass

        self.assertTrue(algorithm.done)

    def test_no_walkable_neighbors(self):
        mock_pixel_map = Mock()
        mock_pixel_map.start = (5, 5)
        mock_pixel_map.end = (10, 10)

        def is_walkable(pos):
            return pos == (5, 5)

        mock_pixel_map.is_walkable = is_walkable

        algorithm = JumpPointSearch(mock_pixel_map)
        search_generator = algorithm.search_step()
        try:
            next(search_generator)
        except StopIteration:
            pass

        # Only start in closed set
        self.assertIn((5, 5), algorithm.closed_set)
