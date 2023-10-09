import random

import pygame

import src.entity
import src.settings


class TesterEntity(src.entity.Entity):
    def __init__(self, window) -> None:
        super().__init__(window)

    def update(self, dt, *kwargs) -> None:
        return super().update(
            src.settings.test_entity_color, src.settings.test_entity_size
        )
