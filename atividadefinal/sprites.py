import pygame
from utils import load_spritesheet
from config import SPRITE_DIR, FRAME_SIZE, SCALE_FACTOR, PLAYER_SPEED, TOP_BORDER_THICKNESS, BORDER_THICKNESS, WIDTH, HEIGHT

class Player(pygame.sprite.Sprite):
    def __init__(self, game):
        super().__init__()
        self.game = game

        self.anim_idle = load_spritesheet(f"{SPRITE_DIR}/Idle.png", FRAME_SIZE, FRAME_SIZE)
        self.anim_walk = load_spritesheet(f"{SPRITE_DIR}/Walk.png", FRAME_SIZE, FRAME_SIZE)
        self.anim_attack = load_spritesheet(f"{SPRITE_DIR}/Attack.png", FRAME_SIZE, FRAME_SIZE)

        if not self.anim_idle: self.anim_idle = [pygame.Surface((FRAME_SIZE, FRAME_SIZE))]
        if not self.anim_walk: self.anim_walk = [pygame.Surface((FRAME_SIZE, FRAME_SIZE))]
        if not self.anim_attack: self.anim_attack = [pygame.Surface((FRAME_SIZE, FRAME_SIZE))]

        self.current_anim = self.anim_idle
        self.frame = 0
        self.frame_time = 0.0
        self.frame_speed = 0.12  

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
        self.image = pygame.transform.scale(base_img, (int(w * self.scale), int(h * self.scale)))
        self.rect = self.image.get_rect(center=(self.x, self.y))

    def set_animation(self, new_anim):

        if self.current_anim is not new_anim:
            self.current_anim = new_anim
            self.frame = 0
            self.frame_time = 0.0

    def handle_input_and_move(self, dt):
        keys = pygame.key.get_pressed()

        dx = 0.0
        dy = 0.0

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

        left_limit = BORDER_THICKNESS + 1
        top_limit = BORDER_THICKNESS + 1

        self.x = max(left_limit, min(self.x, WIDTH - left_limit))
        self.y = max(top_limit, min(self.y, HEIGHT - top_limit))

    def update_animation_and_image(self, dt):
        if self.attacking:
            now = pygame.time.get_ticks() / 1000.0
            if now - self.attack_start >= self.attack_duration:
                self.attacking = False

        if self.attacking:
            self.set_animation(self.anim_attack)
        else:
            pass

        self.frame_time += dt
        if self.frame_time >= self.frame_speed:

            self.frame_time -= self.frame_speed
            self.frame = (self.frame + 1) % len(self.current_anim)

        base_img = self.current_anim[self.frame]
        w, h = base_img.get_size()
        scaled = pygame.transform.scale(base_img, (int(w * self.scale), int(h * self.scale)))

        if self.facing_left:
            scaled = pygame.transform.flip(scaled, True, False)

        self.image = scaled

        self.rect = self.image.get_rect(center=(int(self.x), int(self.y)))

        left_limit = BORDER_THICKNESS + self.rect.width // 2 + 1
        right_limit = WIDTH - (BORDER_THICKNESS + self.rect.width // 2 + 1)
        top_limit = TOP_BORDER_THICKNESS + self.rect.height // 2 + 1
        bottom_limit = HEIGHT - (BORDER_THICKNESS + self.rect.height // 2 + 1)

        self.x = max(left_limit, min(self.x, right_limit))
        self.y = max(top_limit, min(self.y, bottom_limit))

        self.rect.center = (int(self.x), int(self.y))

    def update(self, dt):

        self.handle_input_and_move(dt)

        if not self.attacking:

            keys = pygame.key.get_pressed()
            moving = keys[pygame.K_w] or keys[pygame.K_s] or keys[pygame.K_a] or keys[pygame.K_d]
            if moving:
                self.set_animation(self.anim_walk)
            else:
                self.set_animation(self.anim_idle)

        self.update_animation_and_image(dt)