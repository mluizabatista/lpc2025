import math
import pygame
import time
from core.config import WIDTH, HEIGHT, BALL_RADIUS

BALL_RADIUS = 5
PROJECTILE_SPEED = 10
PROJECTILE_LIFETIME = 2.0 

class Projectile:

    def __init__(self, x, y, angle, color):
        self.x = x
        self.y = y
        self.angle = angle
        self.color = color
        self.created_at = time.time()

        # Luiza: Bullet direction
        angle_radians = math.radians(angle)
        self.dx = math.sin(angle_radians) * PROJECTILE_SPEED
        self.dy = -math.cos(angle_radians) * PROJECTILE_SPEED

    def move(self):

        self.x += self.dx
        self.y += self.dy

        # Luiza: Ranielly's wrap-around
        if self.x < 0:
            self.x = WIDTH
        elif self.x > WIDTH:
            self.x = 0
        if self.y < 0:
            self.y = HEIGHT
        elif self.y > HEIGHT:
            self.y = 0

    def draw(self, surface):
        pygame.draw.circle(surface, self.color, (int(self.x), int(self.y)), BALL_RADIUS)

    def is_expired(self):
        return (time.time() - self.created_at) >= PROJECTILE_LIFETIME
