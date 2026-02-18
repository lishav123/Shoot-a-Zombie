import pygame

from sprites import Zombie
from random import randint

pygame.init()

WIDTH, HEIGHT = 1200, 800
window = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Shoot a Mole")

bg_image = pygame.image.load(f"./assets/Background.png")
bg_image = pygame.transform.scale(bg_image, (WIDTH + 500, HEIGHT + 500))

sizes = [(i * 10, i * 10) for i in range(11)]
side_effect_after_shoot = []

game_closed = False
pygame.mouse.set_visible(False)

class SideEffects:
    def __init__(self, window, x, y, size_array, location):
        self.window = window 
        self.x = x 
        self.y = y 
        self.size_array = size_array
        self.location = location
        self.image = None  
        self._index = 0

    def display(self):
        if self._index == len(self.size_array) - 1:
            ...
        else:
            self.image = pygame.image.load(self.location)
            self.image = pygame.transform.scale(self.image, self.size_array[self._index])
            self.window.blit(self.image, (self.x - (self.size_array[self._index][0] / 2), self.y - (self.size_array[self._index][0] / 2))) 

    def update_index(self):
        if self._index == len(self.size_array) - 1:
            ...
        else:
            self._index += 1


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
                pygame.display.flip()
                pygame.mixer.music.load("./assets/gunshot.mp3")
                pygame.mixer.music.play()

                for i, zombie in enumerate(zombies):
                    if zombie["state"].is_inside_area(mouse_x, mouse_y):
                        side_effect_after_shoot.append(SideEffects(window=window, x=mouse_x, y=mouse_y, size_array=sizes, location="./assets/boom.png"))
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

    for s_effect in side_effect_after_shoot:
        s_effect.display()
        s_effect.update_index()

    pygame.draw.circle(window, (255, 0, 0), (mouse_x, mouse_y), 5)
    pygame.display.flip()

pygame.quit()