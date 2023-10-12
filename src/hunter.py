import random

import pygame

import src.entity as entity
import src.settings as settings


class Hunter(entity.Entity):
    def __init__(self, window) -> None:
        self.ai_target = None

        self.sorted_hunters: list = []
        self.sorted_test_entities: list = []

        self.priority_reproduce: bool = False
        self.reproductive_urge: float = 0

        self.priority_food_source: bool = False
        self.should_wander: bool = True
        self.energy_from_food_source: float = 1

        super().__init__(window)

    def update(self, dt, test_entities, hunters) -> None:
        self.sorted_test_entities = self.update_list_by_distance(hunters)
        self.sorted_hunters = self.update_list_by_distance(test_entities)

        self.dt = dt

        self.update_ai_state()
        self.update_ai_behaviour()

        super().update(settings.hunter_color, settings.hunter_size)

    def update_list_by_distance(self, old_list) -> list:
        unsorted_dict = dict()

        for item in old_list:
            if item is self:
                continue
            unsorted_dict.__setitem__(
                item, pygame.Vector2.distance_to(self.pos, item.pos)
            )

        return sorted(unsorted_dict.items(), key=lambda x: x[1])

    def update_ai_state(self):
        """Updates the state based on a few different variables"""
        if self.energy_from_food_source >= self.reproductive_urge:
            self.priority_food_source = True
            self.priority_reproduce = False
        else:
            self.priority_food_source = False
            self.priority_reproduce = True

    def update_ai_behaviour(self):
        """Updates the behaviour of the AI per frame"""
        # if self.priority_food_srouce:
        #     self.check_for_food_source()
        # else:
        #     self.check_for_mate()
