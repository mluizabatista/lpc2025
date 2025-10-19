# ship/ship.py

from core.config import WIDTH, HEIGHT
from core.triangle import Triangle
from core.projectile import Projectile
import math
import pygame
import time

class Ship(Triangle):

    def __init__(self, position, color, controls):
        super().__init__(position, color, controls)
        self.controls = controls
        self.active_projectile = None

        self.is_disabled = False
        self.disabled_timer = 0
        self.SPIN_SPEED = 15
        self.last_update = time.time()

    def take_damage(self, duration_seconds=1):
        if not self.is_disabled:
            self.is_disabled = True
            self.disabled_timer = duration_seconds
            print(f"Nave atingida! Girando por {duration_seconds} segundos.")

    def update(self):
        now = time.time()
        delta_time = now - self.last_update
        self.last_update = now

        if self.is_disabled:
            self.angle = (self.angle + self.SPIN_SPEED) % 360.0
            self.disabled_timer -= delta_time
            if self.disabled_timer <= 0:
                self.is_disabled = False
                print("Controle restaurado!")
        
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

    def draw_clouds(self, surface):
        cloud_color = (173, 216, 230)
        
        # --- ALTERAÇÕES: Nuvens reajustadas para criar duas massas separadas ---
        # As coordenadas X foram ajustadas para mover os grupos para a esquerda e direita
        # e criar um espaço vazio no centro.

        # Nuvem GRANDE da ESQUERDA (conjunto)
        pygame.draw.rect(surface, cloud_color, (80, 300, 300, 100)) # Principal esquerda
        pygame.draw.rect(surface, cloud_color, (40, 310, 100, 70))  # Extensão inferior esquerda
        pygame.draw.rect(surface, cloud_color, (90, 270, 110, 80))  # Extensão superior esquerda
        pygame.draw.rect(surface, cloud_color, (130, 350, 120, 90)) # Extensão inferior central esq
        pygame.draw.rect(surface, cloud_color, (190, 280, 120, 80)) # Extensão superior central esq
        pygame.draw.rect(surface, cloud_color, (240, 340, 120, 90)) # Extensão inferior direita esq
        pygame.draw.rect(surface, cloud_color, (300, 310, 100, 70)) # Extensão superior direita esq
        pygame.draw.rect(surface, cloud_color, (360, 290, 110, 80)) # Extensão ponta direita esq
        pygame.draw.rect(surface, cloud_color, (410, 330, 90, 60))  # Extensão mais à direita esq
        pygame.draw.rect(surface, cloud_color, (180, 370, 110, 80)) # Abaixo da principal esquerda
        pygame.draw.rect(surface, cloud_color, (100, 330, 90, 60))  # Outra extensão inferior esquerda


        # Nuvem GRANDE da DIREITA (conjunto) - Movida significativamente para a direita
        pygame.draw.rect(surface, cloud_color, (WIDTH - 380, 300, 300, 100)) # Principal direita (usando WIDTH para referência)
        pygame.draw.rect(surface, cloud_color, (WIDTH - 420, 310, 100, 70)) # Extensão inferior esquerda direita
        pygame.draw.rect(surface, cloud_color, (WIDTH - 370, 270, 110, 80)) # Extensão superior esquerda direita
        pygame.draw.rect(surface, cloud_color, (WIDTH - 330, 350, 120, 90)) # Extensão inferior central direita
        pygame.draw.rect(surface, cloud_color, (WIDTH - 270, 280, 120, 80)) # Extensão superior central direita
        pygame.draw.rect(surface, cloud_color, (WIDTH - 220, 340, 120, 90)) # Extensão inferior direita direita
        pygame.draw.rect(surface, cloud_color, (WIDTH - 160, 310, 100, 70)) # Extensão superior direita direita
        pygame.draw.rect(surface, cloud_color, (WIDTH - 100, 290, 110, 80)) # Extensão ponta direita
        pygame.draw.rect(surface, cloud_color, (WIDTH - 50, 330, 90, 60))  # Extensão mais à direita
        pygame.draw.rect(surface, cloud_color, (WIDTH - 280, 370, 110, 80)) # Abaixo da principal direita
        pygame.draw.rect(surface, cloud_color, (WIDTH - 360, 330, 90, 60))  # Outra extensão inferior direita
        
        # Estas eram as nuvens isoladas que você tinha, reajustadas para se encaixar nos grupos
        # Eram: (800, 300, 140, 100), (500, 320, 120, 80), (560, 270, 100, 70), (600, 360, 130, 90), (650, 270, 100, 70), (710, 340, 120, 80), (780, 280, 100, 70), (840, 310, 100, 70), (880, 330, 80, 60), (560, 340, 90, 60), (740, 370, 100, 70), (575, 300, 300, 150)
        # Eu as re-organizei e ajustei as coordenadas para formar os dois grandes blocos.