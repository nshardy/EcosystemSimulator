import pygame


pygame.init()
window = pygame.display.set_mode((800, 600))
clock = pygame.time.Clock()
pygame.display.set_caption("Ecosystem Simulator")


run = True
while run:
    clock.tick(60)

    for e in pygame.event.get():
        if e.type == pygame.QUIT or (
            e.type == pygame.KEYDOWN and e.key == pygame.K_ESCAPE
        ):
            run = False

    # update background
    window.fill("black")

    # TODO: simulation step

    # update pygame window
    pygame.display.update()


pygame.quit()
