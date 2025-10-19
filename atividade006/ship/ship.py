# ship/ship.py

from core.config import WIDTH, HEIGHT
from core.triangle import Triangle
from core.projectile import Projectile
import math
import pygame
import time # <-- Módulo 'time' importado

class Ship(Triangle):

    def __init__(self, position, color, controls):
        super().__init__(position, color, controls)
        self.controls = controls
        self.active_projectile = None

        # --- ADICIONADO: Variáveis para o sistema de dano ---
        self.is_disabled = False          # A nave começa funcionando normalmente
        self.disabled_timer = 0           # Timer para o tempo de desativação
        self.SPIN_SPEED = 15              # Velocidade do giro quando atingido
        self.last_update = time.time()    # Para controlar o tempo do timer

    # --- ADICIONADO: Método chamado quando a nave é atingida ---
    def take_damage(self, duration_seconds=1):
        """Ativa o estado de 'dano' na nave."""
        if not self.is_disabled:
            self.is_disabled = True
            self.disabled_timer = duration_seconds
            print("Nave atingida! Girando por 2 segundos.")

    # --- ADICIONADO: Método que atualiza o estado da nave a cada frame ---
    def update(self):
        """Controla a lógica da nave, incluindo o estado de dano."""
        now = time.time()
        delta_time = now - self.last_update
        self.last_update = now

        if self.is_disabled:
            # Se a nave estiver desabilitada, ela gira sem parar
            self.angle = (self.angle + self.SPIN_SPEED) % 360.0
            
            # Diminui o timer
            self.disabled_timer -= delta_time
            
            # Se o tempo acabou, reativa a nave
            if self.disabled_timer <= 0:
                self.is_disabled = False
                print("Controle restaurado!")
        
        # Chama a lógica de movimento da classe pai
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
        # --- MODIFICADO: Impede o tiro enquanto estiver desabilitado ---
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