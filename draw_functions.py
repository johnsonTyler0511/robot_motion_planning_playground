import pygame
from typing import List, Tuple
from prm import Node

# Define colors
BLACK = (0, 0, 0)
DARK_GRAY = (50, 50, 50)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
ORANGE = (255, 165, 0)
PURPLE = (128, 0, 128)
YELLOW = (255, 255, 0)

def draw_nodes(screen: pygame.Surface, nodes: List[Node]) -> None:
    for node in nodes:
        color = BLUE
        if (len(node.neighbors) == 0):
            color = RED
        pygame.draw.circle(screen, color, (int(node.x), int(node.y)), 3)
        for neighbor in node.neighbors:
            pygame.draw.line(screen, WHITE, (int(node.x), int(node.y)), (int(neighbor.x), int(neighbor.y)))

def draw_obstacles(screen: pygame.Surface, obstacles: List[Tuple[float, float, float, float]]) -> None:
    for obstacle in obstacles:
        x1, y1, x2, y2 = obstacle
        pygame.draw.rect(screen, (0, 255, 0), (x1, y1, x2 - x1, y2 - y1))

def draw_path(screen: pygame.Surface, path: List[Node], color: Tuple[int, int, int]) -> None:
    for i in range(len(path) - 1):
        pygame.draw.line(screen, color, (int(path[i].x), int(path[i].y)), (int(path[i+1].x), int(path[i+1].y)), 3)