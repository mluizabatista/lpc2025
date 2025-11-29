import pygame
from config import WIDTH, HEIGHT, FPS, BORDER_THICKNESS, TOP_BORDER_THICKNESS
from sprites import Player, DobermannNPC

class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Caramel Adventures")
        self.clock = pygame.time.Clock()

        self.all_sprites = pygame.sprite.Group()

        self.player = Player(self)
        self.all_sprites.add(self.player)

        self.dog_npc = DobermannNPC(self)
        self.all_sprites.add(self.dog_npc)

        self.running = True

    def draw_border(self):

        rect = pygame.Rect(
            BORDER_THICKNESS,               
            TOP_BORDER_THICKNESS,          
            WIDTH - 2 * BORDER_THICKNESS, 
            HEIGHT - TOP_BORDER_THICKNESS - BORDER_THICKNESS 
        )

        pygame.draw.rect(self.screen, (255, 255, 255), rect, width=2)

    def run(self):
        while self.running:
            dt = self.clock.tick(FPS) / 1000.0  
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

            self.all_sprites.update(dt)

            self.screen.fill((30, 30, 30))
            self.draw_border()
            self.all_sprites.draw(self.screen)
            pygame.display.flip()

        pygame.quit()