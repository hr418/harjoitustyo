import heapq
from src.algorithms.base import PathfindingAlgorithm


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
    """

    def __init__(self, pixel_map):
        super().__init__(pixel_map)
        self.open_set = heapq.heapify(
            [
                AStarNode(
                    pixel_map.start,
                    g_cost=0,
                    h_cost=self.heuristic(pixel_map.start),
                )
            ]
        )
        self.current_node = None

    def heuristic(self, node):
        """
        Heuristic function for A* algorithm. Uses Manhattan distance.

        Args:
            node (tuple): The (x, y) position of the current node.

        Returns (int): The heuristic cost from the node to the goal.
        """
        return abs(node[0] - self.pixel_map.end[0]) + abs(
            node[1] - self.pixel_map.end[1]
        )

    def search_step(self):
        if not self.open_set:
            return None

        self.current_node = heapq.heappop(self.open_set)

        if self.current_node.position == self.pixel_map.end:
            return self.current_node.position

        for neighbor in self.pixel_map.get_neighbors(self.current_node.position):
            g_cost = self.current_node.g_cost + 1
            h_cost = self.heuristic(neighbor)
            neighbor_node = AStarNode(
                neighbor, g_cost=g_cost, h_cost=h_cost, parent=self.current_node
            )
            heapq.heappush(self.open_set, neighbor_node)

        return None

    def reconstruct_step(self):
        if not self.current_node:
            return None

        current_coord = self.current_node.position
        self.current_node = self.current_node.parent

        return current_coord
