from core.config import WIDTH, HEIGHT
from core.triangle import Triangle
from core.projectile import Projectile
import math
import pygame

# Ranielly: Faz o triângulo atravessar as bordas e reaparecer do outro lado (wrap around)

class Ship(Triangle):

    def __init__(self, position, color, controls):
        super().__init__(position, color, controls)
        self.controls = controls
        self.active_projectile = None

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

        if self.active_projectile is None:
            angle_radians = math.radians(self.angle)

            nose_x = self.position[0] + math.sin(angle_radians) * 25
            nose_y = self.position[1] - math.cos(angle_radians) * 25

            projectile = Projectile(nose_x, nose_y, self.angle, self.color)

            # 🔹 Registra quem disparou o projétil (necessário para o sistema de colisão)
            projectile.shooter = self

            projectiles.append(projectile)

            self.active_projectile = projectile

    def draw_clouds(self, surface):
    
        cloud_color = (173, 216, 230) 

        pygame.draw.ellipse(surface, cloud_color, (800, 300, 140, 100))
        pygame.draw.ellipse(surface, cloud_color, (500, 320, 120, 80))
        pygame.draw.ellipse(surface, cloud_color, (560, 270, 100, 70))
        pygame.draw.ellipse(surface, cloud_color, (600, 360, 130, 90))
        pygame.draw.ellipse(surface, cloud_color, (650, 270, 100, 70))
        pygame.draw.ellipse(surface, cloud_color, (710, 340, 120, 80))
        pygame.draw.ellipse(surface, cloud_color, (780, 280, 100, 70))
        pygame.draw.ellipse(surface, cloud_color, (840, 310, 100, 70))
        pygame.draw.ellipse(surface, cloud_color, (880, 330, 80, 60))
        pygame.draw.ellipse(surface, cloud_color, (560, 340, 90, 60))
        pygame.draw.ellipse(surface, cloud_color, (740, 370, 100, 70))
        pygame.draw.ellipse(surface, cloud_color, (80, 300, 300, 100))
        pygame.draw.ellipse(surface, cloud_color, (575, 300, 300, 150))
        pygame.draw.ellipse(surface, cloud_color, (40, 310, 100, 70))
        pygame.draw.ellipse(surface, cloud_color, (90, 270, 110, 80))
        pygame.draw.ellipse(surface, cloud_color, (130, 350, 120, 90))
        pygame.draw.ellipse(surface, cloud_color, (190, 280, 120, 80))
        pygame.draw.ellipse(surface, cloud_color, (240, 340, 120, 90))
        pygame.draw.ellipse(surface, cloud_color, (300, 310, 100, 70))
        pygame.draw.ellipse(surface, cloud_color, (360, 290, 110, 80))
        pygame.draw.ellipse(surface, cloud_color, (410, 330, 90, 60))
        pygame.draw.ellipse(surface, cloud_color, (180, 370, 110, 80))
        pygame.draw.ellipse(surface, cloud_color, (100, 330, 90, 60))
