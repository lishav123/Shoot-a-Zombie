import pygame
from sprites import Zombie

pygame.init()

WIDTH, HEIGHT = 1200, 800
window = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Shoot a Mole")

game_closed = False
pygame.mouse.set_visible(False)

zombie = Zombie(window, -50, 500, 0.45)
zombie_speed = 10
zombie_flip = False

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

    zombie.display_state(flip=zombie_flip)
    zombie.change_position(zombie.x + zombie_speed, zombie.y)

    if zombie.x > WIDTH:
        zombie_speed = -zombie_speed
        zombie_flip = not zombie_flip

    if zombie.x < -50:
        zombie_speed = -zombie_speed
        zombie_flip = not zombie_flip

    mouse_x, mouse_y = pygame.mouse.get_pos()

    pygame.draw.circle(window, (255, 0, 0), (mouse_x, mouse_y), 5)

    pygame.display.flip()

pygame.quit()