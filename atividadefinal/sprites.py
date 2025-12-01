import pygame
import random
from math import dist


def load_spritesheet(image_path, frame_width, frame_height):
    sheet = pygame.image.load(image_path).convert_alpha()
    sw, sh = sheet.get_size()

    frames = []
    for y in range(0, sh, frame_height):
        for x in range(0, sw, frame_width):
            if x + frame_width > sw or y + frame_height > sh:
                continue
            frame = sheet.subsurface((x, y, frame_width, frame_height)).copy()
            frames.append(frame)
    return frames


def load_hurt_two_frames(path, frame_w, frame_h):
    sheet = pygame.image.load(path).convert_alpha()
    sw, sh = sheet.get_size()

    frames = []
    for x in range(0, sw, frame_w):
        if x + frame_w <= sw:
            frame = sheet.subsurface((x, 0, frame_w, frame_h)).copy()
            frames.append(frame)
    return frames


# =====================================================
# CLASSE BASE
# =====================================================
class Entity(pygame.sprite.Sprite):
    def __init__(self, x, y, speed,
                 spritesheet_idle, spritesheet_walk,
                 frame_w, frame_h, groups):

        super().__init__(groups)

        self.x = x
        self.y = y
        self.speed = speed

        self.frame = 0
        self.frame_time = 0
        self.frame_speed = 0.09

        self.anim_idle = load_spritesheet(spritesheet_idle, frame_w, frame_h)
        self.anim_walk = load_spritesheet(spritesheet_walk, frame_w, frame_h)

        self.current_anim = self.anim_idle

        self.image = self.current_anim[0]
        self.rect = self.image.get_rect(center=(x, y))

        self.dx = 0
        self.dy = 0
        self.facing_left = False

        self.bounds = None

    def set_anim(self, anim):
        if self.current_anim is not anim:
            self.current_anim = anim
            self.frame = 0
            self.frame_time = 0

    def set_bounds(self, bounds):
        self.bounds = bounds

    def animate(self, dt):
        if len(self.current_anim) == 0:
            return

        self.frame_time += dt
        if self.frame_time >= self.frame_speed:
            self.frame_time = 0
            self.frame = (self.frame + 1) % len(self.current_anim)

        base = self.current_anim[self.frame]

        if self.facing_left:
            base = pygame.transform.flip(base, True, False)

        self.image = base
        self.rect = self.image.get_rect(center=(self.x, self.y))

    def move(self, dt):
        self.x += self.dx * self.speed * dt
        self.y += self.dy * self.speed * dt

        if self.bounds:
            bx, by, bw, bh = self.bounds
            if self.x < bx: self.x = bx
            if self.x > bx + bw: self.x = bx + bw
            if self.y < by: self.y = by
            if self.y > by + bh: self.y = by + bh

        self.rect.center = (self.x, self.y)

    def update(self, dt):
        moving = self.dx != 0 or self.dy != 0
        if moving:
            self.set_anim(self.anim_walk)
        else:
            self.set_anim(self.anim_idle)

        if self.dx < 0: self.facing_left = True
        if self.dx > 0: self.facing_left = False

        self.move(dt)
        self.animate(dt)


# =====================================================
# PLAYER
# =====================================================
class Player(Entity):
    def __init__(self, x, y, groups):
        super().__init__(
            x, y,
            speed=150,
            spritesheet_idle="assets/caramel/Idle.png",
            spritesheet_walk="assets/caramel/Walk.png",
            frame_w=48, frame_h=48,
            groups=groups
        )

        self.anim_hurt = load_hurt_two_frames("assets/caramel/Hurt.png", 48, 48)
        self.anim_attack = load_spritesheet("assets/caramel/Attack.png", 48, 48)

        self.is_hurt = False
        self.hurt_timer = 0

        self.is_barking = False
        self.bark_timer = 0
        self.bark_cd = 0

        self.score = 0

    def bark(self):
        if self.bark_cd > 0 or self.is_hurt:
            return

        self.is_barking = True
        self.bark_timer = 0.4
        self.bark_cd = 7.0

        self.set_anim(self.anim_attack)
        self.frame = 0

    def hurt(self):
        if not self.is_hurt:
            self.is_hurt = True
            self.hurt_timer = 0.35
            self.set_anim(self.anim_hurt)
            self.frame = 0

    def update(self, dt):
        keys = pygame.key.get_pressed()

        self.dx = keys[pygame.K_d] - keys[pygame.K_a]
        self.dy = keys[pygame.K_s] - keys[pygame.K_w]

        if self.bark_cd > 0:
            self.bark_cd -= dt

        if self.is_barking:
            self.bark_timer -= dt
            if self.bark_timer <= 0:
                self.is_barking = False
            self.animate(dt)
            return

        if self.is_hurt:
            self.hurt_timer -= dt
            if self.hurt_timer <= 0:
                self.is_hurt = False
            self.animate(dt)
            return

        super().update(dt)


# =====================================================
# NPCs
# =====================================================
class DobermannNPC(Entity):
    def __init__(self, x, y, groups):
        super().__init__(x, y, 90,
            "assets/dobermann/Idle.png",
            "assets/dobermann/Walk.png",
            48, 48, groups)

        self.player = None
        self.random_time = 0

    def update(self, dt):
        if self.player is not None:
            px, py = self.player.x, self.player.y
            dx = px - self.x
            dy = py - self.y
            d = max(1, (dx*dx + dy*dy)**0.5)

            self.dx = dx / d
            self.dy = dy / d
        super().update(dt)


class BlackCatNPC(Entity):
    def __init__(self, x, y, groups):
        super().__init__(x, y, 110,
            "assets/blackcat/Idle.png",
            "assets/blackcat/Walk.png",
            48, 48, groups)
        self.change_time = 0

    def update(self, dt):
        self.change_time -= dt
        if self.change_time <= 0:
            self.dx = random.choice([-1, 0, 1])
            self.dy = random.choice([-1, 0, 1])
            self.change_time = random.uniform(0.5, 1.3)
        super().update(dt)


class OrangeCatNPC(Entity):
    def __init__(self, x, y, groups):
        super().__init__(x, y, 110,
            "assets/orangecat/Idle.png",
            "assets/orangecat/Walk.png",
            48, 48, groups)
        self.change_time = 0

    def update(self, dt):
        self.change_time -= dt
        if self.change_time <= 0:
            self.dx = random.choice([-1, 0, 1])
            self.dy = random.choice([-1, 0, 1])
            self.change_time = random.uniform(0.5, 1.3)
        super().update(dt)


# =====================================================
# GALINHA
# =====================================================
class Chicken(Entity):
    def __init__(self, x, y, groups):
        super().__init__(
            x, y, 90,
            "assets/chicken.png",
            "assets/chicken.png",
            32, 32, groups
        )
        self.change_time = 0

    def update(self, dt):
        self.change_time -= dt
        if self.change_time <= 0:
            self.dx = random.choice([-1, 0, 1])
            self.dy = random.choice([-1, 0, 1])
            self.change_time = random.uniform(0.4, 1.0)

        super().update(dt)
