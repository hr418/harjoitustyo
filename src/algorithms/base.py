class PathfindingAlgorithm:
    """
    Base class for pathfinding algorithms. This class is inherited by algorithm implementations.
    """

    def __init__(self, pixel_map):
        self.pixel_map = pixel_map

    def search_step(self):
        """
        Performs a single step of the pathfinding algorithm.
        """
        raise NotImplementedError("This method should be implemented by subclasses")

    def reconstruct_step(self):
        """
        Reconstructs the path from the start to the end node.
        """
        raise NotImplementedError("This method should be implemented by subclasses")
