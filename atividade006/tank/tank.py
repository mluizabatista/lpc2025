from core.config import WIDTH, HEIGHT, BALL_RADIUS
from core.triangle import Triangle
from core.projectile import Projectile
import core.core as core
import math
import pygame
import time

class Tank(Triangle):

    BACKGROUND_COLOR = (144, 38, 8)

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

        self.keep_inside_screen()

    def move_forward(self):

        angle_radians = math.radians(self.angle)
        self.position[0] += math.sin(angle_radians) * self.SPEED
        self.position[1] -= math.cos(angle_radians) * self.SPEED

    def keep_inside_screen(self):

        if self.position[0] < 0:
            self.position[0] = 0

        elif self.position[0] > WIDTH:
            self.position[0] = WIDTH

        if self.position[1] < 0:
            self.position[1] = 0

        elif self.position[1] > HEIGHT:
            self.position[1] = HEIGHT

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

# Rani eu vou ter pesadelos com esse labirinto 

    def draw_ambience(self, surface):
        wall_color = (237, 187, 49)
        wall_thickness = 40
        top_margin = 80

        # --- BORDAS EXTERNAS (NÃO ALTERAR) ---
        self.walls = [
            (0, top_margin, WIDTH, wall_thickness),  # topo
            (0, HEIGHT - wall_thickness, WIDTH, wall_thickness),  # base
            (0, top_margin, wall_thickness, HEIGHT - top_margin - wall_thickness),  # esquerda
            (WIDTH - wall_thickness, top_margin, wall_thickness, HEIGHT - top_margin - wall_thickness),  # direita
        ]

        # --- BLOCO CENTRAL (pequeno quadrado centralizado) ---
        center_block_size = 60
        self.walls.append((WIDTH/2 - center_block_size/2, HEIGHT/2 - center_block_size/2, center_block_size, center_block_size))

        # --- "ILHAS" NAS QUATRO EXTREMIDADES (cada ilha = L + pequena barra) ---
        # valores posicionados para imitar a imagem; distância do interior da borda:
        # superior-esquerda
        self.walls += [
            (120, 140, 120, 28),    # horizontal superior ilha
            (120, 200, 120, 28),
            (90, 160, 28, 80),
        ]
        # superior-direita (espelhado)
        self.walls += [
            (WIDTH - 240, 140, 120, 28),
            (WIDTH - 240, 200, 120, 28),
            (WIDTH - 118, 160, 28, 80),
        ]
        # inferior-esquerda
        self.walls += [
            (120, HEIGHT - 240, 120, 28),
            (120, HEIGHT - 180, 120, 28),
            (90, HEIGHT - 220, 28, 80),
        ]
        # inferior-direita
        self.walls += [
            (WIDTH - 240, HEIGHT - 240, 120, 28),
            (WIDTH - 240, HEIGHT - 180, 120, 28),
            (WIDTH - 118, HEIGHT - 220, 28, 80),
        ]

        # --- ESTRUTURAS "COLCHETE" (brackets) laterais ---
        # no layout da imagem as aberturas apontam para dentro (parecem dois C pequenos).
        # vamos construir cada colchete como: pequena horizontal superior, grande vertical, pequena horizontal inferior.
        bracket_width = 28
        bracket_len_h = 110
        bracket_gap_top = top_margin + 140

        # esquerdo: posicionado ~100px da borda interna
        left_x = 100
        self.walls += [
            (left_x, bracket_gap_top, bracket_len_h, 25),          # top small horizontal (abre para a direita)
            (left_x, bracket_gap_top + 25, 25, 140),               # vertical bar (desce)
            (left_x, bracket_gap_top + 25 + 140, bracket_len_h, 25)  # bottom small horizontal (abre para a direita)
        ]

        # direito: espelhado (abertura para a esquerda)
        right_x = WIDTH - 100 - bracket_len_h
        # para que pareça colchete invertido, as "pequenas" horizontais ficam mais internas (abrindo para esquerda)
        self.walls += [
            (right_x, bracket_gap_top, bracket_len_h, 25),
            (right_x + bracket_len_h - 25, bracket_gap_top + 25, 25, 140),
            (right_x, bracket_gap_top + 25 + 140, bracket_len_h, 25)
        ]

        # --- 4 QUADRADOS (posições pedidas) ---
        # square_size
        sq = 40

        # Dois horizontais centralizados, separados por 200 px (centros)
        center_y = HEIGHT/2
        left_center_x = WIDTH/2 - 100   # centro esquerdo
        right_center_x = WIDTH/2 + 100  # centro direito
        self.walls += [
            (left_center_x - sq/2, center_y - sq/2, sq, sq),
            (right_center_x - sq/2, center_y - sq/2, sq, sq),
        ]

        # Dois verticalmente centralizados: ambos centralizados horizontalmente (x = WIDTH/2),
        # um perto da margem superior interna e outro perto da margem inferior interna,
        # com distância vertical entre seus centros de 400 px.
        vert_center_x = WIDTH/2
        top_center_y = top_margin + 120
        bottom_center_y = top_center_y + 400
        self.walls += [
            (vert_center_x - sq/2, top_center_y - sq/2, sq, sq),
            (vert_center_x - sq/2, bottom_center_y - sq/2, sq, sq),
        ]

        # --- 4 "L" menores (cantoneiras internas, aproximando layout) ---
        # Dispostos próximos ao centro, como na imagem
        L_w = 60
        L_h = 20
        # cima-esquerda L
        self.walls += [
            (WIDTH/2 - 130, HEIGHT/2 - 80, L_w, L_h),
            (WIDTH/2 - 130, HEIGHT/2 - 80, L_h, L_w),
        ]
        # cima-direita L (espelhado)
        self.walls += [
            (WIDTH/2 + 70, HEIGHT/2 - 80, L_w, L_h),
            (WIDTH/2 + 110, HEIGHT/2 - 80, L_h, L_w),
        ]
        # baixo-esquerda L
        self.walls += [
            (WIDTH/2 - 130, HEIGHT/2 + 40, L_w, L_h),
            (WIDTH/2 - 130, HEIGHT/2 + 40 + L_h, L_h, L_w),
        ]
        # baixo-direita L
        self.walls += [
            (WIDTH/2 + 70, HEIGHT/2 + 40, L_w, L_h),
            (WIDTH/2 + 110, HEIGHT/2 + 40 + L_h, L_h, L_w),
        ]

        # --- DESENHA TODAS AS PAREDES ---
        for rect in self.walls:
            pygame.draw.rect(surface, wall_color, rect)

        # --- COLISÃO DO TANQUE: se tocar a parede, recua (comportamento existente) ---
        tank_rect = pygame.Rect(self.position[0] - 15, self.position[1] - 15, 30, 30)
        for rect in self.walls:
            wall_rect = pygame.Rect(rect)
            if tank_rect.colliderect(wall_rect):
                # recua o tanque (mesma estratégia que você já tinha)
                angle_radians = math.radians(self.angle)
                self.position[0] -= math.sin(angle_radians) * self.SPEED * 2
                self.position[1] += math.cos(angle_radians) * self.SPEED * 2
                break

        # --- PROJÉTEIS: somem ao tocar qualquer parede ---
        for proj in core.projectiles[:]:
            proj_rect = pygame.Rect(proj.x - BALL_RADIUS/2, proj.y - BALL_RADIUS/2, BALL_RADIUS, BALL_RADIUS)
            for rect in self.walls:
                if pygame.Rect(rect).colliderect(proj_rect):
                    if proj in core.projectiles:
                        core.projectiles.remove(proj)
                    break
