from pygame import *
from random import randint
from time import time as timer

class GameSprite(sprite.Sprite):

    def __init__(self, player_image, player_x, player_y, player_speed):
        super().__init__()
        self.image = transform.scale( image.load(player_image), (70,70))
        self.speed = player_speed
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y

    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

bullet_group = sprite.Group()

class Player(GameSprite):
    def __init__(self, player_image, player_x, player_y, player_speed):
        super().__init__(player_image, player_x, player_y, player_speed)

    def update(self):
        keys_pressed = key.get_pressed()
        if keys_pressed[K_a] and self.rect.x > 0:
            self.rect.x -= self.speed
        if keys_pressed[K_d] and self.rect.x < 650:
            self.rect.x += self.speed

    def fire(self):
    
        bullet = Bullet("bullet.png", self.rect.centerx, self.rect.top, 5)
        bullet_group.add(bullet)

lost = 0

class Enemy(GameSprite):
    def __init__(self, player_image, player_x, player_y, player_speed):
        super().__init__(player_image, player_x, player_y, player_speed)

    def update(self):

        global lost

        if self.rect.y <= 450:
            self.rect.y += self.speed

        else:
            self.rect.x = randint(1, 630)
            self.speed = randint(1, 3)
            self.rect.y = 0
            lost = lost + 1

class Bullet(GameSprite):
    def __init__(self, player_image, player_x, player_y, player_speed):
        super().__init__(player_image, player_x, player_y, player_speed)
        self.image = transform.scale( image.load(player_image), (10,10))
    
    def update(self):
        self.rect.y -= self.speed

        if self.rect.y < 0:
                self.kill()


window = display.set_mode((700, 500))
display.set_caption("Супер мега крутой шутер 2к 23")

background = transform.scale(image.load("galaxy.jpg"), (700, 500))

mixer.init()
mixer.music.load("space.ogg")
mixer.music.play()
fire = mixer.Sound("fire.ogg")

clock = time.Clock()
FPS = 60

sprite1 = Player(("rocket.png"), 50, 420, 10)

ufo_group = sprite.Group()
asteroid_group = sprite.Group()

for i in range(5):
    ufo = Enemy("ufo.png", randint(1, 630), 0, randint(1,3))

    ufo_group.add(ufo)

for i in range(3):
    asteroid = Enemy("asteroid.png", randint(1, 630), 0, randint(1, 3))

    asteroid_group.add(asteroid)

font.init()
font = font.SysFont("Arial", 20)

points = 0

run = True
finish = False

while run:

    for e in event.get():
        if e.type == QUIT:
            run = False 

    if finish != True:

        window.blit(background,(0, 0))
        lost_text = font.render("Пропущено:"+str(lost), True, (206, 234, 240))
        window.blit(lost_text, (20, 20))
        lost_text = font.render("Счёт:"+str(points), True, (206, 234, 240))
        window.blit(lost_text, (20, 40))

        clock.tick(FPS)

        sprite1.reset()
        sprite1.update()
        
        ufo_group.draw(window)
        ufo_group.update()

        asteroid_group.draw(window)
        asteroid_group.update()


        bullet_group.draw(window)
        bullet_group.update()
        keys_pressed = key.get_pressed()

        num_fire = 0
        rel_time = False

        if keys_pressed[K_SPACE] and num_fire < 5 and rel_time == False:

            sprite1.fire()
            num_fire += 1
            fire.play()

        if num_fire >= 5 and rel_time == False:

            time1 = timer()
            rel_time = True

        if num_fire >= 5 and rel_time == True:

            time2 = timer()
            time3 = time2 - time1

            if time3 >= 3 and rel_time == True:

                rel_time = False
                num_fire = 0


        if lost >= 10:
            
            lost_text = font.render("YOU LOSE ...", True, (206, 234, 240))
            window.blit(lost_text, (320, 250))

            finish = True


        if sprite.groupcollide(ufo_group, bullet_group, True, True):
            points += 1
            ufo = Enemy("ufo.png", randint(1, 700), 0, randint(1,4))

            ufo_group.add(ufo)

        if points >= 10:

            lost_text = font.render("YOU WIN !", True, (206, 234, 240))
            window.blit(lost_text, (320, 250))

            finish = True

        if sprite.spritecollide(sprite1, ufo_group, False):
            lost_text = font.render("YOU LOSE ...", True, (206, 234, 240))
            window.blit(lost_text, (320, 250))

            finish = True

        if sprite.spritecollide(sprite1, asteroid_group, False):
            lost_text = font.render("YOU LOSE ...", True, (206, 234, 240))
            window.blit(lost_text, (320, 250))

            finish = True

        display.update()