from core.config import WIDTH, HEIGHT
from core.triangle import Triangle

# Ranielly: Faz o triângulo atravessar as bordas e reaparecer do outro lado (wrap around)

class Ship(Triangle):

    def wrap_around_screen(self):
        if self.position[0] < 0:
            self.position[0] = WIDTH
        elif self.position[0] > WIDTH:
            self.position[0] = 0

        if self.position[1] < 0:
            self.position[1] = HEIGHT
        elif self.position[1] > HEIGHT:
            self.position[1] = 0
