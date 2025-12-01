from math import dist
import pygame
import random

from config import WIDTH, HEIGHT, FPS, BORDER_THICKNESS, TOP_BORDER_THICKNESS
from sprites import Player, DobermannNPC, BlackCatNPC, OrangeCatNPC, Chicken


class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Caramel Adventures")
        self.clock = pygame.time.Clock()

        self.font = pygame.font.SysFont("consolas", 24)
        self.big_font = pygame.font.SysFont("consolas", 64)

        self.all_sprites = pygame.sprite.Group()
        self.chickens = pygame.sprite.Group()

        # Sistema de fases
        self.phase = 1
        self.base_chickens = 4
        self.n_npcs = 5 + 3 + 3

        # Vidas
        self.max_hits = 3
        self.hits_taken = 0

        # PLAYER – posição inicial fixa
        self.spawn_x = WIDTH // 2
        self.spawn_y = HEIGHT // 2
        self.player = Player(self.spawn_x, self.spawn_y, self.all_sprites)

        # Limites do mapa
        self.bounds = pygame.Rect(
            BORDER_THICKNESS,
            TOP_BORDER_THICKNESS,
            WIDTH - 2 * BORDER_THICKNESS,
            HEIGHT - TOP_BORDER_THICKNESS - BORDER_THICKNESS
        )
        self.player.set_bounds(self.bounds)

        # Spawn inicial dos NPCs
        self.spawn_phase_entities()

        # Delay inicial da fase
        self.phase_delay = 3.0
        self.waiting_phase_start = True
        self.phase_timer = self.phase_delay

        self.running = True
        self.game_over = False

    # -----------------------------------------------------------
    def random_pos_away_from_player(self, margin, min_distance=150):
        """Posição aleatória que respeita o mapa e distância mínima do player."""
        px, py = self.spawn_x, self.spawn_y   # Sempre o spawn fixo

        while True:
            left = BORDER_THICKNESS + margin
            right = WIDTH - BORDER_THICKNESS - margin
            top = TOP_BORDER_THICKNESS + margin
            bottom = HEIGHT - BORDER_THICKNESS - margin

            x = random.randint(int(left), int(right))
            y = random.randint(int(top), int(bottom))

            if dist((x, y), (px, py)) >= min_distance:
                return x, y

    # -----------------------------------------------------------
    def respawn_player(self):
        """Reposiciona o jogador no centro da tela no início da fase."""
        self.player.x = self.spawn_x
        self.player.y = self.spawn_y
        self.player.rect.center = (self.spawn_x, self.spawn_y)

    # -----------------------------------------------------------
    def spawn_phase_entities(self):
        self.all_sprites.empty()
        self.chickens.empty()

        # Player sempre primeiro
        self.all_sprites.add(self.player)

        dogs = self.n_npcs // 3
        blacks = self.n_npcs // 3
        oranges = self.n_npcs - dogs - blacks

        # Dobermanns
        for _ in range(dogs):
            x, y = self.random_pos_away_from_player(80)
            npc = DobermannNPC(x, y, self.all_sprites)
            npc.player = self.player

        # Gatos pretos
        for _ in range(blacks):
            x, y = self.random_pos_away_from_player(60)
            BlackCatNPC(x, y, self.all_sprites)

        # Gatos laranjas
        for _ in range(oranges):
            x, y = self.random_pos_away_from_player(60)
            OrangeCatNPC(x, y, self.all_sprites)

        # Galinhas
        for _ in range(self.base_chickens):
            x, y = self.random_pos_away_from_player(40)
            Chicken(x, y, [self.all_sprites, self.chickens])

        # Aplicar bounds
        for s in self.all_sprites:
            if hasattr(s, "set_bounds"):
                s.set_bounds(self.bounds)

    # -----------------------------------------------------------
    def next_phase(self):
        self.phase += 1
        self.n_npcs += 3

        # Sempre respawnar player no início da fase
        self.respawn_player()

        self.spawn_phase_entities()

        self.waiting_phase_start = True
        self.phase_timer = self.phase_delay

    # -----------------------------------------------------------
    def apply_bark_knockback(self):
        if not self.player.is_barking:
            return

        px, py = self.player.x, self.player.y

        for ent in list(self.all_sprites):
            if ent is self.player:
                continue
            if ent in self.chickens:
                continue

            d = dist((px, py), (ent.x, ent.y))
            if d <= 150:
                dx = ent.x - px
                dy = ent.y - py
                mag = max(1, (dx*dx + dy*dy)**0.5)

                new_x = ent.x + (dx / mag) * 150
                new_y = ent.y + (dy / mag) * 150

                bx, by, bw, bh = self.bounds

                new_x = max(bx, min(new_x, bx + bw))
                new_y = max(by, min(new_y, by + bh))

                ent.x = new_x
                ent.y = new_y
                ent.rect.center = (ent.x, ent.y)

    # -----------------------------------------------------------
    def handle_chicken_collisions(self):
        for chicken in list(self.chickens):
            for entity in list(self.all_sprites):
                if entity is chicken:
                    continue
                if entity.rect.colliderect(chicken.rect):
                    if isinstance(entity, Player):
                        entity.score += 1000
                    chicken.kill()
                    break

        if len(self.chickens) == 0:
            self.next_phase()

    # -----------------------------------------------------------
    def handle_player_entity_collisions(self):
        if self.waiting_phase_start:
            return

        for entity in self.all_sprites:
            if entity is self.player:
                continue
            if entity in self.chickens:
                continue

            if entity.rect.colliderect(self.player.rect):
                if not self.player.is_hurt:
                    self.player.hurt()
                    self.hits_taken += 1

                if self.hits_taken >= self.max_hits:
                    self.game_over = True
                return

    # -----------------------------------------------------------
    def draw_score(self):
        txt = f"{self.player.score:06d}  |  Fase {self.phase}"
        surf = self.font.render(txt, True, (255, 255, 255))
        self.screen.blit(surf, (12, 6))

    # -----------------------------------------------------------
    def show_game_over(self):
        text = self.big_font.render("GAME OVER", True, (255, 80, 80))
        rect = text.get_rect(center=(WIDTH//2, HEIGHT//2))
        self.screen.blit(text, rect)
        pygame.display.flip()
        pygame.time.wait(2500)

    # -----------------------------------------------------------
    def run(self):
        while self.running:

            dt = self.clock.tick(FPS) / 1000

            if self.game_over:
                self.show_game_over()
                self.running = False
                continue

            # Eventos
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                if not self.waiting_phase_start:
                    if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                        self.player.bark()

            # -----------------------------
            # TELA DE ESPERA DA FASE
            # -----------------------------
            if self.waiting_phase_start:
                self.phase_timer -= dt

                # Render da tela com entidades paradas
                self.screen.fill((30, 30, 30))
                pygame.draw.rect(self.screen, (255,255,255), self.bounds, 2)

                # Desenhar entidades já spawnadas (paradas)
                for s in self.all_sprites:
                    self.screen.blit(s.image, s.rect)

                msg = self.font.render(
                    f"Fase {self.phase} começa em {int(self.phase_timer)+1}",
                    True, (255,255,0)
                )
                rect = msg.get_rect(center=(WIDTH//2, HEIGHT//2))
                self.screen.blit(msg, rect)

                self.draw_score()
                pygame.display.flip()

                if self.phase_timer <= 0:
                    self.waiting_phase_start = False
                continue

            # -----------------------------
            # JOGO NORMAL
            # -----------------------------
            self.apply_bark_knockback()
            self.all_sprites.update(dt)
            self.handle_chicken_collisions()
            self.handle_player_entity_collisions()

            # Render
            self.screen.fill((30, 30, 30))
            pygame.draw.rect(self.screen, (255,255,255), self.bounds, 2)
            self.draw_score()

            self.all_sprites.draw(self.screen)
            pygame.display.flip()

        pygame.quit()
