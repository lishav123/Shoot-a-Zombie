from pygame import transform
from pygame import image

from os import listdir

zombies = listdir('./assets/')

class ZombieSprite:
    RUN  = sorted(list(filter(lambda x: "Walk" in x, zombies)))    

class Sprites:
    def __init__(self, window, x, y, scale, sprite, location):
        self.window  = window
        self.x       = x
        self.y       = y
        self.scale   = scale
        self._index  = 0
        self.sprite = sprite
        self.state   = sprite.RUN
        self.location = location
        self.object = None

        self._loop_stack = []

    def change_position(self, x, y):
        self.x = x 
        self.y = y

    def display_state(self, flip=False):
        try:
            self.state[self._index]

        except IndexError:
            self._index = 0

        finally:
            img = image.load(f"{self.location}/{self.state[self._index]}").convert()
                
            resize = transform.scale(img, (img.get_width () * self.scale, img.get_height() * self.scale))
            self.object = transform.flip(resize, flip, False)
            self.window.blit(self.object, (self.x, self.y))

            if self._index == len(self.state) - 1 and self._loop_stack:
                self._index = 0
            self._index += 1

class Zombie(Sprites):
    def __init__(self, window, x, y, scale):
        super().__init__(window, x, y, scale, ZombieSprite, "./assets/")