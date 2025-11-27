import pygame
import os

class SoundManager:
    def __init__(self):
        try:
            pygame.mixer.init()
        except Exception:
            pass
        self.bark = None

    def play_bark(self):
        if self.bark:
            self.bark.play()
