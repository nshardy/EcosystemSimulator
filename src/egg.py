"""The egg Python file
"""
from pygame import Surface, Vector2
import settings
import random as r
from entity import Entity


class Egg(Entity):

    """Summary

    Attributes:
        egg_list (list): the egg list
        has_hatched (bool): if the egg has hatched
        hunter_list (list): the hunter list
        prey_list (list): the prey list
    """

    def __init__(self, w, position, p_or_h, mothers_traits=None, fathers_traits=None) -> None:
        """The initializer method

        Args:
            w (surface): the Pygame window
            mother (Entity): the mother Entity
            position (Vector2): the position of the mother
            p_or_h (string): 'p' if the egg is for prey,
                             'h' if the egg is for hunters
        """

        self.screen: Surface = w
        self.mother_traits = mothers_traits
        self.father_traits = fathers_traits

        self.p_or_h: str = p_or_h
        self.time_until_hatch: float = r.randrange(5, 10)
        self.hatch_timer: float = 0
        self.has_hatched: bool = False

        self.prey_list: list
        self.hunter_list: list
        self.egg_list: list

        super().__init__(w=self.screen)
        self.pos: Vector2 = position

    def update(self, sdl, h, p, f, e, dt) -> None:
        """Updates the egg 1 time per frame

        Args:
            sdl (bool): show_debug_lines
            h (list): the list of hunters
            p (list): the list of prey
            f (list): the list of food
            e (list): the list of eggs
            dt (float): deltaTime is the time inbetween frames
        """

        self.hatch_timer += dt
        self.prey_list = p
        self.egg_list = e
        self.hunter_list = h
        self.check_hatch()

        super().update(dt=dt, color=settings.EGG_COLOR, size=settings.EGG_SIZE)

    def check_hatch(self) -> None:
        """Used to check to see if the egg should hatch

        Returns:
            None
        """

        if self.hatch_timer < self.time_until_hatch and not self.has_hatched:
            return

        self.has_hatched = True

        if self.p_or_h == "p":
            from prey import Prey

            child = Prey(
                w=self.screen,
            )
            child.pos = self.pos
            self.prey_list.append(child)
            self.egg_list.remove(self)
            del self

        elif self.p_or_h == "h":
            from hunter import Hunter

            child = Hunter(
                w=self.screen, mother=self.mother_traits, father=self.father_traits
            )
            child.pos = self.pos
            self.hunter_list.append(child)
            self.egg_list.remove(self)
            del self
