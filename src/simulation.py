"""the Simulation python file
"""
from food import Food
from prey import Prey
from hunter import Hunter
import random as r
import settings


class Simulation:

    """the Simulation python file

    Attributes:
        screen (surface): the Pygame Window
    """

    def __init__(self, w) -> None:
        """Initialize the simulation

        Args:
            w (surface): the Pygame window
        """
        self.prey: list = []
        self.hunters: list = []
        self.foods: list = []
        self.eggs: list = []

        self.screen = w

        self.start_prey_amount: int = r.randint(2, 5 * 3)
        self.start_hunter_amount: int = r.randint(2, 15)
        self.start_food_amount: int = r.randint(50, 100)
        self.pause_simulation: bool = False
        self.show_debug_lines: bool = bool

        for _ in range(self.start_prey_amount):
            self.add_prey()
        for _ in range(self.start_food_amount):
            self.add_food()
        for _ in range(self.start_hunter_amount):
            self.add_hunter()

    def add_prey(self) -> None:
        """A method that adds a new prey to the list of prey"""
        self.prey.append(Prey(w=self.screen))

    def add_food(self) -> None:
        """A method that adds a new food to the list of food"""
        self.foods.append(Food(w=self.screen))

    def add_hunter(self) -> None:
        """A method that adds a new hunter to the list of hunters"""
        self.hunters.append(Hunter(w=self.screen))

    def update(self, dt) -> None:
        """The update method that runs every frame to update the entities
        behaviours, positions, rotations

        Args:
            dt (TYPE): Description
        """

        if not self.pause_simulation:
            all_entities = self.foods + self.prey + self.eggs + self.hunters

            for entity in all_entities:
                entity.update(
                    sdl=self.show_debug_lines,
                    h=self.hunters,
                    p=self.prey,
                    f=self.foods,
                    e=self.eggs,
                    dt=dt,
                )

                if (
                    entity.pos.y > self.screen.get_height()
                    or entity.pos.y < 0
                    or entity.pos.x > self.screen.get_width()
                    or entity.pos.x < 0
                ):
                    if entity in self.prey:
                        self.prey.remove(entity)
                    elif entity in self.hunters:
                        self.hunters.remove(entity)
                    else:
                        self.eggs.remove(entity)

                    del entity
