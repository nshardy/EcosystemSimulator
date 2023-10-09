import random

import pygame

import src.entity
import src.settings


class Hunter(src.entity.Entity):
    def __init__(self, window) -> None:
        super().__init__(window)

    def update(self, dt, *kwargs) -> None:
        return super().update(src.settings.hunter_color, src.settings.hunter_size)
