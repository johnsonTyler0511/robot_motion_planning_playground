import random, math
from typing import List, Tuple

class Node:
    def __init__(self, x: float, y: float):
        self.x = x
        self.y = y
        self.neighbors: List[Node] = []

def generate_random_node(width: float, height: float) -> Node:
    x = random.uniform(0, width)
    y = random.uniform(0, height)
    return Node(x, y)

def generate_random_obstacles(num_obstacles: int, width: float, height: float, max_size: float) -> List[Tuple[float, float, float, float]]:
    obstacles = []
    for _ in range(num_obstacles):
        x1 = random.uniform(0, width - max_size)
        y1 = random.uniform(0, height - max_size)
        size = random.uniform(0, max_size)
        x2 = x1 + size
        y2 = y1 + size
        obstacles.append((x1, y1, x2, y2))
    return obstacles

def closest_node(nodes: List[Node], x: float, y: float) -> Node:
    closest = None
    min_distance = float('inf')
    for node in nodes:
        d = distance(node, Node(x, y))
        if d < min_distance:
            min_distance = d
            closest = node
    return closest

def distance(node1: Node, node2: Node) -> float:
    return math.sqrt((node1.x - node2.x)**2 + (node1.y - node2.y)**2)