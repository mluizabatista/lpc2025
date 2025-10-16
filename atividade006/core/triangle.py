import math
import pygame
from core.config import TRIANGLE_SIZE, ROTATION_SPEED, MOVEMENT_SPEED, BRAKE_MODE

def rotate_point(point, angle_degrees):
    angle_radians = math.radians(angle_degrees)
    x, y = point
    cos_theta = math.cos(angle_radians)
    sin_theta = math.sin(angle_radians)
    return (
        x * cos_theta - y * sin_theta,
        x * sin_theta + y * cos_theta,
    )

# Luiza: Triangle class (due to circular import)

class Triangle:
    
    def __init__(self, position, color, controls):
        self.position = [float(position[0]), float(position[1])]
        self.angle = 0.0
        self.color = color
        self.moving = False
        self.controls = controls

        self.local_points = [
            (0.0, -TRIANGLE_SIZE),
            (-TRIANGLE_SIZE / 2.0, TRIANGLE_SIZE / 2.0),
            (TRIANGLE_SIZE / 2.0, TRIANGLE_SIZE / 2.0),
        ]

    def get_transformed_points(self):
        transformed = []
        for point in self.local_points:
            rotated = rotate_point(point, self.angle)
            screen_point = (
                rotated[0] + self.position[0],
                rotated[1] + self.position[1],
            )
            transformed.append(screen_point)
        return transformed

    def rotate(self, direction):
        if direction == "left":
            self.angle = (self.angle - ROTATION_SPEED) % 360.0
        elif direction == "right":
            self.angle = (self.angle + ROTATION_SPEED) % 360.0

    def move(self, direction=None):
        angle_radians = math.radians(self.angle)
        dx = math.sin(angle_radians) * MOVEMENT_SPEED
        dy = -math.cos(angle_radians) * MOVEMENT_SPEED

        if BRAKE_MODE == 0:
            if direction == "forward":
                self.moving = True
            elif direction == "stop":
                self.moving = False

            if self.moving:
                self.position[0] += dx
                self.position[1] += dy
        else:
            if direction == "forward":
                self.position[0] += dx
                self.position[1] += dy

    def draw(self, surface):
        pygame.draw.polygon(surface, self.color, self.get_transformed_points())
