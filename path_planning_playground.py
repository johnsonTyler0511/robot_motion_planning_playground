import pygame
from typing import List
from prm import *
from draw_functions import *
from path_functions import *
from utils import *

def main() -> None:

    # Initialize Pygame
    pygame.init()

    # Set the width and height of the screen
    screen_width: int = 800
    screen_height: int = 600
    screen: pygame.Surface = pygame.display.set_mode((screen_width, screen_height))
    pygame.display.set_caption("PRM Visualization")

    # Generate PRM nodes
    num_nodes: int = 300
    width: float = 800
    height: float = 600
    max_connections: int = 8

    # Generate random obstacles
    num_obstacles = 10
    max_obs_size = 150
    obstacles = generate_random_obstacles(num_obstacles, width, height, max_obs_size)

    nodes: List[Node] = generate_prm(num_nodes, width, height, max_connections, obstacles)

    start = closest_node(nodes, 50,50)
    end = closest_node(nodes, 750, 550)

    path = dijkstra(start, end, nodes)
    bspline_smooth_path = bspline_smoothing(path, len(path), 100)
    bazier_smooth_path = bezier_smoothing(path, len(path), 100)

    if (len(path) == 0):
        print(f"No path found from [{start.x},{start.y}] to [{end.x},{end.y}]")

    # Game loop
    running: bool = True
    while running:
        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Clear the screen
        screen.fill(DARK_GRAY)

        # Draw obstacles
        draw_obstacles(screen, obstacles)
        # Draw nodes and connections
        draw_nodes(screen, nodes)
        # Draw path
        draw_path(screen, path, ORANGE)
        # Draw smooth path
        draw_path(screen, bspline_smooth_path, PURPLE)
        draw_path(screen, bazier_smooth_path, YELLOW)

        # Update the screen
        pygame.display.flip()

    # Quit Pygame
    pygame.quit()

# Run the main function
if __name__ == "__main__":
    main()
