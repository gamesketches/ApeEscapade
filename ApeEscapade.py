import os, pygame, sys
from pygame.locals import *

main_dir = os.path.split(os.path.abspath(sys.argv[0]))[0]
data_dir = os.path.join(main_dir, 'data')

TERMINALVELOCITY = 2

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
        self.terminalVelocity = 2
        self.velocity = [0,0]
        self.net = False
        self.timer = 0
        self.grounded = False

    def update(self):
        "Move character, start netting if commanded, update counter"
        if self.net:
            self.timer += 0
            if self.timer > 30:
                self.net = False
                self.timer = 0
        if not self.grounded:
            #self.rect = self.rect.move((0,1))
            if self.velocity[1] <= TERMINALVELOCITY:
                self.velocity[1] += 1
        if pygame.key.get_pressed()[K_RIGHT]:
            #self.rect = self.rect.move((1,0))
            self.velocity[0] += 1
        elif pygame.key.get_pressed()[K_LEFT]:
            #self.rect = self.rect.move((-1,0))
            self.velocity[0] += -1
        elif pygame.key.get_pressed()[K_UP]:
            self.velocity[1] += -1
        if pygame.key.get_pressed()[K_SPACE]:
            self.net = True

        self.rect = self.rect.move((self.velocity[0],self.velocity[1]))

    def checkGrounded(self, groundRect):
        if self.rect.colliderect(groundRect):
            self.grounded = True
            self.rect = self.rect.move(0,-1)
            self.velocity[1] = 0

class Monkey(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image, self.rect = load_image('monkey.bmp')
        self.moveRate = 5

    def update(self):
        self.rect = self.rect.move((5,0))

def main():
    pygame.init()
    screen = pygame.display.set_mode((700, 400))
    pygame.display.set_caption('Ape Escapade!')
    pygame.mouse.set_visible(0)

    background = pygame.Surface(screen.get_size())
    background = background.convert()
    background.fill((250, 250, 250))

    ground = pygame.Surface((700, 50))
    ground = ground.convert()
    ground.fill((0,0,0))

    groundRect = pygame.Rect(0, 350, 700, 50)

    screen.blit(background, (0,0))
    screen.blit(ground,(0,350))
    pygame.display.flip()
    
    spike = Player()

    monkey = Monkey()
    allsprites = pygame.sprite.Group()
    allsprites.add(spike, monkey)

    clock = pygame.time.Clock()

    while True:
        clock.tick(60)
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
            elif event.type == KEYDOWN and event.key == K_ESCAPE:
                pygame.quit()

        spike.checkGrounded(groundRect)
        allsprites.update()
        allsprites.draw(screen)
        pygame.display.flip()

if __name__ == '__main__':
    main()
