from typing import List
from utils import Node, distance
import heapq

def dijkstra(start_node: Node, end_node: Node, nodes: List[Node]) -> List[Node]:
    # Initialize distances and previous nodes
    distances = {node: float('inf') for node in nodes}
    distances[start_node] = 0
    previous = {node: None for node in nodes}

    # Create a priority queue to store nodes with their distances
    queue = [(0, start_node)]
    finished = False

    while queue:
        # Get the node with the smallest distance from the queue
        current_distance, current_node = heapq.heappop(queue)

        # If the current node is the end node, we have found the shortest path
        if current_node == end_node:
            finished = True
            break

        # Check the neighbors of the current node
        for neighbor in current_node.neighbors:
            # Calculate the distance from the start node to the neighbor
            next_distance = current_distance + distance(current_node, neighbor)

            # If the new distance is smaller than the current distance, update it
            if next_distance < distances[neighbor]:
                distances[neighbor] = next_distance
                previous[neighbor] = current_node

                # Add the neighbor to the queue with its new distance
                heapq.heappush(queue, (next_distance, neighbor))

    if finished:
        # Reconstruct the shortest path from the end node to the start node
        path = []
        current = end_node
        while current:
            path.append(current)
            current = previous[current]
        path.reverse()
        return path

    return []

def bspline_smoothing(path: List[Node], control_points: int, iterations: int) -> List[Node]:
    if (path == None or len(path) == 0):
        return []

    # Create a list of control points
    control_path = path[:control_points]
    
    # Perform B-spline smoothing iterations
    for _ in range(iterations):
        new_path = [path[0]]
        
        # Update the intermediate points using B-spline interpolation
        for i in range(1, len(path) - 1):
            prev_control = control_path[(i - 1) % control_points]
            curr_control = control_path[i % control_points]
            next_control = control_path[(i + 1) % control_points]
            
            new_point = Node(
                (prev_control.x + 4 * curr_control.x + next_control.x) / 6,
                (prev_control.y + 4 * curr_control.y + next_control.y) / 6
            )
            
            new_path.append(new_point)
        
        new_path.append(path[-1])
        path = new_path
    
    return path

def bezier_smoothing(path: List[Node], control_points: int, iterations: int) -> List[Node]:
    if (path == None or len(path) == 0):
        return []

    # Create a list of control points
    control_path = path[:control_points]
    
    # Perform Bezier curve smoothing iterations
    for _ in range(iterations):
        new_path = [path[0]]
        
        # Update the intermediate points using Bezier curve interpolation
        for i in range(1, len(path) - 1):
            t = 1 / (control_points - 1)
            t1 = i * t
            t2 = (i + 1) * t
            
            prev_control = control_path[i - 1]
            curr_control = control_path[i]
            next_control = control_path[i + 1]
            
            new_point = Node(
                (1 - t2) ** 2 * prev_control.x + 2 * (1 - t2) * t2 * curr_control.x + t2 ** 2 * next_control.x,
                (1 - t2) ** 2 * prev_control.y + 2 * (1 - t2) * t2 * curr_control.y + t2 ** 2 * next_control.y
            )
            
            new_path.append(new_point)
        
        new_path.append(path[-1])
        path = new_path
        
        return path