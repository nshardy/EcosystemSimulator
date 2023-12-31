"""The hunter Python file
"""
import math
import random as r

import pygame

import entity
import settings
from egg import Egg
from trait import Trait


class Hunter(entity.Entity):
    """the Hunter class

    Attributes:
        ai_target (entity): the entity target of this entity
        angle (float): the current movement angle
        energy (int): the current amount of energy
        food_is_priority (bool): if food is priority
        mate_is_priority (bool): if mate is priority
        mates_ordered_by_distance (list): a list of mates ordered by distance
        prey_ordered_by_distance (list): a list of prey ordered by distance
        reproductive_urge (int): how much this entity wants to mate
        screen (surface): the Pygame window
    """

    def __init__(self, w, mother=None, father=None) -> None:
        """The initializer method

        Args:
            w (Surface): the window
        """

        self.screen = w

        self.prey_list: list
        self.hunter_list: list
        self.egg_list: list
        self.mates_ordered_by_distance: dict
        self.prey_ordered_by_distance: dict

        # self.wander_strength: float = 0.1
        self.speed: int = 1
        # self.chase_speed: float = self.speed + r.random()
        self.angle: float = r.uniform(0, 2 * math.pi)

        self.food_is_priority: bool = False
        # self.prey_check_distance: int = 75
        # self.eating_distance: int = 1
        # self.metabolism: float = r.random()
        self.energy: float = 1
        # self.lifespan: float = r.randrange(20, 50)
        self.age_timer: float = 0
        self.lost_interest_time: int = 5
        self.lost_interest_timer: float = 0

        self.reproductive_urge: float = 0
        self.mate_is_priority: bool = False
        # self.mate_detection_distance: int = 300
        # self.gender: bool = r.choice([False, True])
        self.mating_distance: int = 5

        self.trait__gender: Trait = Trait(None, None)
        self.trait__wander_strength: Trait = Trait(None, None)
        self.trait__chase_speed: Trait = Trait(None, None)
        self.trait__prey_check_distance: Trait = Trait(None, None)
        self.trait__mate_detection_distance: Trait = Trait(None, None)
        self.trait__eating_distance: Trait = Trait(None, None)
        self.trait__metabolism: Trait = Trait(None, None)
        self.trait__lifespan: Trait = Trait(None, None)

        self.traits = [
            self.trait__gender,
            self.trait__wander_strength,
            self.trait__chase_speed,
            self.trait__prey_check_distance,
            self.trait__eating_distance,
            self.trait__metabolism,
            self.trait__lifespan,
        ]

        if not mother and not father:
            self.trait__gender = Trait(True, r.choice([True, False]))
            self.trait__wander_strength = Trait(r.choice([True, False]), r.random())
            self.trait__prey_check_distance = Trait(r.choice([True, False]), 75)
            self.trait__eating_distance = Trait(r.choice([True, False]), 1)
            self.trait__metabolism = Trait(r.choice([True, False]), r.random())
            self.trait__lifespan = Trait(r.choice([True, False]), r.randrange(20, 50))
            self.trait__chase_speed = Trait(
                r.choice([True, False]), self.speed + r.random()
            )
            self.trait__mate_detection_distance = Trait(
                r.choice([True, False]), r.randrange(75, 300)
            )
        elif mother and not father:
            for trait in self.traits:
                index = self.traits.index(trait)
                self.traits[index].trait_value = father.traits[index].trait_value
        elif not mother and father:
            for trait in self.traits:
                index = self.traits.index(trait)
                self.traits[index].trait_value = mother.traits[index].trait_value
        else:
            for trait in self.traits:
                index = self.traits.index(trait)
                self.traits[index].trait_value = Trait.compare_traits(
                    trait, mother_traits=mother, father_traits=father
                )
            # self.gender = Trait.compare_traits(mother_traits=mother, father_traits=father)
            # self.wander_strength: Trait(r.choice([True, False]), r.random())
            # self.chase_speed: Trait = Trait(
            # self.prey_check_distance: Trait = Trait(r.choice([True, False]), 75)
            # self.eating_distance: Trait = Trait(r.choice([True, False]), 1)
            # self.metabolism: Trait = Trait(r.choice([True, False]), r.random())
            # self.lifespan: Trait = Trait(r.choice([True, False]), r.randrange(20, 50))

        self.ai_target: entity = None
        self.dt: float = 0

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

        self.dt: float = dt
        self.egg_list: list = e
        self.prey_list: list = p
        self.hunter_list: list = h

        if sdl:
            if self.ai_target is not None and self.ai_target in self.prey_list:
                pygame.draw.line(
                    self.screen, settings.FOOD_COLOR, self.pos, self.ai_target.pos
                )
            if self.ai_target is not None and self.ai_target in self.hunter_list:
                pygame.draw.line(
                    self.screen, settings.MATE_COLOR, self.pos, self.ai_target.pos
                )

        self.reproductive_urge = 1 + self.trait__metabolism.trait_value
        self.energy -= dt * self.trait__metabolism.trait_value * 0.1
        self.age_timer += dt * self.trait__metabolism.trait_value * 0.1

        self.prey_ordered_by_distance = self.update_dict_by_distance(p)
        self.mates_ordered_by_distance = self.update_dict_by_distance(h)

        self.ai_state_management()
        self.ai_state_logic()

        self.death_check(h=h)

        super().update(dt=dt, color=settings.HUNTER_COLOR, size=settings.ENTITY_SIZE)

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

        # Return the sorted dictionary by distance
        return sorted(unsorted_dict.items(), key=lambda x: x[1])

    def ai_state_management(self) -> None:
        """Controls what bools are active based on certain conditions"""

        if self.energy > self.reproductive_urge:
            self.food_is_priority = True
            self.mate_is_priority = False
        elif self.reproductive_urge > self.energy:
            self.food_is_priority = False
            self.mate_is_priority = True

    def ai_state_logic(self) -> None:
        """Controls what the entity is doing based on if food or mate is priority"""

        if self.food_is_priority:
            self.check_for_prey()
        elif self.mate_is_priority:
            self.check_for_mate()

    def death_check(self, h) -> None:
        """Checks if this entity should die

        Args:
            h (list): the hunter list
        """

        if self.energy <= 0 or self.age_timer > self.trait__lifespan.trait_value:
            h.remove(self)

    def move_wander(self) -> None:
        """Controls wandering around randomly"""

        if (
                self.pos.x < 0 + settings.ENTITY_WINDOW_BORDER
                or self.pos.x > 800
                or self.pos.y < 0 + settings.ENTITY_WINDOW_BORDER
                or self.pos.y > 600
        ):
            self.angle += math.pi

        if r.random() < self.trait__wander_strength.trait_value:
            self.angle += r.uniform(-0.5, 0.5)

        self.move_by_angle_and_speed()

    def move_by_angle_and_speed(self) -> None:
        """Move entity based on angle and speed"""

        if self.ai_target and self.ai_target not in self.prey_ordered_by_distance:
            self.pos.x += self.speed * math.cos(self.angle)
            self.pos.y += self.speed * math.sin(self.angle)
        else:
            self.pos.x += self.trait__chase_speed.trait_value * math.cos(self.angle)
            self.pos.y += self.trait__chase_speed.trait_value * math.sin(self.angle)

    def check_for_prey(self) -> None:
        """Checking the closest prey if it's in range, and moving to it if it is"""

        if self.prey_ordered_by_distance.__len__() > 0:
            prey_obj = self.prey_ordered_by_distance[0][0]
            prey_dst = self.prey_ordered_by_distance[0][1]

            # If food is far away and there's no target, wander
            if (
                    prey_dst > self.trait__prey_check_distance.trait_value
                    and self.ai_target is None
            ):
                self.move_wander()
            # If food is within distance, set it as the target
            elif prey_dst < self.trait__prey_check_distance.trait_value:
                del self.ai_target
                self.ai_target = prey_obj

            # Move towards the food target
            if self.ai_target:
                if self.ai_target in self.prey_list:
                    if not self.ai_target.is_hunter_target:
                        self.ai_target.is_hunter_target = True
                    else:
                        self.lost_interest_timer += self.dt
                        if self.lost_interest_timer > self.lost_interest_time:
                            self.ai_target.is_hunter_target = False
                            self.ai_target = None
                self.move_to_prey_target()
        else:
            self.move_wander()

    def move_to_prey_target(self) -> None:
        """Moving this hunter to the prey"""

        if self.ai_target:
            # Move towards the target
            self.angle = math.atan2(
                self.ai_target.pos.y - self.pos.y, self.ai_target.pos.x - self.pos.x
            )
            self.move_by_angle_and_speed()

            dist = pygame.Vector2.distance_to(self.pos, self.ai_target.pos)
            # Check if close enough to target
            if dist < self.trait__eating_distance.trait_value:
                # Remove target if it's a food object
                self.energy = 1
                if self.ai_target in self.prey_list:
                    self.prey_list.remove(self.ai_target)

                self.ai_target = None

    def check_for_mate(self) -> None:
        """Checking the closest mate if it's in range, and moving to it if it is"""

        if self.mates_ordered_by_distance.__len__() > 0:
            # Get the closest food object and its distance
            mate_obj = self.mates_ordered_by_distance[0][0]
            mate_dst = self.mates_ordered_by_distance[0][1]

            # If mate is far away and there's no target, or they aren't wanting a mate, wander
            if (
                    mate_dst > self.trait__mate_detection_distance.trait_value
                    and self.ai_target is None
            ) or mate_obj.mate_is_priority is False:
                self.ai_target = None

            # If mate is within distance, opposite gender and wanting a mate, set it as the target
            elif (
                    mate_dst < self.trait__mate_detection_distance.trait_value
                    and self.trait__gender.trait_value != mate_obj.trait__gender.trait_value
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
        """Moving this hunter to the mate"""

        if (
                self.ai_target
                not in self.prey_ordered_by_distance
                # and self.ai_target in self.mates_ordered_by_distance
        ):
            # Move towards the target
            self.angle = math.atan2(
                self.ai_target.pos.y - self.pos.y, self.ai_target.pos.x - self.pos.x
            )
            self.move_by_angle_and_speed()
            dist = pygame.Vector2.distance_to(self.pos, self.ai_target.pos)

            if dist < self.mating_distance and self.trait__gender.trait_value == True:
                self.reproductive_urge = 0
                self.energy -= self.trait__metabolism.trait_value
            elif (
                    dist < self.mating_distance and self.trait__gender.trait_value == False
            ):
                current_pos = pygame.Vector2(self.pos.x, self.pos.y)
                child_egg = Egg(
                    self.screen,
                    current_pos,
                    "h",
                    mothers_traits=self.traits,
                    fathers_traits=self.ai_target.traits,
                )
                self.egg_list.append(child_egg)
                self.reproductive_urge = 0
                self.energy -= self.trait__metabolism.trait_value
        else:
            self.reproductive_urge = 0
            self.move_wander()
