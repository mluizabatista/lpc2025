import sys
import math
import pygame

from core.config import *

from ship.ship import Ship
from core.triangle import Triangle


# Luiza: Rotating functions
def rotate_point(point, angle_degrees):

    angle_radians = math.radians(angle_degrees)
    x, y = point

    cos_theta = math.cos(angle_radians)
    sin_theta = math.sin(angle_radians)

    return (
        x * cos_theta - y * sin_theta,
        x * sin_theta + y * cos_theta,
    )


# Luiza: Main function
def game():

    pygame.init()

    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Combat")
    clock = pygame.time.Clock()

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

    # Luiza: Players entity (triangle) initialization
    player1 = Ship((WIDTH * 0.3, HEIGHT / 2), TRIANGLE_COLOR_1, controls_p1)
    player2 = Ship((WIDTH * 0.7, HEIGHT / 2), TRIANGLE_COLOR_2, controls_p2)

    # Luiza: Main loop
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

        # Luiza: Player's control definition
        if keys[player1.controls["left"]]:
            player1.rotate("left")
        if keys[player1.controls["right"]]:
            player1.rotate("right")
        if keys[player1.controls["forward"]]:
            player1.move("forward")
        if keys[player1.controls["back"]]:
            player1.move("stop")

        if keys[player2.controls["left"]]:
            player2.rotate("left")
        if keys[player2.controls["right"]]:
            player2.rotate("right")
        if keys[player2.controls["forward"]]:
            player2.move("forward")
        if keys[player2.controls["back"]]:
            player2.move("stop")

        player1.move()
        player2.move()

        # Ranielly: garante que atravessem as bordas da tela
        player1.wrap_around_screen()
        player2.wrap_around_screen()

        player1.draw(screen)
        player2.draw(screen)

        # Atualiza e desenha os projéteis
        for projectile in projectiles[:]:
            projectile.move()
            projectile.draw(screen)

            if projectile.is_expired():
                if player1.active_projectile == projectile:
                    player1.active_projectile = None
                if player2.active_projectile == projectile:
                    player2.active_projectile = None
                projectiles.remove(projectile)

        # --- Colisão dos projéteis com os triângulos ---
        for projectile in projectiles[:]:
            # Pega a posição do projétil
            px, py = projectile.x, projectile.y

            # Define um pequeno raio de colisão (ajuste se necessário)
            projectile_radius = 5  

            # Função auxiliar para detectar colisão com o triângulo
            def check_collision(projectile_x, projectile_y, triangle):
                tx, ty = triangle.position
                dx = projectile_x - tx
                dy = projectile_y - ty
                distance = math.hypot(dx, dy)
                triangle_size = getattr(triangle, "size", 25)
                return distance < triangle_size + projectile_radius

            # Se colidir com o player 1 ou player 2
            if check_collision(px, py, player1) or check_collision(px, py, player2):

                # Ignora colisão com o próprio atirador
                if hasattr(projectile, "shooter") and projectile.shooter == player1 and check_collision(px, py, player1):
                    continue
                if hasattr(projectile, "shooter") and projectile.shooter == player2 and check_collision(px, py, player2):
                    continue

                # Remove o projétil da lista
                if projectile in projectiles:
                    projectiles.remove(projectile)

                # Libera o slot do projétil ativo do jogador
                if player1.active_projectile == projectile:
                    player1.active_projectile = None
                if player2.active_projectile == projectile:
                    player2.active_projectile = None

        pygame.display.flip()

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    game()
