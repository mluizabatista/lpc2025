import sys
import pygame
import time

from core.config import *
from ship.ship import Ship  

def create_players(game_type, score_p1=0, score_p2=0):

    if game_type == "ship":

        from ship.ship import Ship as PlayerClass
        pos_p1 = (WIDTH * 0.3, HEIGHT / 2)
        pos_p2 = (WIDTH * 0.7, HEIGHT / 2)

    elif game_type == "tank":

        from tank.tank import Tank as PlayerClass
        pos_p1 = (WIDTH * 0.15, HEIGHT / 2)
        pos_p2 = (WIDTH * 0.85, HEIGHT / 2)

    controls_p1 = {
        "forward": pygame.K_w, 
        "back": pygame.K_s, 
        "left": pygame.K_a, 
        "right": pygame.K_d
    }

    controls_p2 = {
        "forward": pygame.K_UP, 
        "back": pygame.K_DOWN, 
        "left": pygame.K_LEFT, 
        "right": pygame.K_RIGHT
    }

    player1 = PlayerClass(pos_p1, TRIANGLE_COLOR_1, controls_p1)
    player2 = PlayerClass(pos_p2, TRIANGLE_COLOR_2, controls_p2)

    player1.score = score_p1
    player2.score = score_p2

    return player1, player2

def game():

    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Combat")
    clock = pygame.time.Clock()

    try:
        score_font = pygame.font.Font(None, 50)

    except pygame.error:
        score_font = pygame.font.Font(pygame.font.get_default_font(), 50)

    current_game = "ship"
    player1, player2 = create_players(current_game)
    projectiles = []

    running = True

    while running:

        clock.tick(FPS)

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                running = False

            elif event.type == pygame.KEYDOWN:

                if event.key == pygame.K_ESCAPE:
                   
                    current_game = "tank" if current_game == "ship" else "ship"
                    score_p1, score_p2 = player1.score, player2.score
                    player1, player2 = create_players(current_game, score_p1, score_p2)
                    projectiles = []

                elif event.key == pygame.K_SPACE:
                    player1.shoot(projectiles)

                elif event.key == pygame.K_RETURN:
                    player2.shoot(projectiles)

        keys = pygame.key.get_pressed()

        if not player1.is_disabled:

            if keys[player1.controls["left"]]:
                player1.rotate("left")

            if keys[player1.controls["right"]]:
                player1.rotate("right")

        if not player2.is_disabled:

            if keys[player2.controls["left"]]:
                player2.rotate("left")

            if keys[player2.controls["right"]]:
                player2.rotate("right")

        player1.update()
        player2.update()

        background_color = getattr(player1, "BACKGROUND_COLOR", (0, 0, 0))
        screen.fill(background_color)

        player1.draw(screen)
        player2.draw(screen)

        if hasattr(player1, "draw_ambience"):
            player1.draw_ambience(screen)

        for projectile in projectiles[:]:

            projectile.move()
            projectile.draw(screen)

            if projectile.is_expired():

                if player1.active_projectile == projectile:
                    player1.active_projectile = None

                if player2.active_projectile == projectile:
                    player2.active_projectile = None

                projectiles.remove(projectile)

        for proj in projectiles[:]:

            proj_rect = pygame.Rect(
                proj.x - BALL_RADIUS, proj.y - BALL_RADIUS,
                BALL_RADIUS * 2, BALL_RADIUS * 2
            )
            p1_rect = pygame.Rect(
                player1.position[0] - TRIANGLE_SIZE, player1.position[1] - TRIANGLE_SIZE,
                TRIANGLE_SIZE * 2, TRIANGLE_SIZE * 2
            )
            p2_rect = pygame.Rect(
                player2.position[0] - TRIANGLE_SIZE, player2.position[1] - TRIANGLE_SIZE,
                TRIANGLE_SIZE * 2, TRIANGLE_SIZE * 2
            )

            if proj.shooter != player1 and p1_rect.colliderect(proj_rect):

                proj.shooter.score += 1
                player1.take_damage()
                projectiles.remove(proj)
                continue

            if proj.shooter != player2 and p2_rect.colliderect(proj_rect):

                proj.shooter.score += 1
                player2.take_damage()
                projectiles.remove(proj)

        p1_score_text = score_font.render(str(player1.score), True, player1.color)
        p2_score_text = score_font.render(str(player2.score), True, player2.color)
        screen.blit(p1_score_text, (30, 20))
        screen.blit(p2_score_text, (WIDTH - p2_score_text.get_width() - 30, 20))

        pygame.display.flip()

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    game()
