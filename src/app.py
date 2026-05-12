import json
from pathlib import Path
import pygame
from pixel_map import PixelMap
from algorithms.a_star import AStar
from algorithms.jump_point_search import JumpPointSearch


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
                (offset_x + x * pixel_scale, y * pixel_scale, pixel_scale, pixel_scale),
            )

    # Draw open set
    for position, status in positions.items():
        if status == "open":
            pygame.draw.rect(
                screen,
                (0, 255, 0),
                (
                    offset_x + position[0] * pixel_scale,
                    position[1] * pixel_scale,
                    pixel_scale,
                    pixel_scale,
                ),
            )

    # Draw closed set
    for position, status in positions.items():
        if status == "closed":
            pygame.draw.rect(
                screen,
                (0, 0, 255),
                (
                    offset_x + position[0] * pixel_scale,
                    position[1] * pixel_scale,
                    pixel_scale,
                    pixel_scale,
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
                    offset_x + pos[0] * pixel_scale + pixel_scale // 2,
                    pos[1] * pixel_scale + pixel_scale // 2,
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
            offset_x + pixel_map.start[0] * pixel_scale,
            pixel_map.start[1] * pixel_scale,
            pixel_scale,
            pixel_scale,
        ),
    )
    pygame.draw.rect(
        screen,
        (255, 0, 255),
        (
            offset_x + pixel_map.end[0] * pixel_scale,
            pixel_map.end[1] * pixel_scale,
            pixel_scale,
            pixel_scale,
        ),
    )


def print_algorithm_stats(name, algorithm):
    print(f"{name} path length:", algorithm.path_length)
    print(f"{name} nodes added to closed set:", algorithm.closed_count)
    print(f"{name} nodes added to open set:", algorithm.open_count)
    print(f"{name} time:", algorithm.time)
    print("\n")


CONFIG_PATH = "./config.json"

try:
    with open(CONFIG_PATH, "r", encoding="utf-8") as f:
        cfg = json.load(f)
except FileNotFoundError:
    raise FileNotFoundError(f"Configuration file not found at: {CONFIG_PATH}")

required_keys = ["pixel_map_path", "start", "end", "pixel_scale"]
missing = [k for k in required_keys if k not in cfg]
if missing:
    raise KeyError(f"Missing configuration keys: {', '.join(missing)}")

pixel_map_path = cfg["pixel_map_path"]
start = tuple(cfg["start"])
end = tuple(cfg["end"])
pixel_scale = cfg["pixel_scale"]

pixel_map = PixelMap(pixel_map_path, start, end)

a_star = AStar(pixel_map)
jump_point_search = JumpPointSearch(pixel_map)

print("\nMeasuring algorithm performance... The visualization will launch soon.\n")

a_star.measure_performance()
jump_point_search.measure_performance()

a_star_positions = {}
a_star_path = []
a_star_done = False
a_star_stats_printed = False
a_star_search_gen = a_star.search_step()
a_star_reconstruct_gen = None

jump_point_search_positions = {}
jump_point_search_path = []
jump_point_search_done = False
jump_point_search_stats_printed = False
jps_search_gen = jump_point_search.search_step()
jps_reconstruct_gen = None

# Initialize Pygame
pygame.init()

# Set up the app window
screen = pygame.display.set_mode(
    ((pixel_map.width * 2 + 1) * pixel_scale, pixel_map.height * pixel_scale)
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
            opn, cls = next(a_star_search_gen)
            a_star_positions.update(
                {pos: "open" for pos in opn if a_star_positions.get(pos) != "closed"}
            )
            a_star_positions.update({pos: "closed" for pos in cls})
        except StopIteration:
            a_star_done = True
            a_star_reconstruct_gen = a_star.reconstruct_step()
            if not a_star_stats_printed:
                print_algorithm_stats("A*", a_star)
                a_star_stats_printed = True
    else:
        try:
            pos = next(a_star_reconstruct_gen)
            a_star_path.append(pos)
        except StopIteration:
            pass

    if not jump_point_search_done:
        try:
            opn, cls = next(jps_search_gen)
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
            jps_reconstruct_gen = jump_point_search.reconstruct_step()
            if not jump_point_search_stats_printed:
                print_algorithm_stats("Jump Point Search", jump_point_search)
                jump_point_search_stats_printed = True
    else:
        try:
            pos = next(jps_reconstruct_gen)
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
        pixel_map.width * pixel_scale + pixel_scale,
    )

    # Update the display
    pygame.display.flip()


# Quit Pygame
pygame.quit()
