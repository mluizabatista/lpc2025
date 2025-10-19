from core.config import WIDTH, HEIGHT
from core.triangle import Triangle
from core.projectile import Projectile
import math
import pygame
import time

class Tank(Triangle):

    BACKGROUND_COLOR = (15, 15, 15)

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

#    def draw_ambience(self, surface):

