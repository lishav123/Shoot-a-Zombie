import pygame
from random import randint, choice

from sprites import Zombie

pygame.init()
font = pygame.font.SysFont('Arial', 36) 
bigfont = pygame.font.SysFont('Arial', 50) 

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

WIDTH, HEIGHT = 1200, 800
window = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Shoot a Mole")

bg_image = pygame.image.load(f"./assets/Background.png")
bg_image = pygame.transform.scale(bg_image, (WIDTH + 500, HEIGHT + 500))

open_image = pygame.transform.scale(pygame.image.load(f"./assets/open.png"), (WIDTH, HEIGHT))

sizes = [(i * 10, i * 10) for i in range(11)]
side_effect_after_shoot = []

game_closed = False
pygame.mouse.set_visible(False)

level = 1
zombie_id = 0
allow_missed = 15
zombies = [
    {
        "id": zombie_id,
        "state": Zombie(window, -randint(10, 50), 480, 0.45),
        "speed": randint(2, 10) * (0.5),
        "flip" : False
    } for _ in range(level)
]

fps = pygame.time.Clock()

page = 0

while not game_closed:
    mouse_x, mouse_y = pygame.mouse.get_pos()
    fps.tick(60)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_closed = True

        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 3 or event.button == 1:
                pygame.display.flip()

                if page == 1:
                    pygame.mixer.music.load("./assets/gunshot.mp3")
                    pygame.mixer.music.play()

                    for i, zombie in enumerate(zombies):
                        if zombie["state"].is_inside_area(mouse_x, mouse_y):
                            side_effect_after_shoot.append(SideEffects(window=window, x=mouse_x, y=mouse_y, size_array=sizes, location="./assets/boom.png"))
                            zombies[:] = list(filter(lambda z: z["id"] != zombie["id"], zombies))
                
                elif page == 0:
                    if (mouse_x > 500 and mouse_x < 735) and (mouse_y > 400 and mouse_y < 460):
                        page = 1
    
    if page == 0:
        window.blit(open_image, (0, 0))
        window.blit(bigfont.render(f'PLAY GAME', True, (255, 0, 0), (25, 25, 25)), (WIDTH / 2 - 100, HEIGHT / 2))

    elif page == 1:
        window.blit(bg_image, (0, -500))
        window.blit(font.render(f'Level: {level}', True, (255, 255, 255)), (10, 10))

        pygame.draw.rect(window, (0, 0, 0), pygame.Rect((WIDTH / 2 - 100), 10, 15 * 15, 36))
        pygame.draw.rect(window, (255, 0, 0), pygame.Rect((WIDTH / 2 - 100), 10, 15 * allow_missed, 36))

        for i, zombie in enumerate(zombies):
            zombie["state"].display_state(flip=zombie["flip"])
            zombie["state"].change_position(zombie["state"].x + zombie["speed"], zombie["state"].y)

            if zombie["state"].x > WIDTH + 100:
                zombies[:] = list(filter(lambda z: z["id"] != zombie["id"], zombies))
                allow_missed -= 1

        for s_effect in side_effect_after_shoot:
            s_effect.display()
            s_effect.update_index()

        if len(zombies) == 0:
            zombies.extend([{
                "id": f"Lv{level}Idx{num}",
                "state": Zombie(window, -(num * 120) + randint(10, 50), choice([60, 480]), 0.45),
                "speed": randint(5, 8),
                "flip" : False
            } for num in range((level // 10) + 1)])
            level += 1

        if allow_missed == 0:
            page = 0


    pygame.draw.circle(window, (255, 0, 0), (mouse_x, mouse_y), 5)
    pygame.display.flip()

pygame.quit()