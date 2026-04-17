import pygame
from pixel_map import PixelMap
from algorithms.a_star import AStar
from algorithms.jump_point_search import JumpPointSearch

pixel_map = PixelMap("maps/AR0012SR.png", (8, 69), (133, 91))

# Initialize Pygame
pygame.init()

# Set up the game window
screen = pygame.display.set_mode((1024, 512))
pygame.display.set_caption("Hello Pygame")

# App loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Fill the screen white
    screen.fill((255, 255, 255))

    # Draw a 2px wide black line down the middle
    pygame.draw.line(screen, (0, 0, 0), (512, 0), (512, 512), 2)

    # Update the display
    pygame.display.flip()

# Quit Pygame
pygame.quit()
