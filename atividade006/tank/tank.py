# tank/tank.py

from core.config import WIDTH, HEIGHT, BALL_RADIUS
from core.triangle import Triangle
from core.projectile import Projectile
import core.core as core
import math
import pygame
import time

class Tank(Triangle):

    def __init__(self, position, color, controls):
        super().__init__(position, color, controls)
        self.controls = controls
        self.active_projectile = None
        self.is_disabled = False
        self.disabled_timer = 0
        self.SPIN_SPEED = 1
        self.DISABLED_SPIN_SPEED = 100
        self.SPEED = 1
        self.last_update = time.time()
        self.moving_forward = False
        self.rotating = False

    def update(self):
        now = time.time()
        delta_time = now - self.last_update
        self.last_update = now

        if self.is_disabled:
            self.angle = (self.angle + self.DISABLED_SPIN_SPEED * delta_time * 60) % 360.0
            self.disabled_timer -= delta_time
            if self.disabled_timer <= 0:
                self.is_disabled = False
            return

        keys = pygame.key.get_pressed()
        forward_pressed = keys[self.controls["forward"]]

        if not forward_pressed:
            if keys[self.controls["left"]]:
                self.angle = (self.angle - self.SPIN_SPEED) % 360.0
                self.rotating = True
            elif keys[self.controls["right"]]:
                self.angle = (self.angle + self.SPIN_SPEED) % 360.0
                self.rotating = True
            else:
                self.rotating = False
        else:
            self.rotating = True

        if forward_pressed and not (keys[self.controls["left"]] or keys[self.controls["right"]]):
            self.move_forward()
            self.moving_forward = True
        else:
            self.moving_forward = False
        
        # A colisão com as paredes agora controla os limites, não mais keep_inside_screen
        # self.keep_inside_screen()

    def move_forward(self):
        angle_radians = math.radians(self.angle)
        self.position[0] += math.sin(angle_radians) * self.SPEED
        self.position[1] -= math.cos(angle_radians) * self.SPEED

    def keep_inside_screen(self):
        # Esta função não é mais necessária com as paredes externas
        pass

    def take_damage(self, duration_seconds=1):
        if not self.is_disabled:
            self.is_disabled = True
            self.disabled_timer = duration_seconds

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

    # --- MÉTODO DO MAPA TOTALMENTE REESCRITO ---
    def draw_ambience(self, surface):
        wall_color = (205, 179, 128)  # Cor bege/amarelada das paredes
        
        # --- Definição da estrutura do novo mapa ---
        self.walls = []
        margin = 30
        wall_thickness = 15

        # 1. Bordas Externas
        self.walls.append(pygame.Rect(0, 0, WIDTH, margin)) # Topo
        self.walls.append(pygame.Rect(0, HEIGHT - margin, WIDTH, margin)) # Base
        self.walls.append(pygame.Rect(0, 0, margin, HEIGHT)) # Esquerda
        self.walls.append(pygame.Rect(WIDTH - margin, 0, margin, HEIGHT)) # Direita

        # 2. Barreiras Centrais (2 retângulos verticais)
        center_wall_w = 20
        center_wall_h = 150
        center_gap = 180
        self.walls.append(pygame.Rect(WIDTH/2 - center_gap/2 - center_wall_w, HEIGHT/2 - center_wall_h/2, center_wall_w, center_wall_h))
        self.walls.append(pygame.Rect(WIDTH/2 + center_gap/2, HEIGHT/2 - center_wall_h/2, center_wall_w, center_wall_h))

        # 3. Barreiras Laterais (em formato de U)
        side_wall_h = 200
        side_wall_w = 80
        side_offset_x = 150
        # U da Esquerda
        self.walls.append(pygame.Rect(side_offset_x, HEIGHT/2 - side_wall_h/2, side_wall_w, wall_thickness))
        self.walls.append(pygame.Rect(side_offset_x, HEIGHT/2 + side_wall_h/2 - wall_thickness, side_wall_w, wall_thickness))
        self.walls.append(pygame.Rect(side_offset_x, HEIGHT/2 - side_wall_h/2, wall_thickness, side_wall_h))
        # U da Direita
        self.walls.append(pygame.Rect(WIDTH - side_offset_x - side_wall_w, HEIGHT/2 - side_wall_h/2, side_wall_w, wall_thickness))
        self.walls.append(pygame.Rect(WIDTH - side_offset_x - side_wall_w, HEIGHT/2 + side_wall_h/2 - wall_thickness, side_wall_w, wall_thickness))
        self.walls.append(pygame.Rect(WIDTH - side_offset_x - wall_thickness, HEIGHT/2 - side_wall_h/2, wall_thickness, side_wall_h))

        # 4. Barreiras de Canto (em formato de L)
        corner_wall_len = 100
        corner_offset = 120
        # Canto Superior Esquerdo
        self.walls.append(pygame.Rect(corner_offset, corner_offset, corner_wall_len, wall_thickness))
        self.walls.append(pygame.Rect(corner_offset, corner_offset, wall_thickness, corner_wall_len))
        # Canto Superior Direito
        self.walls.append(pygame.Rect(WIDTH - corner_offset - corner_wall_len, corner_offset, corner_wall_len, wall_thickness))
        self.walls.append(pygame.Rect(WIDTH - corner_offset - wall_thickness, corner_offset, wall_thickness, corner_wall_len))
        # Canto Inferior Esquerdo
        self.walls.append(pygame.Rect(corner_offset, HEIGHT - corner_offset - wall_thickness, corner_wall_len, wall_thickness))
        self.walls.append(pygame.Rect(corner_offset, HEIGHT - corner_offset - corner_wall_len, wall_thickness, corner_wall_len))
        # Canto Inferior Direito
        self.walls.append(pygame.Rect(WIDTH - corner_offset - corner_wall_len, HEIGHT - corner_offset - wall_thickness, corner_wall_len, wall_thickness))
        self.walls.append(pygame.Rect(WIDTH - corner_offset - wall_thickness, HEIGHT - corner_offset - corner_wall_len, wall_thickness, corner_wall_len))

        # --- DESENHA TODAS AS PAREDES ---
        for wall in self.walls:
            pygame.draw.rect(surface, wall_color, wall)

        # --- COLISÃO DO TANQUE ---
        tank_rect = pygame.Rect(self.position[0] - 15, self.position[1] - 15, 30, 30)
        for wall in self.walls:
            if tank_rect.colliderect(wall):
                angle_radians = math.radians(self.angle)
                # Recua o tanque um pouco mais para evitar que ele fique preso
                self.position[0] -= math.sin(angle_radians) * self.SPEED * 2
                self.position[1] += math.cos(angle_radians) * self.SPEED * 2
                break

        # --- COLISÃO DOS PROJÉTEIS ---
        for proj in core.projectiles[:]:
            proj_rect = pygame.Rect(proj.x - BALL_RADIUS, proj.y - BALL_RADIUS, BALL_RADIUS*2, BALL_RADIUS*2)
            for wall in self.walls:
                if wall.colliderect(proj_rect):
                    if proj in core.projectiles:
                        core.projectiles.remove(proj)
                    break