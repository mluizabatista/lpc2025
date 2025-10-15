import sys
import math
import pygame

# Luiza: Constants

WIDTH, HEIGHT = 1000, 800
FPS = 60
BACKGROUND_COLOR = (20, 20, 30)
TRIANGLE_COLOR_1 = (255, 100, 100)
TRIANGLE_COLOR_2 = (100, 180, 255)
TRIANGLE_SIZE = 50
ROTATION_SPEED = 3
MOVEMENT_SPEED = 5
BRAKE_MODE = 0 # 0 = continuous, 1 = momentary

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

# Luiza: Triangle class 

class Triangle:
    def __init__(self, position, color, controls):
        self.position = [float(position[0]), float(position[1])]
        self.angle = 0.0
        self.color = color
        self.moving = False
        self.controls = controls

        self.local_points = [
            (0.0, -TRIANGLE_SIZE),
            (-TRIANGLE_SIZE / 2.0, TRIANGLE_SIZE / 2.0),
            (TRIANGLE_SIZE / 2.0, TRIANGLE_SIZE / 2.0),
        ]

    def get_transformed_points(self):
        transformed = []
        for point in self.local_points:
            rotated = rotate_point(point, self.angle)
            screen_point = (
                rotated[0] + self.position[0],
                rotated[1] + self.position[1],
            )
            transformed.append(screen_point)
        return transformed

    def rotate(self, direction):
        if direction == "left":
            self.angle = (self.angle - ROTATION_SPEED) % 360.0
        elif direction == "right":
            self.angle = (self.angle + ROTATION_SPEED) % 360.0

    def move(self, direction=None):
        angle_radians = math.radians(self.angle)
        dx = math.sin(angle_radians) * MOVEMENT_SPEED
        dy = -math.cos(angle_radians) * MOVEMENT_SPEED

        if BRAKE_MODE == 0:
            if direction == "forward":
                self.moving = True
            elif direction == "stop":
                self.moving = False

            if self.moving:
                self.position[0] += dx
                self.position[1] += dy
        else:
            if direction == "forward":
                self.position[0] += dx
                self.position[1] += dy

# Ranielly: Faz o triângulo atravessar as bordas e reaparecer do outro lado (wrap around)
    def wrap_around_screen(self):
        if self.position[0] < 0:
            self.position[0] = WIDTH
        elif self.position[0] > WIDTH:
            self.position[0] = 0

        if self.position[1] < 0:
            self.position[1] = HEIGHT
        elif self.position[1] > HEIGHT:
            self.position[1] = 0


    def draw(self, surface):
        pygame.draw.polygon(surface, self.color, self.get_transformed_points())

# Luiza: Main function

def game():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Dois Jogadores — Triângulos")
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

    player1 = Triangle((WIDTH * 0.3, HEIGHT / 2), TRIANGLE_COLOR_1, controls_p1)
    player2 = Triangle((WIDTH * 0.7, HEIGHT / 2), TRIANGLE_COLOR_2, controls_p2)

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
