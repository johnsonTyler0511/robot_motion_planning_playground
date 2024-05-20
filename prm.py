from typing import List, Tuple
from utils import *

def is_collision(node1: Node, node2: Node, obstacles: List[Tuple[float, float, float, float]]) -> bool:
    for obstacle in obstacles:
        x1, y1, x2, y2 = obstacle
        if (x1 <= node1.x <= x2 or x1 <= node2.x <= x2) and (y1 <= node1.y <= y2 or y1 <= node2.y <= y2):
            return True
        # Check if the line passing through node1 and node2 intersects with the obstacle
        if line_intersects_obstacle(node1, node2, obstacle):
            return True
    return False

def line_intersects_obstacle(node1: Node, node2: Node, obstacle: Tuple[float, float, float, float]) -> bool:
    x1, y1, x2, y2 = obstacle
    # Check if the line intersects with any of the four sides of the obstacle
    if line_intersects_segment(node1.x, node1.y, node2.x, node2.y, x1, y1, x2, y1):
        return True
    if line_intersects_segment(node1.x, node1.y, node2.x, node2.y, x2, y1, x2, y2):
        return True
    if line_intersects_segment(node1.x, node1.y, node2.x, node2.y, x2, y2, x1, y2):
        return True
    if line_intersects_segment(node1.x, node1.y, node2.x, node2.y, x1, y2, x1, y1):
        return True
    return False

def line_intersects_segment(x1: float, y1: float, x2: float, y2: float, x3: float, y3: float, x4: float, y4: float) -> bool:
    """
    Check if a line segment intersects with another line segment.

    Args:
        x1 (float): The x-coordinate of the first point of the first line segment.
        y1 (float): The y-coordinate of the first point of the first line segment.
        x2 (float): The x-coordinate of the second point of the first line segment.
        y2 (float): The y-coordinate of the second point of the first line segment.
        x3 (float): The x-coordinate of the first point of the second line segment.
        y3 (float): The y-coordinate of the first point of the second line segment.
        x4 (float): The x-coordinate of the second point of the second line segment.
        y4 (float): The y-coordinate of the second point of the second line segment.

    Returns:
        bool: True if the line segments intersect, False otherwise.
    """
    # Calculate the direction of the line segments
    d1 = (x4 - x3) * (y1 - y3) - (x1 - x3) * (y4 - y3)
    d2 = (x4 - x3) * (y2 - y3) - (x2 - x3) * (y4 - y3)
    d3 = (x2 - x1) * (y3 - y1) - (x3 - x1) * (y2 - y1)
    d4 = (x2 - x1) * (y4 - y1) - (x4 - x1) * (y2 - y1)
    # Check if the line segments intersect
    if (d1 * d2 < 0) and (d3 * d4 < 0):
        return True
    return False

def generate_prm(num_nodes: int, width: float, height: float, max_connections: int, obstacles: List[Tuple[float, float, float, float]]) -> List[Node]:
    nodes: List[Node] = []
    for _ in range(num_nodes):
        node = generate_random_node(width, height)
        nodes.append(node)

    for i in range(num_nodes):
        distances = []
        for j in range(num_nodes):
            if i != j:
                distances.append((distance(nodes[i], nodes[j]), j))
        distances.sort()
        for k in range(min(max_connections, len(distances))):
            if not is_collision(nodes[i], nodes[distances[k][1]], obstacles) \
                and len(nodes[i].neighbors) < max_connections \
                and len(nodes[distances[k][1]].neighbors) < max_connections:
                    nodes[i].neighbors.append(nodes[distances[k][1]])
                    nodes[distances[k][1]].neighbors.append(nodes[i])

    nodes = [node for node in nodes if node.neighbors]

    return nodes