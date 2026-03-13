import pygame
from random import randint, choice

from sprites import Zombie

pygame.init()

# Sound assets initalized
pygame.mixer.set_num_channels(8)
bg_music = pygame.mixer.Sound("./assets/jojo.mp3") # Music that will play when the game will start
shoot_music = pygame.mixer.Sound("./assets/gunshot.mp3") # The sound effect of the shoot

# Initializing the fonts
font = pygame.font.SysFont('Arial', 36)  # Font for small texts
bigfont = pygame.font.SysFont('Arial', 50) # Font for big task mainly for first screen

# When user will shoot the zombie, we can see a effect like image of "boom" is scaling, this class is made for handling that effect in ease
class SideEffects:
    def __init__(self, window, x, y, size_array, location):
        '''
          Args:
            window: the game window
            x: the x-axis
            y: the y-axis
            size_array: the array of tuples for animation expanding
            location: location of the image
            image: the image object
            self._index: for following the list of size of objects
        '''
        self.window = window 
        self.x = x 
        self.y = y 
        self.size_array = size_array
        self.location = location
        self.image = None  
        self._index = 0

    def display(self):
        '''
          This displays the animation
        '''
        if self._index == len(self.size_array) - 1:
            ...
        else:
            self.image = pygame.image.load(self.location)
            self.image = pygame.transform.scale(self.image, self.size_array[self._index])
            self.window.blit(self.image, (self.x - (self.size_array[self._index][0] / 2), self.y - (self.size_array[self._index][0] / 2))) 

    def update_index(self):
        '''
          updates the animation here.
        '''
        if self._index == len(self.size_array) - 1:
            ...
        else:
            self._index += 1

# Configuring the game window
WIDTH, HEIGHT = 1200, 800
window = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Shoot a Mole")

# Loading the background image (not displayed yet)
bg_image = pygame.image.load(f"./assets/Background.png")
bg_image = pygame.transform.scale(bg_image, (WIDTH + 500, HEIGHT + 500))

# Loading the opening image of the game
open_image = pygame.transform.scale(pygame.image.load(f"./assets/open.png"), (WIDTH, HEIGHT))

# setting the size animation for "boom" effects, means first size will be 0 height 0 width pixels then 10 height 10 width pixels then 20....30 and so on till 100
sizes = [(i * 10, i * 10) for i in range(11)]
side_effect_after_shoot = [] # will track the postions of boom so that it can play on specifiy area where needed

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

score = 0
hight_score = 0

try:
    with open("highscore.txt") as fs:
        hight_score = int(fs.read().strip())
except:
    with open("highscore.txt", "w") as fs:
        fs.write("0")

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
                    shoot_music.play()

                    for i, zombie in enumerate(zombies):
                        if zombie["state"].is_inside_area(mouse_x, mouse_y):
                            side_effect_after_shoot.append(SideEffects(window=window, x=mouse_x, y=mouse_y, size_array=sizes, location="./assets/boom.png"))
                            zombies[:] = list(filter(lambda z: z["id"] != zombie["id"], zombies))
                            score += 5
                
                elif page == 0:
                    if (mouse_x > 500 and mouse_x < 735) and (mouse_y > 400 and mouse_y < 460):
                        page = 1
                        score = 0
                        bg_music.play(loops=-1) 

    
    if page == 0:
        window.blit(open_image, (0, 0))
        window.blit(bigfont.render(f'PLAY GAME', True, (255, 0, 0), (25, 25, 25)), (WIDTH / 2 - 100, HEIGHT / 2))
        window.blit(font.render(f'Recent Hight Score: {hight_score} | Recent Score: {score}', True, (255, 255, 255), (25, 25, 25)), (WIDTH / 2 - 270, HEIGHT - 60))

        if score > hight_score:
            with open("highscore.txt", "w") as fs:
                fs.write(f"{score}")
                hight_score = score

    elif page == 1:

        window.blit(bg_image, (0, -500))
        window.blit(font.render(f'Level: {level}', True, (255, 255, 255)), (10, 10))
        window.blit(font.render(f'Score: {score}', True, (255, 255, 255)), (WIDTH - 180, 10))

        

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
            if not level > 150:
                nums_zombies = (level // 10) + 1

            zombies.extend([{
                "id": f"Lv{level}Idx{num}",
                "state": Zombie(window, -(num * 120) + randint(10, 50), choice([60, 480]), 0.45),
                "speed": randint(5, 8),
                "flip" : False
            } for num in range(nums_zombies)])
            level += 1

        if allow_missed == 0:
            page = 0
            allow_missed = 15
            level = 1
            zombies = [{
                "id": zombie_id,
                "state": Zombie(window, -randint(10, 50), 480, 0.45),
                "speed": randint(2, 10) * (0.5),
                "flip" : False
            } for _ in range(level)
            ]
            zombie_id = 0
            bg_music.stop()


    pygame.draw.circle(window, (255, 0, 0), (mouse_x, mouse_y), 5)
    pygame.display.flip()

pygame.quit()
