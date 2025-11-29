import pygame
import random
from utils import load_spritesheet
from config import (
    SPRITE_DIR,
    FRAME_SIZE,
    SCALE_FACTOR,
    PLAYER_SPEED,
    TOP_BORDER_THICKNESS,
    BORDER_THICKNESS,
    WIDTH,
    HEIGHT
)

# ---------------------------
# PLAYER
# ---------------------------
class Player(pygame.sprite.Sprite):
    def __init__(self, game):
        super().__init__()
        self.game = game

        # carregar animações do player
        self.anim_idle = load_spritesheet(f"{SPRITE_DIR}/Idle.png", FRAME_SIZE, FRAME_SIZE)
        self.anim_walk = load_spritesheet(f"{SPRITE_DIR}/Walk.png", FRAME_SIZE, FRAME_SIZE)
        self.anim_attack = load_spritesheet(f"{SPRITE_DIR}/Attack.png", FRAME_SIZE, FRAME_SIZE)

        # fallbacks mínimos
        if not self.anim_idle: self.anim_idle = [pygame.Surface((FRAME_SIZE, FRAME_SIZE))]
        if not self.anim_walk: self.anim_walk = [pygame.Surface((FRAME_SIZE, FRAME_SIZE))]
        if not self.anim_attack: self.anim_attack = [pygame.Surface((FRAME_SIZE, FRAME_SIZE))]

        self.current_anim = self.anim_idle
        self.frame = 0
        self.frame_time = 0.0
        self.frame_speed = 0.12  # segundos por frame (sensação natural)

        self.facing_left = False

        self.x = WIDTH // 2
        self.y = HEIGHT // 2
        self.speed = PLAYER_SPEED
        self.scale = SCALE_FACTOR

        self.attacking = False
        self.attack_start = 0.0
        self.attack_duration = 0.35

        base_img = self.current_anim[0]
        w, h = base_img.get_size()
        self.image = pygame.transform.scale(base_img, (int(w*self.scale), int(h*self.scale)))
        self.rect = self.image.get_rect(center=(self.x, self.y))

    def set_animation(self, anim):
        if self.current_anim is not anim:
            self.current_anim = anim
            self.frame = 0
            self.frame_time = 0.0

    def handle_input_and_move(self, dt):
        keys = pygame.key.get_pressed()
        dx = dy = 0.0

        if keys[pygame.K_w]:
            dy -= self.speed * dt
        if keys[pygame.K_s]:
            dy += self.speed * dt
        if keys[pygame.K_a]:
            dx -= self.speed * dt
            self.facing_left = True
        if keys[pygame.K_d]:
            dx += self.speed * dt
            self.facing_left = False

        self.x += dx
        self.y += dy

        if keys[pygame.K_SPACE] and not self.attacking:
            self.attacking = True
            self.attack_start = pygame.time.get_ticks() / 1000.0
            self.set_animation(self.anim_attack)

    def update_animation_and_image(self, dt):
        # timeout do ataque
        if self.attacking:
            now = pygame.time.get_ticks() / 1000.0
            if now - self.attack_start >= self.attack_duration:
                self.attacking = False

        # Se não atacando, escolhe walk/idle conforme input
        if not self.attacking:
            keys = pygame.key.get_pressed()
            moving = keys[pygame.K_w] or keys[pygame.K_s] or keys[pygame.K_a] or keys[pygame.K_d]
            self.set_animation(self.anim_walk if moving else self.anim_idle)

        # animação
        self.frame_time += dt
        if self.frame_time >= self.frame_speed:
            self.frame_time -= self.frame_speed
            self.frame = (self.frame + 1) % len(self.current_anim)

        base_img = self.current_anim[self.frame]
        w, h = base_img.get_size()
        scaled = pygame.transform.scale(base_img, (int(w*self.scale), int(h*self.scale)))

        if self.facing_left:
            scaled = pygame.transform.flip(scaled, True, False)

        self.image = scaled
        self.rect = self.image.get_rect(center=(int(self.x), int(self.y)))

        # limites de borda (leva em conta metade do sprite)
        left_limit = BORDER_THICKNESS + self.rect.width//2 + 1
        right_limit = WIDTH - (BORDER_THICKNESS + self.rect.width//2 + 1)
        top_limit = TOP_BORDER_THICKNESS + self.rect.height//2 + 1
        bottom_limit = HEIGHT - (BORDER_THICKNESS + self.rect.height//2 + 1)

        self.x = max(left_limit, min(self.x, right_limit))
        self.y = max(top_limit, min(self.y, bottom_limit))

        self.rect.center = (int(self.x), int(self.y))

    def update(self, dt):
        self.handle_input_and_move(dt)
        self.update_animation_and_image(dt)


# ---------------------------
# GENERIC NPC CLASS
# ---------------------------
class NPC(pygame.sprite.Sprite):
    """
    NPC genérico que usa sprites na pasta assets/<folder> com Idle.png e Walk.png.
    Forneça 'folder' ao instanciar (por exemplo: 'dobermann', 'blackcat', 'orangecat').
    """

    def __init__(self, folder: str, scale: float = 2.0, speed: float = 120.0):
        super().__init__()

        self.folder = folder
        self.anim_idle = load_spritesheet(f"assets/{folder}/Idle.png", FRAME_SIZE, FRAME_SIZE)
        self.anim_walk = load_spritesheet(f"assets/{folder}/Walk.png", FRAME_SIZE, FRAME_SIZE)

        if not self.anim_idle: self.anim_idle = [pygame.Surface((FRAME_SIZE, FRAME_SIZE))]
        if not self.anim_walk: self.anim_walk = [pygame.Surface((FRAME_SIZE, FRAME_SIZE))]

        self.current_anim = self.anim_idle
        self.frame = 0
        self.frame_time = 0.0
        self.frame_speed = 0.15

        self.scale = scale
        self.speed = speed
        self.facing_left = False

        # posição inicial aleatória dentro da área útil (considera margem)
        margin_x = BORDER_THICKNESS + 64
        margin_y = TOP_BORDER_THICKNESS + 64
        self.x = random.randint(margin_x, WIDTH - margin_x)
        self.y = random.randint(margin_y, HEIGHT - margin_y)

        self.direction_timer = random.uniform(0.0, 2.0)
        # dx/dy representam velocidade em px/s (podem ser negativos)
        self.dx = 0.0
        self.dy = 0.0

        base_img = self.current_anim[0]
        w, h = base_img.get_size()
        self.image = pygame.transform.scale(base_img, (int(w*self.scale), int(h*self.scale)))
        self.rect = self.image.get_rect(center=(int(self.x), int(self.y)))

    def choose_new_direction(self):
        # direção como vetor unitário rotacionado
        angle = random.uniform(0, 360)
        v = pygame.math.Vector2(1, 0).rotate(angle)
        self.dx = v.x * self.speed
        self.dy = v.y * self.speed
        self.direction_timer = random.uniform(0.8, 2.5)
        self.facing_left = self.dx < 0

    def move(self, dt):
        self.direction_timer -= dt
        if self.direction_timer <= 0:
            self.choose_new_direction()

        self.x += self.dx * dt
        self.y += self.dy * dt

        # limites (centro da entidade)
        left = BORDER_THICKNESS + self.rect.width//2 + 1
        right = WIDTH - (BORDER_THICKNESS + self.rect.width//2 + 1)
        top = TOP_BORDER_THICKNESS + self.rect.height//2 + 1
        bottom = HEIGHT - (BORDER_THICKNESS + self.rect.height//2 + 1)

        bounced = False
        if self.x < left:
            self.x = left
            self.dx *= -1
            bounced = True
        if self.x > right:
            self.x = right
            self.dx *= -1
            bounced = True
        if self.y < top:
            self.y = top
            self.dy *= -1
            bounced = True
        if self.y > bottom:
            self.y = bottom
            self.dy *= -1
            bounced = True

        if bounced:
            self.facing_left = self.dx < 0

    def animate(self, dt):
        moving = abs(self.dx) > 1e-3 or abs(self.dy) > 1e-3
        self.current_anim = self.anim_walk if moving else self.anim_idle

        self.frame_time += dt
        if self.frame_time >= self.frame_speed:
            self.frame_time -= self.frame_speed
            self.frame = (self.frame + 1) % len(self.current_anim)

        base_img = self.current_anim[self.frame]
        w, h = base_img.get_size()
        img = pygame.transform.scale(base_img, (int(w*self.scale), int(h*self.scale)))
        if self.facing_left:
            img = pygame.transform.flip(img, True, False)

        self.image = img
        self.rect = self.image.get_rect(center=(int(self.x), int(self.y)))

    def update(self, dt):
        self.move(dt)
        self.animate(dt)


# ---------------------------
# CONCRETE NPC SUBCLASSES
# ---------------------------

class DobermannNPC(NPC):
    def __init__(self, game=None):
        # scale e speed pensados para dobermann
        super().__init__("dobermann", scale=2.0, speed=150.0)

class BlackCatNPC(NPC):
    def __init__(self, game=None):
        super().__init__("blackcat", scale=2.0, speed=150.0)

class OrangeCatNPC(NPC):
    def __init__(self, game=None):
        super().__init__("orangecat", scale=2.0, speed=150.0)
