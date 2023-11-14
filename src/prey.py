"""The prey Python file
"""
import math
import time
import food
import pygame
import settings
import random as r
from egg import Egg
from entity import Entity
from typing import Optional


class Prey(Entity):

    """The prey class

    Attributes:
        ai_target (entity): the current target
        angle (float): the angle
        egg_list (list): the list of all eggs
        food_is_priority (bool): if the entity is hungry and that is the priority
        food_list (list): the list of all food
        food_ordered_by_distance (list): a list of all food, ordered by distance
        hunter_list (list): the list of all hunters
        hunters_ordered_by_distance (list): a list of all hunters, ordered by distance
        mate_is_priority (bool): if finding a mate is priority
        mates_ordered_by_distance (list): a list of all mates, ordered by distance
        prey_list (list): the list of all prey
        reproductive_urge (int): how strongly the prey wants to amte
        screen (surface): the Pygame window
        self_is_priority (bool): if this entity is being hunted
    """

    def __init__(self, w) -> None:
        """The initializer method

        Args:
            w (Surface): the window
        """

        self.screen = w

        # Initialize lists and dictionaries
        self.prey_list: list = []
        self.hunter_list: list = []
        self.food_list: list = []
        self.egg_list: list = []
        self.mates_ordered_by_distance: dict
        self.food_ordered_by_distance: dict
        self.hunters_ordered_by_distance: dict

        # Behavior parameters
        self.wander_strength: float = 0.1
        self.speed: int = 1
        self.angle: float = r.uniform(0, 2 * math.pi)

        self.food_is_priority: bool = False
        self.food_check_distance: int = 50
        self.eating_distance: int = 1
        self.energy: float = 1
        self.metabolism: float = r.random()
        self.age: int = r.randrange(20, 50)
        self.age_timer: float = 0

        self.laying_eggs: bool = False
        # self.amount_of_offspring: int = r.randint(1, 3)
        self.amount_of_offspring: int = 3
        self.energy_needed_to_mate: int = r.randint(3, 5)
        self.reproductive_urge = 0
        self.mate_is_priority: bool = False
        self.gender: bool = bool(r.getrandbits(1))
        self.mating_distance: int = 5
        self.pheromone_secretion_distance: float = r.randint(10, 50)
        self.pheromone_detection_distance: float = r.randint(50, 100)
        self.egg_hatch_timer = 0

        self.self_is_priority: bool = False
        self.is_hunter_target: bool = False

        self.ai_target: Optional[Entity] = None

        # Call superclass constructor
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

        self.hunter_list = h
        self.prey_list = p
        self.food_list = f
        self.egg_list = e

        # Debug drawing
        if sdl:
            if self.ai_target is not None and self.ai_target in self.food_list:
                pygame.draw.line(
                    self.screen, settings.FOOD_COLOR, self.pos, self.ai_target.pos
                )
            if self.ai_target is not None and self.ai_target in self.prey_list:
                pygame.draw.line(
                    self.screen, settings.MATE_COLOR, self.pos, self.ai_target.pos
                )

        self.reproductive_urge += dt * self.metabolism * self.metabolism
        self.energy -= dt * self.metabolism * 0.1
        self.age_timer += dt * self.metabolism * self.metabolism
        self.dt = dt

        # Update closest objects
        self.food_ordered_by_distance = self.update_dict_by_distance(self.food_list)
        self.mates_ordered_by_distance = self.update_dict_by_distance(self.prey_list)
        self.hunters_ordered_by_distance = self.update_dict_by_distance(
            self.hunter_list
        )

        # Update behaviors
        self.ai_state_management()
        self.ai_state_logic()

        self.death_check(p=p)

        # Call superclass update method
        super().update(dt=dt, color=settings.PREY_COLOR, size=settings.ENTITY_SIZE)

    def update_dict_by_distance(self, old_list) -> list:
        """Returns a new list sorted by distance

        Args:
            old_list (list): the old list that is being used to create the new list

        Returns:
            list: a container of items
        """

        unsorted_dict = dict()

        for item in old_list:
            if item is self:
                continue
            unsorted_dict.__setitem__(
                item, pygame.Vector2.distance_to(self.pos, item.pos)
            )

        # Return the sorted list of tuples by distance
        return sorted(unsorted_dict.items(), key=lambda x: x[1])

    def ai_state_management(self) -> None:
        """Controls what bools are active based on certain conditions"""

        if self.is_hunter_target:
            self.self_is_priority = True
            self.food_is_priority = False
            self.mate_is_priority = False
            self.ai_target = None
        elif self.energy <= self.energy_needed_to_mate and not self.is_hunter_target:
            self.self_is_priority = False
            self.food_is_priority = True
            self.mate_is_priority = False
        elif (
            self.reproductive_urge > self.energy_needed_to_mate
            and not self.is_hunter_target
        ):
            self.self_is_priority = False
            self.food_is_priority = False
            self.mate_is_priority = True

    def ai_state_logic(self) -> None:
        """Controls what the entity is doing based on if self, food or mate is priority"""

        if self.self_is_priority:
            self.move_away_from_hunter()
        elif self.food_is_priority:
            self.check_for_food()
        elif self.mate_is_priority:
            self.check_for_mate()

    def move_away_from_hunter(self) -> None:
        """Moves away from the hunter"""

        if len(self.hunters_ordered_by_distance) > 0:
            self.ai_target = self.hunters_ordered_by_distance[0][0]
            self.angle = math.atan2(
                self.ai_target.pos.y - self.pos.y, self.ai_target.pos.x - self.pos.x
            )
            self.angle = -self.angle
            self.move_by_angle_and_speed()

    def death_check(self, p) -> None:
        """Checks if this entity should die

        Args:
            p (list): the prey list
        """

        if self.energy <= 0 or self.age_timer > self.age:
            p.remove(self)

    def move_wander(self) -> None:
        """Controls wandering around randomly"""

        if (
            self.pos.x < 0 + settings.ENTITY_WINDOW_BORDER
            or self.pos.x > 800
            or self.pos.y < 0 + settings.ENTITY_WINDOW_BORDER
            or self.pos.y > 600
        ):
            self.angle += math.pi

        if r.random() < self.wander_strength:
            self.angle += r.uniform(-0.5, 0.5)

        self.move_by_angle_and_speed()

    def move_by_angle_and_speed(self) -> None:
        """Move entity based on angle and speed"""

        self.pos.x += self.speed * math.cos(self.angle)
        self.pos.y += self.speed * math.sin(self.angle)

    def check_for_food(self) -> None:
        """Checking the closest food if it's in range, and moving to it if it is"""

        if self.food_ordered_by_distance.__len__() > 0:
            food_obj = self.food_ordered_by_distance[0][0]
            food_dst = self.food_ordered_by_distance[0][1]

            # If food is far away and there's no target, wander
            if food_dst > self.food_check_distance and self.ai_target is None:
                self.move_wander()
            # If food is within distance, set it as the target
            elif food_dst < self.food_check_distance:
                del self.ai_target
                self.ai_target = food_obj

                # Move towards the food target
                self.move_to_food_target()
        else:
            self.move_wander()

    def move_to_food_target(self) -> None:
        """Moving this prey to the food"""
        if self.ai_target is not None:
            self.angle = math.atan2(
                self.ai_target.pos.y - self.pos.y, self.ai_target.pos.x - self.pos.x
            )
            self.move_by_angle_and_speed()

            dist = pygame.Vector2.distance_to(self.pos, self.ai_target.pos)
            # Check if close enough to target
            if dist < self.eating_distance:
                # Remove target if it's a food object
                if self.ai_target in self.food_list and isinstance(
                    self.ai_target, food.Food
                ):
                    self.energy += self.ai_target.energy
                    self.food_list.remove(self.ai_target)

                self.ai_target = None

    def check_for_mate(self) -> None:
        """Checking the closest mate if it's in range, and moving to it if it is"""

        if self.mates_ordered_by_distance.__len__() > 0:
            # Get the closest food object and its distance
            mate_obj = self.mates_ordered_by_distance[0][0]
            mate_dst = self.mates_ordered_by_distance[0][1]

            # If mate is far away and there's no target, or they aren't wanting a mate, wander
            if (
                (
                    mate_dst
                    > self.pheromone_detection_distance
                    + mate_obj.pheromone_secretion_distance
                    and self.ai_target is None
                )
                or mate_obj.mate_is_priority == False
                or mate_obj.laying_eggs
            ):
                self.ai_target = None

            # If mate is within distance, opposite gender and wanting a mate, set it as the target
            elif (
                mate_dst
                < self.pheromone_detection_distance
                + mate_obj.pheromone_secretion_distance
                and self.gender != mate_obj.gender
                and mate_obj.mate_is_priority
            ):
                self.ai_target = mate_obj

            # Move towards the mate target
            if self.ai_target:
                self.move_to_mate_target()
            else:
                self.move_wander()
        else:
            self.reproductive_urge = 0
            self.move_wander()

    def move_to_mate_target(self) -> None:
        """Moving this prey to the mate"""

        if (
            self.ai_target is not None
            and self.ai_target not in self.food_ordered_by_distance
        ):
            # Move towards the target
            self.angle = math.atan2(
                self.ai_target.pos.y - self.pos.y, self.ai_target.pos.x - self.pos.x
            )
            self.move_by_angle_and_speed()
            dist = pygame.Vector2.distance_to(self.pos, self.ai_target.pos)

            if dist < self.mating_distance and self.gender == True:
                self.reproductive_urge = 0

            elif dist < self.mating_distance and self.gender == False:
                self.laying_eggs = True

                while self.laying_eggs:
                    for _ in range(self.amount_of_offspring):
                        self.egg_hatch_timer += self.dt

                        if self.egg_hatch_timer > 1.25:
                            current_pos = pygame.Vector2(self.pos.x, self.pos.y)
                            child_egg = Egg(self.screen, self, current_pos, "p")
                            self.energy = 1
                            self.egg_list.append(child_egg)
                            self.egg_hatch_timer = 0

                    self.laying_eggs = False

                # TODO: bug with reproducing, creating hundreds of eggs
                self.reproductive_urge = 0
        else:
            self.reproductive_urge = 0
            self.move_wander()
