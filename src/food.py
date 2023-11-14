"""The food Python file
"""
import entity
import settings
import random as r


class Food(entity.Entity):

    """the Food class

    Attributes:
        screen (surface): the Pygame window
    """

    def __init__(self, w) -> None:
        """The initializer method

        Args:
            w (surface): the Pygame window
        """

        self.energy = r.uniform(0, 3)
        self.screen = w
        super().__init__(w=self.screen)

    def update(self, sdl, h, p, f, e, dt) -> None:
        """The update method that runs every frame to update this entities
        behaviours, positions, rotations

        Args:
            sdl (bool): show_debug_lines shows where the entity will be heading
            h (list): the hunter list
            p (list): the prey list
            f (list): the food list
            e (list): the egg list
            dt (float): Description
        """
        # chance = 0.0001 * (len(p) - len(h))
        chance = (1 / (len(p) + len(e))) / len(f)

        if r.random() < chance:
            f.append(Food(w=self.screen))
        super().update(dt=dt, color=settings.FOOD_COLOR, size=2 + self.energy)
