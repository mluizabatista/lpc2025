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

    running = True
    while running:
        clock.tick(FPS)
        screen.fill(BACKGROUND_COLOR)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

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

        pygame.display.flip()

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    game()
