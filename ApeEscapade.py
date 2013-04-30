import os, pygame, sys
from pygame.locals import *

def load_image(name, colorkey=None):
    fullname = os.path.join(data_dir, name)
    try:
        image = pygame.image.load(fullname)
    except pygame.error:
        print('Cannot load image:', fullname)
        raise SystemExit(str(geterror()))
    image = image.convert()
    if colorkey is not None:
        if colorkey is -1:
            colorkey = image.get_at((0,0))
        image.set_colorkey(colorkey, RLEACCEL)
    return image, image.get_rect()

class Player(pygame.sprite.Sprite):
    """Player Object, walks around and casts his net"""
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image, self.rect = load_image("spike.bmp")
        self.moveRate = 10
        self.net = False
        self.timer = 0

    def update(self):
        "Move character, start netting if commanded, update counter"
        if self.net:
            self.timer += 0
            if self.timer > 30:
                self.net = False
                self.timer = 0
        
