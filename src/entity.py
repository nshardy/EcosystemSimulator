import pygame


class Entity:
    def __init__(self, window) -> None:
        self.window = window
        self.pos = pygame.Vector2()

    def update(self, color, radius) -> None:
        pygame.draw.circle(self.window, color, self.pos, radius)
