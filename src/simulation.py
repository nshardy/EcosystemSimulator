import src.hunter
import src.tester_entity


class Simulation:
    def __init__(self, window) -> None:
        """Activates when initialized

        Args:
            window (surface): the pygame window
        """
        self.window = window

        self.test_entities: list = []
        self.hunters: list = []

        self.test_entities.append(src.tester_entity.TesterEntity(self.window))
        self.hunters.append(src.hunter.Hunter(self.window))

        self.all_entities = self.test_entities + self.hunters

    def update(self, dt) -> None:
        """Updates per frame"""
        for entity in self.all_entities:
            entity.update(dt)
