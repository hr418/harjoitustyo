import heapq
from algorithms.base import PathfindingAlgorithm


class AStarNode:
    """
    Node class for A* algorithm.

    Attributes:
        position (tuple): The (x, y) position of the node.
        g_cost (int): The cost from the start node to this node.
        h_cost (int): The heuristic cost from this node to the goal node.
        f_cost (int): The total cost (g_cost + h_cost).
        parent (AStarNode): The parent node in the path.
    """

    def __init__(self, position, g_cost=0, h_cost=0, parent=None):
        self.position = position
        self.g_cost = g_cost
        self.h_cost = h_cost
        self.parent = parent

    @property
    def f_cost(self):
        return self.g_cost + self.h_cost

    def __lt__(self, other):
        # Need to compare nodes based on f_cost for the priority queue
        return self.f_cost < other.f_cost


class AStar(PathfindingAlgorithm):
    """
    A* pathfinding algorithm implementation.

    Attributes:
        open_set (list): A priority queue of nodes to be evaluated.
        current_node (AStarNode): The current node being evaluated.
        closed_set (set): A set of positions that have been evaluated.
        g_scores (dict): A dictionary mapping positions to their current best g_costs.
    """

    def __init__(self, pixel_map):
        super().__init__(pixel_map)
        self.open_set = [
            AStarNode(
                pixel_map.start,
                g_cost=0,
                h_cost=self._heuristic(pixel_map.start),
            )
        ]
        heapq.heapify(self.open_set)
        self.current_node = None
        self.closed_set = set()
        self.g_scores = {pixel_map.start: 0}

    def _heuristic(self, node):
        """
        Heuristic function for A* algorithm. Uses chebyshev distance.

        Args:
            node (tuple): The (x, y) position of the current node.

        Returns (int): The heuristic cost from the node to the goal.
        """
        return max(
            abs(node[0] - self.pixel_map.end[0]), abs(node[1] - self.pixel_map.end[1])
        )

    def search_step(self):
        while self.open_set:
            positions_added_to_closed = []
            positions_added_to_open = []

            self.current_node = heapq.heappop(self.open_set)

            if self.current_node.position in self.closed_set:
                continue

            self.closed_set.add(self.current_node.position)
            positions_added_to_closed.append(self.current_node.position)

            if self.current_node.position == self.pixel_map.end:
                self.done = True
                raise StopIteration

            neighbors = []

            for dx, dy in [
                (-1, -1),
                (-1, 0),
                (-1, 1),
                (0, -1),
                (0, 1),
                (1, -1),
                (1, 0),
                (1, 1),
            ]:
                neighbor_pos = (
                    self.current_node.position[0] + dx,
                    self.current_node.position[1] + dy,
                )
                if self.pixel_map.is_walkable(neighbor_pos):
                    neighbors.append(neighbor_pos)

            for neighbor in neighbors:
                g_cost = self.current_node.g_cost + 1

                if g_cost >= self.g_scores.get(neighbor, float("inf")):
                    continue

                self.g_scores[neighbor] = g_cost
                h_cost = self._heuristic(neighbor)
                neighbor_node = AStarNode(
                    neighbor, g_cost=g_cost, h_cost=h_cost, parent=self.current_node
                )
                heapq.heappush(self.open_set, neighbor_node)
                positions_added_to_open.append(neighbor)

            yield (positions_added_to_open, positions_added_to_closed)

    def reconstruct_step(self):
        while self.current_node:
            current_coord = self.current_node.position
            self.current_node = self.current_node.parent
            yield current_coord
