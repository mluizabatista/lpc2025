import pygame
import random
from config import WIDTH, HEIGHT, FPS, BORDER_THICKNESS, TOP_BORDER_THICKNESS
from sprites import Player, DobermannNPC, BlackCatNPC, OrangeCatNPC, ChickenNPC

class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Caramel Adventures")
        self.clock = pygame.time.Clock()

        # Grupo único para desenhar/atualizar todas as sprites
        self.all_sprites = pygame.sprite.Group()

        # Grupo adicional para frangos (para detectar remoção facilmente)
        self.chickens = pygame.sprite.Group()

        # ----- PLAYER -----
        player_x = WIDTH // 2
        player_y = HEIGHT // 2
        self.player = Player(player_x, player_y, self.all_sprites)

        # definir limites de mapa
        self.bounds = pygame.Rect(
            BORDER_THICKNESS,
            TOP_BORDER_THICKNESS,
            WIDTH - 2 * BORDER_THICKNESS,
            HEIGHT - TOP_BORDER_THICKNESS - BORDER_THICKNESS
        )
        self.player.set_bounds(self.bounds)

        # ----- NPCs -----
        self.spawn_npcs()
        self.spawn_chickens()

        # aplicar limites a todos
        for sprite in self.all_sprites:
            if hasattr(sprite, "set_bounds"):
                sprite.set_bounds(self.bounds)

        self.running = True

    def random_pos(self, margin=60):
        left = BORDER_THICKNESS + margin
        right = WIDTH - BORDER_THICKNESS - margin
        top = TOP_BORDER_THICKNESS + margin
        bottom = HEIGHT - BORDER_THICKNESS - margin

        x = random.randint(int(left), int(max(left + 1, right)))
        y = random.randint(int(top), int(max(top + 1, bottom)))
        return x, y

    def spawn_npcs(self):
        # Dobermanns
        for _ in range(5):
            x, y = self.random_pos(80)
            npc = DobermannNPC(x, y, self.all_sprites)
            npc.player = self.player

        # Black cats
        for _ in range(3):
            x, y = self.random_pos(60)
            BlackCatNPC(x, y, self.all_sprites)

        # Orange cats
        for _ in range(3):
            x, y = self.random_pos(60)
            OrangeCatNPC(x, y, self.all_sprites)

    def spawn_chickens(self):
        for _ in range(4):
            x, y = self.random_pos(40)
            chicken = ChickenNPC(x, y, [self.all_sprites, self.chickens])

    def draw_border(self):
        pygame.draw.rect(self.screen, (255, 255, 255), self.bounds, width=2)

    def handle_chicken_collisions(self):
        # qualquer entidade colide com frango => frango some
        for chicken in list(self.chickens):
            collided = pygame.sprite.spritecollide(
                chicken,
                self.all_sprites,
                False,
                pygame.sprite.collide_mask
            )
            for entity in collided:
                if entity is not chicken:
                    chicken.kill()

    def run(self):
        while self.running:
            dt = self.clock.tick(FPS) / 1000.0

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

            self.all_sprites.update(dt)

            self.handle_chicken_collisions()

            self.screen.fill((30, 30, 30))
            self.draw_border()
            self.all_sprites.draw(self.screen)
            pygame.display.flip()

        pygame.quit()
