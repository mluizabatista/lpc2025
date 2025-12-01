import pygame
import random

def load_spritesheet(image_path, frame_width, frame_height):
    sheet = pygame.image.load(image_path).convert_alpha()
    sheet_width, sheet_height = sheet.get_size()

    frames = []
    for y in range(0, sheet_height, frame_height):
        for x in range(0, sheet_width, frame_width):
            if x + frame_width > sheet_width or y + frame_height > sheet_height:
                continue
            frame = sheet.subsurface((x, y, frame_width, frame_height))
            frames.append(frame)
    return frames


# -------------------- BASE ENTITY ----------------------
class Entity(pygame.sprite.Sprite):
    def __init__(self, x, y, speed, spritesheet_idle, spritesheet_walk, frame_w, frame_h, groups):
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

    def set_bounds(self, bounds):
        self.bounds = bounds

    def animate(self, dt):
        if len(self.current_anim) == 0:
            return

        self.frame_time += dt
        if self.frame_time >= self.frame_speed:
            self.frame_time = 0
            self.frame = (self.frame + 1) % len(self.current_anim)

            base_img = self.current_anim[self.frame]
            if self.facing_left:
                base_img = pygame.transform.flip(base_img, True, False)

            self.image = base_img
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
        self.current_anim = self.anim_walk if moving else self.anim_idle

        if self.dx < 0:
            self.facing_left = True
        elif self.dx > 0:
            self.facing_left = False

        self.move(dt)
        self.animate(dt)


# -------------------- PLAYER ----------------------
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

    def update(self, dt):
        keys = pygame.key.get_pressed()
        self.dx = keys[pygame.K_d] - keys[pygame.K_a]
        self.dy = keys[pygame.K_s] - keys[pygame.K_w]
        super().update(dt)


# -------------------- DOBERMANN ----------------------
class DobermannNPC(Entity):
    def __init__(self, x, y, groups):
        super().__init__(
            x, y,
            speed=50,
            spritesheet_idle="assets/dobermann/Idle.png",
            spritesheet_walk="assets/dobermann/Walk.png",
            frame_w=48, frame_h=48,
            groups=groups
        )
        self.player = None

    def update(self, dt):
        if self.player:
            px, py = self.player.x, self.player.y
            dx = px - self.x
            dy = py - self.y
            dist = max(1, (dx**2 + dy**2) ** 0.5)
            self.dx = dx / dist
            self.dy = dy / dist

        super().update(dt)


# -------------------- BLACK CAT ----------------------
class BlackCatNPC(Entity):
    def __init__(self, x, y, groups):
        super().__init__(
            x, y,
            speed=120,
            spritesheet_idle="assets/blackcat/Idle.png",
            spritesheet_walk="assets/blackcat/Walk.png",
            frame_w=48, frame_h=48,
            groups=groups
        )
        self.change_time = 0

    def update(self, dt):
        self.change_time -= dt
        if self.change_time <= 0:
            self.dx = random.choice([-1, 0, 1])
            self.dy = random.choice([-1, 0, 1])
            self.change_time = random.uniform(0.5, 1.3)
        super().update(dt)


# -------------------- ORANGE CAT ----------------------
class OrangeCatNPC(Entity):
    def __init__(self, x, y, groups):
        super().__init__(
            x, y,
            speed=120,
            spritesheet_idle="assets/orangecat/Idle.png",
            spritesheet_walk="assets/orangecat/Walk.png",
            frame_w=48, frame_h=48,
            groups=groups
        )
        self.change_time = 0

    def update(self, dt):
        self.change_time -= dt
        if self.change_time <= 0:
            self.dx = random.choice([-1, 0, 1])
            self.dy = random.choice([-1, 0, 1])
            self.change_time = random.uniform(0.5, 1.3)
        super().update(dt)


# -------------------- CHICKEN NPC ----------------------
class ChickenNPC(pygame.sprite.Sprite):
    def __init__(self, x, y, groups):
        super().__init__(groups)

        img = pygame.image.load("assets/chicken.png").convert_alpha()
        self.image = pygame.transform.scale(img, (32, 32))
        self.rect = self.image.get_rect(center=(x, y))

        self.x = x
        self.y = y
        self.speed = 70
        self.dx = random.choice([-1, 0, 1])
        self.dy = random.choice([-1, 0, 1])
        self.change_time = random.uniform(0.5, 1.5)

        self.bounds = None

    def set_bounds(self, bounds):
        self.bounds = bounds

    def update(self, dt):
        self.change_time -= dt
        if self.change_time <= 0:
            self.dx = random.choice([-1, 0, 1])
            self.dy = random.choice([-1, 0, 1])
            self.change_time = random.uniform(0.4, 1.2)

        self.x += self.dx * self.speed * dt
        self.y += self.dy * self.speed * dt

        if self.bounds:
            bx, by, bw, bh = self.bounds
            if self.x < bx: self.x = bx
            if self.x > bx + bw: self.x = bx + bw
            if self.y < by: self.y = by
            if self.y > by + bh: self.y = by + bh

        self.rect.center = (self.x, self.y)
