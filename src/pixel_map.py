from PIL import Image


class PixelMap:
    def __init__(self, image_path, start, end):
        self.image = Image.open(image_path)
        self.start = start
        self.end = end

    def get_neighbors(self, position):
        x, y = position
        neighbors = []
        for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            nx, ny = x + dx, y + dy
            if (
                0 <= nx < self.image.width
                and 0 <= ny < self.image.height
                and self.image.getpixel((nx, ny)) == (255, 255, 255)
            ):
                neighbors.append((nx, ny))
        return neighbors
