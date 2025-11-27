import pygame
from config import WIDTH, HEIGHT, FPS
from sprites import Player

class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Caramel Adventures")

        self.clock = pygame.time.Clock()

        self.all_sprites = pygame.sprite.Group()

        self.player = Player(self)
        self.all_sprites.add(self.player)

        self.running = True

    def run(self):
        while self.running:
            dt = self.clock.tick(FPS) / 1000.0   # dt em segundos
            self.events()
            self.update(dt)
            self.draw()

    def events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

    def update(self, dt):
        self.all_sprites.update(dt)

    def draw(self):
        self.screen.fill((30, 30, 30))
        self.all_sprites.draw(self.screen)
        pygame.display.flip()
