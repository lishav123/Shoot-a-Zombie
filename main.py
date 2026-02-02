import pygame

pygame.init()

WIDTH, HEIGHT = 1200, 800
window = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Shoot a Mole")

game_closed = False
while not game_closed:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_closed = True

        if event.type == pygame.KEYDOWN:
            window.fill((255, 255, 255))


    mouse_x, mouse_y = pygame.mouse.get_pos()

    window.fill((0, 0, 0))
    pygame.draw.circle(window, (255, 0, 0), (mouse_x, mouse_y), 10)

    pygame.display.flip()

pygame.quit()