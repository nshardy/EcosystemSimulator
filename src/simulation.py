import src.tester_entity


class Simulation:
    def __init__(self, window) -> None:
        """Activates when initialized

        Args:
            window (surface): the pygame window
        """
        self.window = window
        self.test_entities = []

        self.test_entities.append(src.tester_entity.TesterEntity(self.window))

    def update(self) -> None:
        """Updates per frame"""
        for e in self.test_entities:
            e.update()
