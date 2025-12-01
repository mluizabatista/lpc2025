import pygame 
import random
from math import dist

from config import WIDTH, HEIGHT, FPS, BORDER_THICKNESS, TOP_BORDER_THICKNESS
from sprites import Player, DobermannNPC, BlackCatNPC, OrangeCatNPC, Chicken


class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Caramel Adventures")
        self.clock = pygame.time.Clock()

        self.font = pygame.font.SysFont("consolas", 24)

        self.all_sprites = pygame.sprite.Group()
        self.chickens = pygame.sprite.Group()

        # PLAYER
        px = WIDTH // 2
        py = HEIGHT // 2
        self.player = Player(px, py, self.all_sprites)

        self.bounds = pygame.Rect(
            BORDER_THICKNESS,
            TOP_BORDER_THICKNESS,
            WIDTH - 2 * BORDER_THICKNESS,
            HEIGHT - TOP_BORDER_THICKNESS - BORDER_THICKNESS
        )
        self.player.set_bounds(self.bounds)

        self.spawn_npcs()
        self.spawn_chickens()

        for s in list(self.all_sprites):
            if hasattr(s, "set_bounds"):
                s.set_bounds(self.bounds)

        self.running = True

    # ============================================================
    # POSIÇÃO INICIAL LONGE DO PLAYER
    # ============================================================
    def random_pos_away_from_player(self, margin, min_distance=100):
        px, py = self.player.x, self.player.y

        while True:
            left = BORDER_THICKNESS + margin
            right = WIDTH - BORDER_THICKNESS - margin
            top = TOP_BORDER_THICKNESS + margin
            bottom = HEIGHT - BORDER_THICKNESS - margin

            x = random.randint(int(left), int(max(left + 1, right)))
            y = random.randint(int(top), int(max(top + 1, bottom)))

            if dist((x, y), (px, py)) >= min_distance:
                return x, y

    # ============================================================
    # NPCs
    # ============================================================
    def spawn_npcs(self):
        for _ in range(5):
            x, y = self.random_pos_away_from_player(80, 50)
            npc = DobermannNPC(x, y, self.all_sprites)
            npc.player = self.player

        for _ in range(3):
            x, y = self.random_pos_away_from_player(60, 50)
            BlackCatNPC(x, y, self.all_sprites)

        for _ in range(3):
            x, y = self.random_pos_away_from_player(60, 50)
            OrangeCatNPC(x, y, self.all_sprites)

    # ============================================================
    # GALINHAS
    # ============================================================
    def spawn_chickens(self):
        for _ in range(4):
            x, y = self.random_pos_away_from_player(40, 50)
            Chicken(x, y, [self.all_sprites, self.chickens])

    # ============================================================
    # LATIDO → EMPURRÃO INSTANTÂNEO DE 150px
    # ============================================================
    def apply_bark_knockback(self):
        """Empurra entidades em raio de 150px, instantaneamente, 150px para longe."""
        if not self.player.is_barking:
            return

        px, py = self.player.x, self.player.y

        for ent in list(self.all_sprites):
            if ent is self.player:
                continue
            if ent in self.chickens:
                continue  # frango não é empurrado

            d = dist((px, py), (ent.x, ent.y))

            if d <= 150:
                dx = ent.x - px
                dy = ent.y - py
                mag = max(1, (dx*dx + dy*dy)**0.5)

                # 150px na direção oposta ao jogador
                new_x = ent.x + (dx / mag) * 150
                new_y = ent.y + (dy / mag) * 150

                # CLAMPA DENTRO DAS BORDAS
                bx, by, bw, bh = self.bounds
                new_x = max(bx, min(new_x, bx + bw))
                new_y = max(by, min(new_y, by + bh))

                ent.x = new_x
                ent.y = new_y
                ent.rect.center = (ent.x, ent.y)

    # ============================================================
    # COLISÃO COM GALINHAS
    # ============================================================
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

    # ============================================================
    # PLAYER vs OUTRAS ENTIDADES
    # ============================================================
    def handle_player_entity_collisions(self):
        for entity in list(self.all_sprites):
            if entity is self.player:
                continue
            if entity in self.chickens:
                continue

            if entity.rect.colliderect(self.player.rect):
                self.player.hurt()

    # ============================================================
    # HUD
    # ============================================================
    def draw_score(self):
        txt = f"{self.player.score:06d}"
        surf = self.font.render(txt, True, (255, 255, 255))
        self.screen.blit(surf, (12, 6))

    # ============================================================
    # GAME LOOP
    # ============================================================
    def run(self):
        while self.running:
            dt = self.clock.tick(FPS) / 1000

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        self.player.bark()

            self.apply_bark_knockback()

            self.all_sprites.update(dt)

            self.handle_chicken_collisions()
            self.handle_player_entity_collisions()

            self.screen.fill((30, 30, 30))
            pygame.draw.rect(self.screen, (255,255,255), self.bounds, 2)
            self.draw_score()
            self.all_sprites.draw(self.screen)
            pygame.display.flip()

        pygame.quit()
