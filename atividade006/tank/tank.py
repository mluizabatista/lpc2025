from core.config import WIDTH, HEIGHT
from core.triangle import Triangle
import math
import pygame
import time

class Tank(Triangle): 

    BACKGROUND_COLOR = (15, 15, 15)  # fundo escuro para o modo tank

    def __init__(self, position, color, controls):

        super().__init__(position, color, controls)
        self.controls = controls
        self.active_projectile = None
        self.is_disabled = False
        self.disabled_timer = 0
        self.SPIN_SPEED = 8        
        self.SPEED = 3            
        self.last_update = time.time()

        self.moving = False
        self.rotating = False

    def update(self):

        now = time.time()
        delta_time = now - self.last_update
        self.last_update = now

        if self.is_disabled:

            self.angle = (self.angle + self.SPIN_SPEED) % 360.0
            self.disabled_timer -= delta_time

            if self.disabled_timer <= 0:
                self.is_disabled = False

            return  

        keys = pygame.key.get_pressed()

        if not self.moving:

            if keys[self.controls["left"]]:

                self.angle = (self.angle - self.SPIN_SPEED) % 360.0
                self.rotating = True

            elif keys[self.controls["right"]]:

                self.angle = (self.angle + self.SPIN_SPEED) % 360.0
                self.rotating = True

            else:
                self.rotating = False

        if not self.rotating:

            if keys[self.controls["forward"]]:

                self.move_forward()
                self.moving = True

            elif keys[self.controls["back"]]:

                self.move_backward()
                self.moving = True

            else:
                self.moving = False

        self.keep_inside_screen()

    def move_forward(self):

        angle_radians = math.radians(self.angle)
        self.position[0] += math.sin(angle_radians) * self.SPEED
        self.position[1] -= math.cos(angle_radians) * self.SPEED

    def move_backward(self):

        angle_radians = math.radians(self.angle)
        self.position[0] -= math.sin(angle_radians) * self.SPEED
        self.position[1] += math.cos(angle_radians) * self.SPEED

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

        pass

    def draw_ambience(self, surface):
        surface.fill(self.BACKGROUND_COLOR)

