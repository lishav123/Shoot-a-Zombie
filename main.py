import pygame
from sprites import Zombie

pygame.init()

WIDTH, HEIGHT = 1200, 800
window = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Shoot a Mole")

game_closed = False
pygame.mouse.set_visible(False)

zombie = Zombie(window, 500, 500, 0.5)

fps = pygame.time.Clock()
while not game_closed:
    window.fill((0, 0, 0))
    fps.tick(60)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_closed = True

        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 3 or event.button == 1:
                window.fill((255, 255, 255))
                pygame.display.flip()

    zombie.display_state(flip=False)


    mouse_x, mouse_y = pygame.mouse.get_pos()

    pygame.draw.circle(window, (255, 0, 0), (mouse_x, mouse_y), 5)

    pygame.display.flip()

pygame.quit()