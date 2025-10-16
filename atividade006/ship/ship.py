from core.config import WIDTH, HEIGHT
from core.triangle import Triangle
from core.projectile import Projectile
import math

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
