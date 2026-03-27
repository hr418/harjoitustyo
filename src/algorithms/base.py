class PathfindingAlgorithm:
    """
    Base class for pathfinding algorithms. This class is inherited by algorithm implementations.

    Attributes:
        pixel_map (PixelMap): The pixel map on which the algorithm operates.
    """

    def __init__(self, pixel_map):
        self.pixel_map = pixel_map

    def search_step(self):
        """
        Performs a single step of the pathfinding algorithm.

        Returns (tuple or None): A tuple containing the (x, y) position of the current node, or None if no path is found.
        """
        raise NotImplementedError("This method should be implemented by subclasses")

    def reconstruct_step(self):
        """
        Reconstructs the path from the start to the end node.

        Returns (tuple or None): A tuple containing the (x, y) position of the current node in the path reconstruction process, or None if the path has been fully reconstructed.
        """
        raise NotImplementedError("This method should be implemented by subclasses")
