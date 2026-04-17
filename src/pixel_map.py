from PIL import Image


class PixelMap:
    def __init__(self, image_path, start, end):
        self.image = Image.open(image_path)
        self.start = start
        self.end = end
        self.width, self.height = self.image.size

    def is_walkable(self, position):
        x, y = position
        return (
            0 <= x < self.image.width
            and 0 <= y < self.image.height
            and self.image.getpixel((x, y)) == (255, 255, 255)
        )
