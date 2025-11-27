import pygame
from utils import load_spritesheet
from config import SPRITE_DIR, FRAME_SIZE, PLAYER_SPEED

class Player(pygame.sprite.Sprite):
    def __init__(self, game):
        super().__init__()
        self.game = game

        # Carrega spritesheets (caminho relativo via utils.build_path)
        self.anim_idle = load_spritesheet(f"{SPRITE_DIR}/Idle.png", FRAME_SIZE, FRAME_SIZE)
        self.anim_walk = load_spritesheet(f"{SPRITE_DIR}/Walk.png", FRAME_SIZE, FRAME_SIZE)
        self.anim_bark = load_spritesheet(f"{SPRITE_DIR}/Attack.png", FRAME_SIZE, FRAME_SIZE)

        # Proteções mínimas
        if not self.anim_idle: self.anim_idle = [pygame.Surface((FRAME_SIZE, FRAME_SIZE))]
        if not self.anim_walk: self.anim_walk = [pygame.Surface((FRAME_SIZE, FRAME_SIZE))]
        if not self.anim_bark: self.anim_bark = [pygame.Surface((FRAME_SIZE, FRAME_SIZE))]

        # Estado de animação
        self.current_anim = self.anim_idle
        self.frame = 0
        self.frame_time = 0.0
        self.frame_speed = 0.12   # tempo em segundos por frame -> sensação natural

        # Direção e posição
        self.facing_left = False
        self.image = self.current_anim[0]
        self.rect = self.image.get_rect(center=(400, 300))

        # Movimento
        self.speed = PLAYER_SPEED  # px/s

        # Latido
        self.barking = False
        self.bark_timer = 0
        self.bark_duration = 0.35  # segundos

    def set_animation(self, new_anim):
        """Muda animação com reset de frame para evitar IndexError."""
        if self.current_anim is not new_anim:
            self.current_anim = new_anim
            self.frame = 0
            self.frame_time = 0.0

    def handle_input(self, dt):
        keys = pygame.key.get_pressed()

        dx = 0.0
        dy = 0.0

        # Se está latindo, ainda permitimos movimento -- opcional.
        # Aqui mantemos movimento permitido enquanto latir (como antes).
        if keys[pygame.K_w]:
            dy = -self.speed * dt
        if keys[pygame.K_s]:
            dy = self.speed * dt
        if keys[pygame.K_a]:
            dx = -self.speed * dt
            self.facing_left = True
        if keys[pygame.K_d]:
            dx = self.speed * dt
            self.facing_left = False

        # Aplica movimento
        self.rect.x += int(dx)
        self.rect.y += int(dy)

        # Latido (mantido)
        if keys[pygame.K_SPACE] and not self.barking:
            self.barking = True
            self.bark_timer = pygame.time.get_ticks() / 1000.0  # em segundos
            self.set_animation(self.anim_bark)
            return

        # Se estiver latindo, continuamos com anim_bark até o fim do tempo
        if self.barking:
            return

        # Escolhe animação de movimento ou idle
        if dx != 0.0 or dy != 0.0:
            self.set_animation(self.anim_walk)
        else:
            self.set_animation(self.anim_idle)

    def update(self, dt):
        # dt em segundos (passado do game.loop)
        self.handle_input(dt)

        # Bark timeout
        if self.barking:
            now = pygame.time.get_ticks() / 1000.0
            if now - self.bark_timer >= self.bark_duration:
                self.barking = False
                # volta à idle (ou walk, caso esteja se movendo)
                self.set_animation(self.anim_idle)

        # Atualiza frame (usando frame_speed em segundos)
        self.frame_time += dt
        # segurança: se current_anim for vazio (não deveria), evita crash
        n = len(self.current_anim) if self.current_anim else 1
        if self.frame_time >= self.frame_speed:
            self.frame_time -= self.frame_speed  # subtrai para evitar drift
            self.frame = (self.frame + 1) % n

        # Garante índice válido (caso troca de animação mudou o comprimento)
        if self.frame >= n:
            self.frame = 0

        image = self.current_anim[self.frame]
        if self.facing_left:
            image = pygame.transform.flip(image, True, False)
        self.image = image
