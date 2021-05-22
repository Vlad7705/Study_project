#Создай собственный Шутер!

from pygame import *
from random import *



class GameSprite(sprite.Sprite):
    def __init__(self, player_image, player_x, player_y, size_x, size_y, player_speed):
        super().__init__()
        self.image = transform.scale(image.load(player_image), (size_x,size_y))
        self.speed = player_speed
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y
    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

bullets = sprite.Group( )

class Player(GameSprite):
    def update(self):
        key_pressed = key.get_pressed()
        if key_pressed[K_a] and self.rect.x > 5:
            self.rect.x -= self.speed
        if key_pressed[K_d] and self.rect.x < 700 - 80:
            self.rect.x += self.speed
    def fire(self):
        bullet = Granata("NightmareMangle.png", self.rect.centerx, self.rect.top, 15, 20, -15)
        bullets.add(bullet)
       
lost = 0

font.init()
font = font.Font(None, 70)
lose = font.render('You lose!', True, (255, 215, 0))

class Enemy(GameSprite):
    def update(self):
        self.rect.y += self.speed
        global lost
        if self.rect.y > 500:
            self.rect.x = randint(80, 620)
            self.rect.y = 0
            lost = lost + 1

class Granata(GameSprite):
    def update(self):
        self.rect.y += self.speed
        if self.rect.y < 0:
            self.kill()

class Meteorit(GameSprite):
    def update(self):
        if self.rect.x < 1:
            self.side = "right"
        elif self.rect.x > 690:
            self.side = "left"
        if self.side == "left":
            self.rect.x -= self.speed
            self.rect.y += 5
        else:
            self.rect.x += self.speed
            self.rect.y += 5
        if self.rect.y == 500:
            self.rect.y = 0

window = display.set_mode((700,500))
display.set_caption("8-bit shooter")
background = transform.scale(image.load("galaxy.jpg"),(700,500))

raketa = Player("Nightmare_Extra.png", 5, 500 - 80, 80, 100, 10)

vragi = sprite.Group()
for i in range(1, 6):
    vrag = Enemy("NFoxy_Extra.png", randint(80, 620), -40, 80, 50, randint(1, 5))
    vragi.add(vrag)

asteroidi = sprite.Group()

for i in range(1, 6):
    num = randint(1,2)
    if num == 1:
        t = 0
    else:
        t = 700
    asteroid = Meteorit("73.png", t, -40, 80, 50, randint(1, 5))
    asteroidi.add(asteroid)

game = True
finish = False
max_lost = 100
score = 0 
clock = time.Clock()
FPS = 60

mixer.init()
mixer.music.load('space.ogg')
mixer.music.play()

while game:
    for e in event.get():
        if e.type == QUIT:
            game = False

        elif e.type == KEYDOWN:
            if e.key == K_SPACE:
                raketa.fire()
    
    if not finish:
        window.blit(background,(0,0))
    
        raketa.update()
        vragi.update()
        bullets.update()
        asteroidi.update()

        raketa.reset()
        vragi.draw(window)
        bullets.draw(window)
        asteroidi.draw(window)

        collides = sprite.groupcollide(vragi, bullets, True, True)
        for c in collides:
            score = score + 1
            vrag = Enemy("NFoxy_Extra.png", randint(80, 620), -40, 80, 50, randint(1, 5))
            vragi.add(vrag)

        for c in collides:
            asteroid = Meteorit("73.png", randint(1, 2), -40, 80, 50, randint(1, 5))
            asteroidi.add(asteroid)

        if sprite.spritecollide(raketa, vragi, False) or lost >= max_lost:
            finish = True
            window.blit(lose, (200, 200))

        display.update()
        clock.tick(FPS)