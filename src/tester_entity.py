import random

import pygame

import src.entity as entity
import src.settings as settings


class TesterEntity(entity.Entity):
    def __init__(self, window) -> None:
        super().__init__(window)

    def update(self, dt, test_entities, hunters) -> None:
        return super().update(settings.test_entity_color, settings.test_entity_size)

    def update_ai_state():
        pass

    def update_ai_behaviour():
        pass
