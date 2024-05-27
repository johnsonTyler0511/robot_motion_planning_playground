import pygame
from typing import List
from prm import *
from draw_functions import *
from path_functions import *
from utils import *


class Robot:
    def __init__(self, x: float, y: float, heading: float, wheel_radius: float, wheel_distance: float, width: float, length: float):
        self.x = x
        self.y = y
        self.heading = heading
        self.wheel_radius = wheel_radius
        self.wheel_distance = wheel_distance
        self.width = width
        self.length = length

    def move_forward(self, v_l: float, v_r: float):
        # Calculate the linear and angular velocities of the robot
        v = (v_l + v_r) / 2
        w = (v_r - v_l) / self.wheel_distance

        # Update the robot's position and heading using differential drive kinematics
        self.x += v * math.cos(math.radians(self.heading))
        self.y += v * math.sin(math.radians(self.heading))
        self.heading += math.degrees(w)

    def get_state(self):
        return self.x, self.y, self.heading

    def rotate(self, angle: float):
        self.heading += angle

    def draw(self, screen: pygame.Surface):
        # Create the arrow surface
        arrow_surface = pygame.Surface((self.width, self.length), pygame.SRCALPHA)
        pygame.draw.polygon(arrow_surface, RED, [(0, 0), (self.width, self.length // 2), (0, self.length)])

        # Rotate the arrow
        rotated_arrow = pygame.transform.rotate(arrow_surface, self.heading)
        rotated_rect = rotated_arrow.get_rect(center=(self.x, self.y))

        # Draw the rotated arrow
        screen.blit(rotated_arrow, rotated_rect)

def calculate_target_point(robot: Robot, lookahead_distance: float, next_node: Node) -> Node:
                # Calculate the distance between the robot and the next node
                distance_to_next_node = distance(Node(robot.x, robot.y), next_node)
                # If the distance is less than the lookahead distance, return the next node
                if distance_to_next_node <= lookahead_distance:
                    return next_node
                # Calculate the ratio of the lookahead distance to the distance between the robot and the next node
                ratio = lookahead_distance / distance_to_next_node
                # Calculate the x and y coordinates of the target point
                target_x = robot.x + ratio * (next_node.x - robot.x)
                target_y = robot.y + ratio * (next_node.y - robot.y)
                # Return the target point as a Node object
                return Node(target_x, target_y)

def calculate_desired_heading(robot: Robot, target_point: Node) -> float:
    # Calculate the angle between the robot's current position and the target point
    dx = target_point.x - robot.x
    dy = target_point.y - robot.y
    desired_heading = math.degrees(math.atan2(dy, dx))
    return desired_heading

def calculate_steering_angle(robot: Robot, desired_heading: float) -> float:
    # Calculate the difference between the desired heading and the robot's current heading
    angle_difference = desired_heading - robot.heading
    # Return the steering angle
    return angle_difference
        
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

    # Create an instance of the Robot class
    wheel_radius = 10.0  # Replace with the actual wheel radius
    wheel_distance = 20.0  # Replace with the actual distance between wheels
    width = 20.0  # Replace with the actual width of the robot body
    length = 35.0  # Replace with the actual length of the robot body
    robot = Robot(start.x, start.y, 0, wheel_radius, wheel_distance, width, length)

    # Game loop
    path_index = 0
    prev_path_index = -1
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

        # Move the robot along the path
        if path_index < len(path):
            next_node = bazier_smooth_path[path_index]

            # Calculate the lookahead distance
            lookahead_distance = 10.0  # Replace with your desired lookahead distance

            # Calculate the target point
            target_point = calculate_target_point(robot, lookahead_distance, next_node)

            # Calculate the desired heading angle
            desired_heading = calculate_desired_heading(robot, target_point)

            # Calculate the steering angle
            steering_angle = calculate_steering_angle(robot, desired_heading)

            # Rotate the robot
            robot.rotate(steering_angle)

            # Move the robot forward
            robot.move_forward(0.1, 0.1)

            # Check if the robot has reached the target point
            if distance(Node(robot.x, robot.y), target_point) < 5:
                path_index += 1

        robot.draw(screen)

        # Update the screen
        pygame.display.flip()

    # Quit Pygame
    pygame.quit()

# Run the main function
if __name__ == "__main__":
    main()
