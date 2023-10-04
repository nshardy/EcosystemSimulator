import pygame

import src.settings as settings
from src.simulation import Simulation


pygame.init()
window = pygame.display.set_mode(settings.window_dimensions)
clock = pygame.time.Clock()
pygame.display.set_caption("Ecosystem Simulator")

# the Simulation variable
simulation = Simulation(window)


run = True
while run:
    # updates the simulation at a consistent framerate
    clock.tick(settings.fps)

    # get keyboard / quit events
    for e in pygame.event.get():
        if e.type == pygame.QUIT or (
            e.type == pygame.KEYDOWN and e.key == pygame.K_ESCAPE
        ):
            run = False

    # update background
    window.fill("black")

    # TODO: simulation step
    simulation.update()

    # update pygame window
    pygame.display.update()


# quits the simulation entirely
pygame.quit()
