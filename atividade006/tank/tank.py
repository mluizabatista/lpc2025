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


    def move_forward(self):
        angle_radians = math.radians(self.angle)
        self.position[0] += math.sin(angle_radians) * self.SPEED
        self.position[1] -= math.cos(angle_radians) * self.SPEED

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

    def draw_ambience(self, surface):
        import math
        import core.core as core
        wall_color = (237, 187, 49)  
        margin_top = 100             
        margin_side = 30
        wall_thickness = 20

        self.walls = []

       
        self.walls.append(pygame.Rect(0, margin_top, WIDTH, wall_thickness))
        self.walls.append(pygame.Rect(0, HEIGHT - wall_thickness, WIDTH, wall_thickness))
        self.walls.append(pygame.Rect(0, margin_top, wall_thickness, HEIGHT - margin_top))
        self.walls.append(pygame.Rect(WIDTH - wall_thickness, margin_top, wall_thickness, HEIGHT - margin_top))

        bracket_height = 200
        bracket_width = 80
        bracket_thickness = 20
        bracket_y = HEIGHT // 2 - bracket_height // 2

        bx_left = 100
        self.walls.append(pygame.Rect(bx_left, bracket_y, bracket_thickness, bracket_height))
        self.walls.append(pygame.Rect(bx_left, bracket_y, bracket_width, bracket_thickness))   
        self.walls.append(pygame.Rect(bx_left, bracket_y + bracket_height - bracket_thickness, bracket_width, bracket_thickness)) 

        bx_right = WIDTH - bx_left - bracket_width
        self.walls.append(pygame.Rect(bx_right + bracket_width - bracket_thickness, bracket_y, bracket_thickness, bracket_height))
        self.walls.append(pygame.Rect(bx_right, bracket_y, bracket_width, bracket_thickness))  
        self.walls.append(pygame.Rect(bx_right, bracket_y + bracket_height - bracket_thickness, bracket_width, bracket_thickness))  

        center_size = 50
        self.walls.append(pygame.Rect(WIDTH // 2 - center_size // 2, HEIGHT // 2 - center_size // 2, center_size, center_size))

        L_len = 80
        L_thick = 20
        offset = 100 

        self.walls.append(pygame.Rect(WIDTH // 2 - offset - L_len, HEIGHT // 2 - offset, L_len, L_thick))
        self.walls.append(pygame.Rect(WIDTH // 2 - offset - L_thick, HEIGHT // 2 - offset, L_thick, L_len))

        self.walls.append(pygame.Rect(WIDTH // 2 + offset, HEIGHT // 2 - offset, L_len, L_thick))
        self.walls.append(pygame.Rect(WIDTH // 2 + offset, HEIGHT // 2 - offset, L_thick, L_len))

        self.walls.append(pygame.Rect(WIDTH // 2 - offset - L_len, HEIGHT // 2 + offset, L_len, L_thick))
        self.walls.append(pygame.Rect(WIDTH // 2 - offset - L_thick, HEIGHT // 2 + offset - L_len + L_thick, L_thick, L_len))

        self.walls.append(pygame.Rect(WIDTH // 2 + offset, HEIGHT // 2 + offset, L_len, L_thick))
        self.walls.append(pygame.Rect(WIDTH // 2 + offset, HEIGHT // 2 + offset - L_len + L_thick, L_thick, L_len))

        small_block_size = 40
        self.walls.append(pygame.Rect(WIDTH // 2 - 150 - small_block_size // 2, HEIGHT // 2 - small_block_size // 2, small_block_size, small_block_size))
        self.walls.append(pygame.Rect(WIDTH // 2 + 150 - small_block_size // 2, HEIGHT // 2 - small_block_size // 2, small_block_size, small_block_size))
        self.walls.append(pygame.Rect(WIDTH // 2 - small_block_size // 2, HEIGHT // 2 - 200 - small_block_size // 2, small_block_size, small_block_size))
        self.walls.append(pygame.Rect(WIDTH // 2 - small_block_size // 2, HEIGHT // 2 + 200 - small_block_size // 2, small_block_size, small_block_size))

        for wall in self.walls:
            pygame.draw.rect(surface, wall_color, wall)

        tank_rect = pygame.Rect(int(self.position[0] - 15), int(self.position[1] - 15), 30, 30)
        for wall in self.walls:
            if tank_rect.colliderect(wall):
                angle_radians = math.radians(self.angle)
                self.position[0] -= math.sin(angle_radians) * self.SPEED * 2
                self.position[1] += math.cos(angle_radians) * self.SPEED * 2
                break

        for proj in core.projectiles[:]:
            proj_rect = pygame.Rect(int(proj.x - BALL_RADIUS / 2), int(proj.y - BALL_RADIUS / 2), int(BALL_RADIUS), int(BALL_RADIUS))
            for wall in self.walls:
                if wall.colliderect(proj_rect):
                    if proj in core.projectiles:
                        core.projectiles.remove(proj)
                    break
