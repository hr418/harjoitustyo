import timeit


class PathfindingAlgorithm:
    """
    Base class for pathfinding algorithms. This class is inherited by algorithm implementations.

    Attributes:
        pixel_map (PixelMap): The pixel map on which the algorithm operates.
    """

    def __init__(self, pixel_map):
        self.pixel_map = pixel_map
        self.done = False
        self.closed_count = 0
        self.open_count = 0
        self.path_length = 0

    def search_step(self):
        """
        Performs a single step of the pathfinding algorithm.

        Returns (tuple): A tuple containing a list of (x, y) positions that were added to the open set and a list of (x, y) positions that were added to the closed set.
        """
        raise NotImplementedError("This method should be implemented by subclasses")

    def reconstruct_step(self):
        """
        Reconstructs the path from the start to the end node.

        Returns (tuple or None): A tuple containing the (x, y) position of the current node in the path reconstruction process, or None if the path has been fully reconstructed.
        """
        raise NotImplementedError("This method should be implemented by subclasses")

    def measure_performance(self):
        """
        Measures the algorithm performance.

        Returns (float): The best time.
        """
        pixel_map = self.pixel_map
        AlgorithmClass = self.__class__

        def run_one_search():
            algo = AlgorithmClass(pixel_map)

            for _ in algo.search_step():
                pass

        times = timeit.repeat(run_one_search, number=10, repeat=10)

        return min(times)
