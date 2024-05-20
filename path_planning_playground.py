import random
import math
import pygame
from typing import List
from prm import *

# Now you can use the generated nodes to implement your visualization with Pygame
# Define colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
ORANGE = (255, 165, 0)

# Initialize Pygame
pygame.init()

# Set the width and height of the screen
screen_width: int = 800
screen_height: int = 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("PRM Visualization")

def draw_nodes(nodes: List[Node]) -> None:
    for node in nodes:
        color = BLUE
        if (len(node.neighbors) == 0):
            color = RED
        pygame.draw.circle(screen, color, (int(node.x), int(node.y)), 3)
        for neighbor in node.neighbors:
            pygame.draw.line(screen, BLACK, (int(node.x), int(node.y)), (int(neighbor.x), int(neighbor.y)))

def draw_obstacles(obstacles: List[Tuple[float, float, float, float]]) -> None:
    for obstacle in obstacles:
        x1, y1, x2, y2 = obstacle
        pygame.draw.rect(screen, (0, 255, 0), (x1, y1, x2 - x1, y2 - y1))

def draw_path(path: List[Node]) -> None:
    for i in range(len(path) - 1):
        pygame.draw.line(screen, ORANGE, (int(path[i].x), int(path[i].y)), (int(path[i+1].x), int(path[i+1].y)), 3)

def main() -> None:
    # Generate PRM nodes
    num_nodes: int = 200
    width: float = 800
    height: float = 600
    max_connections: int = 8

    # Generate maze obstacles
    obstacles: List[Tuple[float, float, float, float]] = [
        (100, 100, 200, 200),
        (300, 300, 400, 400),
        (500, 100, 600, 200),
        (700, 300, 800, 400),
        (150, 250, 250, 350),
        (400, 100, 500, 200),
        (600, 300, 700, 400),
        (200, 400, 300, 500),
        (450, 250, 550, 350),
        (650, 100, 750, 200)
    ]

    nodes: List[Node] = generate_prm_max_connect(num_nodes, width, height, max_connections, obstacles)

    start = closest_node(nodes, 50,50)
    end = closest_node(nodes, 750, 550)

    path = dijkstra(start, end, nodes)

    # Game loop
    running: bool = True
    while running:
        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Clear the screen
        screen.fill(WHITE)

        # Draw obstacles
        draw_obstacles(obstacles)
        # Draw nodes and connections
        draw_nodes(nodes)
        # Draw path
        draw_path(path)

        # Update the screen
        pygame.display.flip()

    # Quit Pygame
    pygame.quit()

# Run the main function
if __name__ == "__main__":
    main()
