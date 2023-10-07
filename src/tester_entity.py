import src.entity
import pygame
import random


class TesterEntity(src.entity.Entity):
    def __init__(self, window) -> None:
        super().__init__(window)
        self.pos = pygame.Vector2(random.randint(0, 800), random.randint(0, 600))

    def update(self) -> None:
        return super().update("yellow", 4)
