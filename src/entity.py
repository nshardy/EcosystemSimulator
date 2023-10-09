import random
import pygame


class Entity:
    def __init__(self, window) -> None:
        self.window = window
        self.pos = pygame.Vector2(
            random.randint(0, window.get_width()),
            random.randint(0, window.get_height()),
        )

    def update(self, color, radius) -> None:
        pygame.draw.circle(self.window, color, self.pos, radius)
