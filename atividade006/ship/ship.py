from core.config import WIDTH, HEIGHT
from core.triangle import Triangle
from core.projectile import Projectile
import math
import pygame
import time

class Ship(Triangle):

    BACKGROUND_COLOR = (135, 206, 235)

    def __init__(self, position, color, controls):

        super().__init__(position, color, controls)
        self.controls = controls
        self.active_projectile = None
        self.is_disabled = False
        self.disabled_timer = 0
        self.SPIN_SPEED = 15              
        self.DISABLED_SPIN_SPEED = 100    
        self.last_update = time.time()

    def take_damage(self, duration_seconds=1):

        if not self.is_disabled:

            self.is_disabled = True
            self.disabled_timer = duration_seconds

    def update(self):

        now = time.time()
        delta_time = now - self.last_update
        self.last_update = now

        if self.is_disabled:

            self.angle = (self.angle + self.DISABLED_SPIN_SPEED * delta_time * 60) % 360.0
            self.disabled_timer -= delta_time

            if self.disabled_timer <= 0:
                self.is_disabled = False
        else:
            super().move()

        self.wrap_around_screen()

    def wrap_around_screen(self):

        if self.position[0] < 0:
            self.position[0] = WIDTH

        elif self.position[0] > WIDTH:
            self.position[0] = 0

        if self.position[1] < 0:
            self.position[1] = HEIGHT

        elif self.position[1] > HEIGHT:
            self.position[1] = 0

    def shoot(self, projectiles):

        if self.is_disabled:
            return

        if self.active_projectile is None or self.active_projectile.is_expired():
            self.active_projectile = None

        if self.active_projectile is None:
            
            angle_radians = math.radians(self.angle)
            nose_x = self.position[0] + math.sin(angle_radians) * 25
            nose_y = self.position[1] - math.cos(angle_radians) * 25

            projectile = Projectile(nose_x, nose_y, self.angle, self.color, shooter=self)
            projectiles.append(projectile)
            self.active_projectile = projectile

    def draw_ambience(self, surface):

        cloud_color = (173, 216, 230)

        pygame.draw.ellipse(surface, cloud_color, (50, 300, 320, 140))
        pygame.draw.ellipse(surface, cloud_color, (80, 280, 160, 100))
        pygame.draw.ellipse(surface, cloud_color, (180, 320, 160, 90))
        pygame.draw.ellipse(surface, cloud_color, (130, 350, 180, 100))
        pygame.draw.ellipse(surface, cloud_color, (240, 300, 140, 80))
        pygame.draw.ellipse(surface, cloud_color, (90, 340, 120, 70))
        pygame.draw.ellipse(surface, cloud_color, (180, 270, 120, 70))

        pygame.draw.ellipse(surface, cloud_color, (WIDTH - 380, 300, 320, 140))
        pygame.draw.ellipse(surface, cloud_color, (WIDTH - 410, 280, 160, 100))
        pygame.draw.ellipse(surface, cloud_color, (WIDTH - 310, 320, 160, 90))
        pygame.draw.ellipse(surface, cloud_color, (WIDTH - 360, 350, 180, 100))
        pygame.draw.ellipse(surface, cloud_color, (WIDTH - 250, 300, 140, 80))
        pygame.draw.ellipse(surface, cloud_color, (WIDTH - 400, 340, 120, 70))
        pygame.draw.ellipse(surface, cloud_color, (WIDTH - 310, 270, 120, 70))
