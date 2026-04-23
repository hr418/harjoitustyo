import pygame
from pixel_map import PixelMap
from algorithms.a_star import AStar
from algorithms.jump_point_search import JumpPointSearch

# This file is very much a work in progress, much of it is temporary to have some visualisation of the algorithms


def draw_map(screen, positions, path, offset_x):
    for x in range(pixel_map.width):
        for y in range(pixel_map.height):
            if pixel_map.is_walkable((x, y)):
                color = (255, 255, 255)
            else:
                color = (0, 0, 0)

            pygame.draw.rect(
                screen,
                color,
                (offset_x + x * PIXEL_SCALE, y * PIXEL_SCALE, PIXEL_SCALE, PIXEL_SCALE),
            )

    # Draw open set
    for position, status in positions.items():
        if status == "open":
            pygame.draw.rect(
                screen,
                (0, 255, 0),
                (
                    offset_x + position[0] * PIXEL_SCALE,
                    position[1] * PIXEL_SCALE,
                    PIXEL_SCALE,
                    PIXEL_SCALE,
                ),
            )

    # Draw closed set
    for position, status in positions.items():
        if status == "closed":
            pygame.draw.rect(
                screen,
                (0, 0, 255),
                (
                    offset_x + position[0] * PIXEL_SCALE,
                    position[1] * PIXEL_SCALE,
                    PIXEL_SCALE,
                    PIXEL_SCALE,
                ),
            )

    # Draw the path
    if path and len(path) > 1:
        pygame.draw.lines(
            screen,
            (255, 0, 0),
            False,
            [
                (
                    offset_x + pos[0] * PIXEL_SCALE + PIXEL_SCALE // 2,
                    pos[1] * PIXEL_SCALE + PIXEL_SCALE // 2,
                )
                for pos in path
            ],
            3,
        )

    # Draw start and end points
    pygame.draw.rect(
        screen,
        (255, 255, 0),
        (
            offset_x + pixel_map.start[0] * PIXEL_SCALE,
            pixel_map.start[1] * PIXEL_SCALE,
            PIXEL_SCALE,
            PIXEL_SCALE,
        ),
    )
    pygame.draw.rect(
        screen,
        (255, 0, 255),
        (
            offset_x + pixel_map.end[0] * PIXEL_SCALE,
            pixel_map.end[1] * PIXEL_SCALE,
            PIXEL_SCALE,
            PIXEL_SCALE,
        ),
    )


pixel_map = PixelMap("maps/AR0012SR.png", (8, 69), (133, 91))
PIXEL_SCALE = 8

a_star = AStar(pixel_map)
jump_point_search = JumpPointSearch(pixel_map)

a_star_positions = {}
a_star_path = []
a_star_done = False
jump_point_search_positions = {}
jump_point_search_path = []
jump_point_search_done = False

# Initialize Pygame
pygame.init()

# Set up the app window
screen = pygame.display.set_mode(
    ((pixel_map.width * 2 + 1) * PIXEL_SCALE, pixel_map.height * PIXEL_SCALE)
)
pygame.display.set_caption("Pathfinding Visualization")

# App loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    if not a_star_done:
        try:
            opn, cls = next(a_star.search_step())
            a_star_positions.update(
                {pos: "open" for pos in opn if a_star_positions.get(pos) != "closed"}
            )
            a_star_positions.update({pos: "closed" for pos in cls})
        except StopIteration:
            a_star_done = True
    else:
        try:
            pos = next(a_star.reconstruct_step())
            a_star_path.append(pos)
        except StopIteration:
            pass

    if not jump_point_search_done:
        try:
            opn, cls = next(jump_point_search.search_step())
            jump_point_search_positions.update(
                {
                    pos: "open"
                    for pos in opn
                    if jump_point_search_positions.get(pos) != "closed"
                }
            )
            jump_point_search_positions.update({pos: "closed" for pos in cls})
        except StopIteration:
            jump_point_search_done = True
    else:
        try:
            pos = next(jump_point_search.reconstruct_step())
            jump_point_search_path.append(pos)
        except StopIteration:
            pass

    # Fill the screen white
    screen.fill((255, 255, 255))

    # Draw the pixel maps
    draw_map(screen, a_star_positions, a_star_path, 0)
    draw_map(
        screen,
        jump_point_search_positions,
        jump_point_search_path,
        pixel_map.width * PIXEL_SCALE + PIXEL_SCALE,
    )

    # Update the display
    pygame.display.flip()


# Quit Pygame
pygame.quit()
