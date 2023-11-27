"""Summary
"""
import pygame
import random as r
import settings
import enum


class ai_state(enum.Enum):

    """Summary

    Attributes:
        looking_for_mate (int): Enum state for looking_for_mate
        looking_for_food (int): Enum state for looking_for_food
        food_state (int): Enum state for food_state
        running_from_hunter (int): Enum state for running_from_hunter
    """

    food_state = 0
    running_from_hunter = 1
    looking_for_food = 2
    looking_for_mate = 3


class Entity:

    """Summary

    Attributes:
        ai_state (TYPE): Description
        pos (TYPE): Description
        screen (TYPE): Description
    """

    def __init__(self, w) -> None:
        """Summary

        Args:
            w (TYPE): Description
        """
        self.screen = w
        self.pos = pygame.math.Vector2(
            r.randint(
                settings.ENTITY_WINDOW_BORDER,
                w.get_size()[0] - settings.ENTITY_WINDOW_BORDER,
            ),
            r.randint(
                settings.ENTITY_WINDOW_BORDER,
                w.get_size()[1] - settings.PIXEL_BORDER - settings.ENTITY_WINDOW_BORDER,
            ),
        )
        self.ai_state = ai_state(value=0)

    def update(self, dt, color, size) -> None:
        """Summary

        Args:
            dt (TYPE): Description
            color (TYPE): Description
            size (TYPE): Description
        """
        pygame.draw.circle(self.screen, color, self.pos, size)
