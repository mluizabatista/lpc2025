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

    # --- ADICIONADO: Configuração da fonte para o placar ---
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

        if keys[player1.controls["left"]]: player1.rotate("left")
        if keys[player1.controls["right"]]: player1.rotate("right")
        if keys[player1.controls["forward"]]: player1.move("forward")
        if keys[player1.controls["back"]]: player1.move("stop")
        
        if keys[player2.controls["left"]]: player2.rotate("left")
        if keys[player2.controls["right"]]: player2.rotate("right")
        if keys[player2.controls["forward"]]: player2.move("forward")
        if keys[player2.controls["back"]]: player2.move("stop")

        player1.move()
        player2.move()

        player1.wrap_around_screen()
        player2.wrap_around_screen()

        player1.draw(screen)
        player2.draw(screen)

        for projectile in projectiles[:]:
            projectile.move()
            projectile.draw(screen)
            if projectile.is_expired():
                # Libera o slot do projétil ativo do jogador
                if player1.active_projectile == projectile:
                    player1.active_projectile = None
                if player2.active_projectile == projectile:
                    player2.active_projectile = None
                projectiles.remove(projectile)
        
        # --- LÓGICA DE COLISÃO E PONTUAÇÃO ATUALIZADA ---
        for proj in projectiles[:]:
            proj_rect = pygame.Rect(proj.x - BALL_RADIUS, proj.y - BALL_RADIUS, BALL_RADIUS * 2, BALL_RADIUS * 2)

            # Define um retângulo de colisão para os jogadores
            # Usamos o tamanho TRIANGLE_SIZE para criar uma caixa de colisão aproximada
            p1_rect = pygame.Rect(player1.position[0] - TRIANGLE_SIZE, player1.position[1] - TRIANGLE_SIZE, TRIANGLE_SIZE * 2, TRIANGLE_SIZE * 2)
            p2_rect = pygame.Rect(player2.position[0] - TRIANGLE_SIZE, player2.position[1] - TRIANGLE_SIZE, TRIANGLE_SIZE * 2, TRIANGLE_SIZE * 2)
            
            # Verifica colisão com player 1
            if proj.shooter != player1 and p1_rect.colliderect(proj_rect):
                proj.shooter.score += 1
                projectiles.remove(proj)
                # Libera o slot de tiro de quem foi atingido
                if player1.active_projectile == proj: player1.active_projectile = None
                if player2.active_projectile == proj: player2.active_projectile = None
                continue # Pula para o próximo projétil
            
            # Verifica colisão com player 2
            if proj.shooter != player2 and p2_rect.colliderect(proj_rect):
                proj.shooter.score += 1
                projectiles.remove(proj)
                # Libera o slot de tiro de quem foi atingido
                if player1.active_projectile == proj: player1.active_projectile = None
                if player2.active_projectile == proj: player2.active_projectile = None

        # --- ADICIONADO: Desenha o placar na tela ---
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