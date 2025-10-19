# core/core.py

import sys
import math
import pygame

from core.config import *
from ship.ship import Ship

def game():
    pygame.init()

    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Combat")
    clock = pygame.time.Clock()

    try:
        score_font = pygame.font.Font(None, 50)
    except pygame.error:
        score_font = pygame.font.Font(pygame.font.get_default_font(), 50)

    controls_p1 = {"forward": pygame.K_w, "back": pygame.K_s, "left": pygame.K_a, "right": pygame.K_d}
    controls_p2 = {"forward": pygame.K_UP, "back": pygame.K_DOWN, "left": pygame.K_LEFT, "right": pygame.K_RIGHT}

    player1 = Ship((WIDTH * 0.3, HEIGHT / 2), TRIANGLE_COLOR_1, controls_p1)
    player2 = Ship((WIDTH * 0.7, HEIGHT / 2), TRIANGLE_COLOR_2, controls_p2)

    projectiles = []
    running = True

    while running:
        clock.tick(FPS)
        screen.fill(BACKGROUND_COLOR)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    player1.shoot(projectiles)
                elif event.key == pygame.K_RETURN:
                    player2.shoot(projectiles)

        keys = pygame.key.get_pressed()

        # --- MODIFICADO: Controles de aceleração e freio REMOVIDOS ---
        # As naves agora se movem constantemente, então só precisamos ler as teclas de rotação.
        
        # Controle do Jogador 1 (apenas rotação)
        if not player1.is_disabled:
            if keys[player1.controls["left"]]: player1.rotate("left")
            if keys[player1.controls["right"]]: player1.rotate("right")
        
        # Controle do Jogador 2 (apenas rotação)
        if not player2.is_disabled:
            if keys[player2.controls["left"]]: player2.rotate("left")
            if keys[player2.controls["right"]]: player2.rotate("right")

        # A função update chama o novo método move(), que aplica o movimento constante.
        player1.update()
        player2.update()

        player1.draw(screen)
        player2.draw(screen)

        for projectile in projectiles[:]:
            projectile.move()
            projectile.draw(screen)
            if projectile.is_expired():
                if player1.active_projectile == projectile:
                    player1.active_projectile = None
                if player2.active_projectile == projectile:
                    player2.active_projectile = None
                projectiles.remove(projectile)
        
        # Lógica de colisão e pontuação (permanece a mesma)
        for proj in projectiles[:]:
            proj_rect = pygame.Rect(proj.x - BALL_RADIUS, proj.y - BALL_RADIUS, BALL_RADIUS * 2, BALL_RADIUS * 2)
            p1_rect = pygame.Rect(player1.position[0] - TRIANGLE_SIZE, player1.position[1] - TRIANGLE_SIZE, TRIANGLE_SIZE * 2, TRIANGLE_SIZE * 2)
            p2_rect = pygame.Rect(player2.position[0] - TRIANGLE_SIZE, player2.position[1] - TRIANGLE_SIZE, TRIANGLE_SIZE * 2, TRIANGLE_SIZE * 2)
            
            if proj.shooter != player1 and p1_rect.colliderect(proj_rect):
                proj.shooter.score += 1
                player1.take_damage()
                projectiles.remove(proj)
                if player1.active_projectile == proj: player1.active_projectile = None
                if player2.active_projectile == proj: player2.active_projectile = None
                continue 
            
            if proj.shooter != player2 and p2_rect.colliderect(proj_rect):
                proj.shooter.score += 1
                player2.take_damage()
                projectiles.remove(proj)
                if player1.active_projectile == proj: player1.active_projectile = None
                if player2.active_projectile == proj: player2.active_projectile = None

        # Desenha o placar
        p1_score_text = score_font.render(str(player1.score), True, player1.color)
        p2_score_text = score_font.render(str(player2.score), True, player2.color)
        screen.blit(p1_score_text, (30, 20))
        screen.blit(p2_score_text, (WIDTH - p2_score_text.get_width() - 30, 20))

        player1.draw_clouds(screen)
        
        pygame.display.flip()

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    game()