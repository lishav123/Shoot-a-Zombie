import pygame
from sprites import Zombie
from random import randint

pygame.init()

WIDTH, HEIGHT = 1200, 800
window = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Shoot a Mole")

game_closed = False
pygame.mouse.set_visible(False)

zombies = [
    {
        "state": Zombie(window, -randint(10, 50), 200, 0.45),
        "speed": randint(2, 10),
        "flip" : False
    } for _ in range(5)
]

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

    for zombie in zombies:
        zombie["state"].display_state(flip=zombie["flip"])
        zombie["state"].change_position(zombie["state"].x + zombie["speed"], zombie["state"].y)

        if zombie["state"].x > WIDTH:
            zombie["speed"] = -zombie["speed"]
            zombie["flip"]  = not zombie["flip"]

        if zombie["state"].x < -50:
            zombie["speed"] = -zombie["speed"]
            zombie["flip"]  = not zombie["flip"]

    mouse_x, mouse_y = pygame.mouse.get_pos()

    pygame.draw.circle(window, (255, 0, 0), (mouse_x, mouse_y), 5)

    pygame.display.flip()

pygame.quit()