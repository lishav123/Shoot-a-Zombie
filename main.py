import pygame
from sprites import Zombie
from random import randint

pygame.init()

WIDTH, HEIGHT = 1200, 800
window = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Shoot a Mole")

bg_image = pygame.image.load(f"./assets/Background.png")
bg_image = pygame.transform.scale(bg_image, (WIDTH + 500, HEIGHT + 500))

sizes = [(10, 10), (20, 20), (50, 50), (100, 100)]
size = (100, 100)

effect_image = pygame.image.load(f"./assets/boom.png")
effect_image = pygame.transform.scale(effect_image, size)

side_effect_after_shoot = []

game_closed = False
pygame.mouse.set_visible(False)

zombies = [
    {
        "state": Zombie(window, -randint(10, 50), 480, 0.45),
        "speed": randint(2, 10) * (0.5),
        "flip" : False
    } for _ in range(1)
]

fps = pygame.time.Clock()
while not game_closed:
    mouse_x, mouse_y = pygame.mouse.get_pos()

    window.blit(bg_image, (0, -500))
    fps.tick(60)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_closed = True

        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 3 or event.button == 1:
                window.fill((255, 255, 255))
                pygame.display.flip()


                for i, zombie in enumerate(zombies):
                    if zombie["state"].is_inside_area(mouse_x, mouse_y):
                        side_effect_after_shoot.append({"image": effect_image})
                        del zombies[i]

    for zombie in zombies:
        zombie["state"].display_state(flip=zombie["flip"])
        zombie["state"].change_position(zombie["state"].x + zombie["speed"], zombie["state"].y)

        if zombie["state"].x > WIDTH:
            zombie["speed"] = -zombie["speed"]
            zombie["flip"]  = not zombie["flip"]

        if zombie["state"].x < -50:
            zombie["speed"] = -zombie["speed"]
            zombie["flip"]  = not zombie["flip"]

    window.blit(effect_image, (mouse_x - size[0]/2, mouse_y - size[1]/2))
    pygame.draw.circle(window, (255, 0, 0), (mouse_x, mouse_y), 5)
    pygame.display.flip()

pygame.quit()