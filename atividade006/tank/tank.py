from core.config import WIDTH, HEIGHT
from core.triangle import Triangle
import pygame
import time

class Tank(Triangle): 

    def __init__(self, position, color, controls):
        super().__init__(position, color, controls)
        self.controls = controls
        self.active_projectile = None
        self.is_disabled = False
        self.disabled_timer = 0
        self.SPIN_SPEED = 15
        self.last_update = time.time()

    def update(self):
        pass

    def draw(self, surface):
        rect_width = 40
        rect_height = 25
        rect = pygame.Rect(
            self.position[0] - rect_width / 2,
            self.position[1] - rect_height / 2,
            rect_width,
            rect_height
        )
        pygame.draw.rect(surface, self.color, rect)

    def shoot(self, projectiles):
        pass

    def draw_clouds(self, surface):
        surface.fill((0, 0, 0))
