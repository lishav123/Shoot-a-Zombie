from pygame import transform
from pygame import image

from os import listdir

zombies = listdir('./assets/')

# Basic structure for zombie sprites
class ZombieSprite:
    RUN  = sorted(list(filter(lambda x: "Walk" in x, zombies))) 

# Basic structure for sprites
class Sprites:
    def __init__(self, window, x, y, scale, sprite, location):
        '''
           Arguments:
               window: the game window
               x: x-axis position of the sprite
               y: y-axis position of the sprite
               scale: size of the sprite twiching it will grow the size of image by keeping in mind that it grows according to ratios
               sprite: a class with arugment of location of different activity
               location: location of the the folder where sprite exists
        '''
        self.window  = window
        self.x       = x
        self.y       = y
        self.scale   = scale
        self._index  = 0 # defines the current index of image
        self.sprite = sprite
        self.state   = sprite.RUN # defines the state or different activity of sprite mention in class with locations like ZombieSprite class
        self.location = location
        self.object = None # contains the object of image given by pygame.image

        self._loop_stack = [] # for making a animation complete before switching, let's say there is animation [run1, run2, run3, run4, run5] 
        # and user change the event to jump, in genreal what will happen is, let's the current value is "run2" then suddenly after event it will 
        # now use jump, note that whole cycle of run ain't completed yet, so _loop_stack is used when you want a complete cycle of animation instead
        # of a sudden change if _loop_stack is not empty then run2 is there and user change the event event that time also first run2 will go till run5 after that jump will happen 

    def change_position(self, x, y):
        '''
         Args:
          x: x position of your sprite
          y: y position of your sprite
        It changes the position of your sprite in (x, y) coords.
        '''
        self.x = x 
        self.y = y

    def is_inside_area(self, x, y):
        '''
         Args:
           x: x position of external point
           y: y position of external point

        Return:
           bool

        It checke weather the external point is inside of your sprite area
        '''
        x0, y0 = self.x, self.y 
        x_, y_ = self.x + self.object.get_width(), self.y + self.object.get_height()

        return x0 < x < x_ and y0 < y < y_ 

    def display_state(self, flip=False):
        try:
            self.state[self._index]

        except IndexError:
            self._index = 0

        finally:
            img = image.load(f"{self.location}/{self.state[self._index]}")
                
            resize = transform.scale(img, (img.get_width () * self.scale, img.get_height() * self.scale))
            self.object = transform.flip(resize, flip, False)
            self.window.blit(self.object, (self.x, self.y))

            if self._index == len(self.state) - 1 and self._loop_stack:
                self._index = 0
            self._index += 1

class Zombie(Sprites):
    def __init__(self, window, x, y, scale):
        super().__init__(window, x, y, scale, ZombieSprite, "./assets/")
