import os, pygame, sys
from pygame.locals import *

main_dir = os.path.split(os.path.abspath(sys.argv[0]))[0]
data_dir = os.path.join(main_dir, 'data')

TERMINALVELOCITY = 2
TERMINALHORIZONTALVELOCITY = 5
NETTIME = 30

allsprites = pygame.sprite.Group()

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
            self.timer += 1
            if self.timer > NETTIME:
                self.net = False
                self.timer = 0
        if not self.grounded:
            #vertical velocity deterioration
            if self.velocity[1] <= TERMINALVELOCITY:
                self.velocity[1] += 1
        else:
            #horizontal velocity deterioration
            if self.velocity[0] > 0:
                self.velocity[0] -= 0.3
            else:
                self.velocity[0] += 0.3

        # input handling
        if pygame.key.get_pressed()[K_RIGHT] and self.velocity[0] < TERMINALHORIZONTALVELOCITY \
           and not self.net:
            self.velocity[0] += 1
        elif pygame.key.get_pressed()[K_LEFT] and self.velocity[0] > -TERMINALHORIZONTALVELOCITY \
             and not self.net:
            self.velocity[0] += -1
        elif pygame.key.get_pressed()[K_UP] and self.grounded:
            self.velocity[1] += -20
            self.grounded = False
        if pygame.key.get_pressed()[K_SPACE] and not self.net:
            self.net = True
            allsprites.add(Net(self.rect.x +self.rect.width, self.rect.y))
        #Add in changes to velocity
        self.rect = self.rect.move((self.velocity[0],self.velocity[1]))

    def checkGrounded(self, groundRect):
        if groundRect.colliderect(self.rect.move(0,self.velocity[1])):
            self.grounded = True
            self.velocity[1] = 0
            self.rect 
            return True

class Net(pygame.sprite.Sprite):
    def __init__(self, startingX,startingY):
        pygame.sprite.Sprite.__init__(self)
        self.image, self.rect = load_image('net.bmp')
        self.rect = self.rect.move((startingX,startingY))
        self.timer = 0

    def update(self):
        self.timer += 1
        if self.timer >= NETTIME:
            self.kill()

class Monkey(pygame.sprite.Sprite):
    def __init__(self, leftBound=0, rightBound=700):
        pygame.sprite.Sprite.__init__(self)
        self.image, self.rect = load_image('monkey.bmp')
        self.moveRate = 5
        self.rightBound = rightBound
        self.leftBound = leftBound

    def update(self):
        self.rect = self.rect.move((self.moveRate,0))
        if self.rect.x >= self.rightBound or self.rect.x <= self.leftBound:
            self.moveRate *= -1
        for i in allsprites.sprites():
            if type(i) == Net:
                if self.rect.colliderect(i.rect):
                    self.kill()

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

    platform = pygame.Surface((400, 50))
    platform = platform.convert()
    platform.fill((250,0,0))

    platformRect = pygame.Rect(300, 150, 400, 50)

    screen.blit(background, (0,0))
    screen.blit(ground,(0,350))
    screen.blit(platform, platformRect.topleft)
    pygame.display.flip()
    
    spike = Player()

    monkey1 = Monkey(100, 500)
    monkey1.rect = monkey1.rect.move(100, 220)
    monkey2 = Monkey(300, 700)
    monkey2.rect = monkey2.rect.move(350, 20)
    allsprites.add(spike, monkey1, monkey2)

    clock = pygame.time.Clock()

    while True:
        clock.tick(60)
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
            elif event.type == KEYDOWN and event.key == K_ESCAPE:
                pygame.quit()

        screen.blit(background, (0,0))
        screen.blit(ground,(0,350))
        screen.blit(platform,platformRect.topleft)
        
        if not spike.checkGrounded(groundRect) and not spike.checkGrounded(platformRect):
            spike.grounded = False
        allsprites.update()
        allsprites.draw(screen)
        pygame.display.flip()

if __name__ == '__main__':
    main()
