"""The main Python file

Attributes:
    window (Surface): the PyGame window
    clock (clock): the clock used to tick the simulation
    fps (int): the target frames per second
    sim (simulation): the simulation
    font (font): the actual font used for rendering
    version (font): the version font

    run (bool): the check for running the window
"""
import pygame
from pygame.time import Clock
import simulation
import settings


pygame.init()
pygame.font.init()


window = pygame.display.set_mode(settings.WINDOW_SIZE)
pygame.display.set_caption("Capstone Project")
clock: Clock = pygame.time.Clock()
sim: simulation.Simulation = simulation.Simulation(w=window)
fps: int = 60


font: pygame.font.Font = pygame.font.Font(
    "src/fonts/Diavlo Medium.otf", settings.FONT_SIZE
)
version: pygame.Surface = font.render(f"{settings.VERSION}", True, "black")


def update_ui() -> None:
    """Updates the UI of the simulation, located at the bottom of the screen"""
    if settings.WINDOW_HEIGHT > 0:
        rect = pygame.Rect(
            (0, window.get_height() - settings.WINDOW_HEIGHT),
            (window.get_width(), settings.WINDOW_HEIGHT),
        )
        pygame.draw.rect(window, "white", rect)

        # creating the UI list
        ui = [
            version,
            font.render(f"Food: {len(sim.foods)}", True, "black"),
            font.render(f"Prey: {len(sim.prey)}", True, "black"),
            font.render(f"Eggs: {len(sim.eggs)}", True, "black"),
            font.render(f"Hunters: {len(sim.hunters)}", True, "black"),
            font.render(f"Paused: {sim.pause_simulation == False}", True, "black"),
            font.render(f"FPS: {int(clock.get_fps())}", True, "black"),
        ]

        # getting total width and the spacing between the objects
        total_ui_width = sum(ui[i].get_width() for i in range(len(ui)))
        x_spacing = (window.get_width() - total_ui_width) / (len(ui) + 1)

        # looping through the ui and bliting them
        for i, element in enumerate(ui):
            x_position = x_spacing * (i + 1) + sum(ui[j].get_width() for j in range(i))
            y_position = window.get_height() - settings.FONT_SIZE

            window.blit(element, (x_position, y_position))


run = True
while run:
    # deltaTime
    dt = clock.tick(fps) * 0.001

    # all events
    keys = pygame.key.get_pressed()

    for e in pygame.event.get():
        # quiting the simulation
        if e.type == pygame.QUIT:
            run = False

        if e.type == pygame.KEYDOWN:
            # restarting
            if e.key == pygame.K_r:
                sim = simulation.Simulation(w=window)

            # pausing
            if e.key == pygame.K_p:
                sim.pause_simulation = not sim.pause_simulation

            # increasing FPS
            if e.key == pygame.K_EQUALS:
                fps += 60
            # decreasing FPS
            if e.key == pygame.K_MINUS and fps > 60:
                fps -= 60

            # drawing debug lines
            if e.key == pygame.K_l:
                sim.show_debug_lines = not sim.show_debug_lines

    # update background
    window.fill("black")

    # update simulation
    sim.update(dt=dt)

    # update UI
    update_ui()

    # update window
    pygame.display.update()

pygame.quit()
