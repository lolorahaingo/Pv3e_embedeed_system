# @Author: rahaingomanana <laurent>
# @Date:   2018-01-31T10:14:36+01:00
# @Email:  laurent.rahaingomanana@estaca.eu
# @Filename: Sprite.py
# @Last modified by:   laurent
# @Last modified time: 2020-10-05T21:02:12+02:00



def main():
    pass

if __name__ == '__main__':
    main()
import pygame
from pygame import *
import random


FPS = 60

# Couleurs
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

nb_mobs = 4
speedy_mob_max = 8
speedy_mob_min = 3

# Initialisation
pygame.init()
screen_s = pygame.display.Info()
WIDTH = int(0.35*screen_s.current_w)
HEIGHT = int(0.55*screen_s.current_h)
pygame.mixer.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Test")
clock = pygame.time.Clock()

font_name = pygame.font.match_font('comic sans ms')
def draw_text(surf, text, size, x, y, color):
    font = pygame.font.Font(font_name, size)
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x, y)
    surf.blit(text_surface, text_rect)

def mob_c():
    m = random.choice(mob_choice)
    if m == 'm1':
        m = Oeuf_mob()
        all_sprites.add(m)
        oeufs.add(m)
    elif m == 'm2':
        m = Tomate_mob()
        all_sprites.add(m)
        tomates.add(m)

def high_score():
    fichier=open("record.txt","r")
    fichier.read()
    fichier.seek(0)
    high=fichier.readline()
    if float(score)>float(high):
        fichier.seek(0)
        print("Le nouveau record est de : ",score)
        print("L'ancien record etait de : ",fichier.read())
        high=score
        high=str(high)
        fichier.close()
        fichier=open("record.txt","w")
        fichier.write(high)
        fichier.close()
    else:
        print("Votre score est de : ",score)
        fichier.seek(0)
        print( "Vous n'avez pas battu le record qui est de : ",fichier.read())
        fichier.close()


class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)

        self.image = pygame.transform.scale(player_img, (110, 88))
        self.rect = self.image.get_rect()
        self.radius = 47
        #pygame.draw.circle(self.image, RED, self.rect.center, self.radius)
        self.rect.centerx = WIDTH / 2
        self.rect.bottom = HEIGHT - 10
        self.last_shot = pygame.time.get_ticks()
        self.power_time = pygame.time.get_ticks()
        self.power = 1
        shoot_delay = 400

    def update(self):
        now = pygame.time.get_ticks()
        if self.power >= 2 and now - self.power_time > powerup_time:
            self.power -= 1
            self.power_time = now

        self.speedx = 0
        self.speedy = 0
        keystate = pygame.key.get_pressed()
        if keystate[pygame.K_LEFT]:
            self.speedx = -5
        if keystate[pygame.K_RIGHT]:
            self.speedx = 5
        self.rect.x += self.speedx
        if keystate[pygame.K_UP]:
            self.speedy = -5
        if keystate[pygame.K_DOWN]:
            self.speedy = 5
        if keystate[pygame.K_SPACE]:
            self.shoot_poele()
        if keystate[pygame.K_LALT]:
            self.shoot_couteau()
        self.rect.x += self.speedx
        self.rect.y += self.speedy

    # Collision
        if self.rect.right > 50 + WIDTH:
            self.rect.right = 50 +WIDTH
        if self.rect.left < -50:
            self.rect.left = -50
        if self.rect.top < 2*HEIGHT / 3:
            self.rect.top = 2*HEIGHT / 3
        if self.rect.bottom > HEIGHT:
            self.rect.bottom = HEIGHT

    def shoot_poele(self):
        if self.power == 1:
            self.shoot_delay = 400
        elif self.power >= 2:
            self.shoot_delay = 200
        now = pygame.time.get_ticks()
        if now - self.last_shot > self.shoot_delay:
            shoot_snd.play()
            self.last_shot = now
            self.image = pygame.transform.scale(persod_img, (110, 88))
            poele = Poele(self.rect.centerx, self.rect.top)
            all_sprites.add(poele)
            poeles.add(poele)



    def shoot_couteau(self):
        if self.power == 1:
            self.shoot_delay = 400
        elif self.power >= 2:
            self.shoot_delay = 200
        now = pygame.time.get_ticks()
        if now - self.last_shot > self.shoot_delay:
            shoot_snd.play()
            self.last_shot = now
            self.image = pygame.transform.scale(persog_img, (110, 88))
            couteau = Couteau(self.rect.centerx, self.rect.top)
            all_sprites.add(couteau)
            couteaux.add(couteau)

class Oeuf_mob(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.type = 'oeuf'
        self.image_orig = pygame.transform.scale(mobs_images[self.type], (39, 50))
        self.image = self.image_orig.copy()
        self.rect = self.image.get_rect()
        self.radius = int(self.rect.width *0.85/ 2)
        #pygame.draw.circle(self.image, RED, self.rect.center, self.radius)
        self.rect.x = random.randrange(WIDTH - self.rect.width)
        self.rect.y = random.randrange(-100, -40)
        self.speedy = random.randrange(speedy_mob_min, speedy_mob_max)
        self.speedx = random.randrange(-2, 2)
        self.rot = 0
        self.rot_speed = random.randrange(-8, 8)
        self.last_update = pygame.time.get_ticks()

    def rotate(self):
        now = pygame.time.get_ticks()
        if now - self.last_update > 50:
            self.last_update = now
            self.rot = (self.rot + self.rot_speed) % 360
            new_image = pygame.transform.rotate(self.image_orig, self.rot)
            old_center = self.rect.center
            self.image = new_image
            self.rect = self.image.get_rect()
            self.rect.center = old_center

    def update(self):
        self.rotate()
        self.rect.x += self.speedx
        self.rect.y += self.speedy
        if self.rect.top > HEIGHT + 10 or self.rect.left < -45 or self.rect.right > WIDTH + 45:
            self.rect.x = random.randrange(WIDTH - self.rect.width)
            self.rect.y = random.randrange(-100, -40)
            self.speedy = random.randrange(speedy_mob_min, speedy_mob_max)

class Tomate_mob(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.type = 'tomate'
        self.image_orig = pygame.transform.scale(mobs_images[self.type], (39, 50))
        self.image = self.image_orig.copy()
        self.rect = self.image.get_rect()
        self.radius = int(self.rect.width *0.85/ 2)
        #pygame.draw.circle(self.image, RED, self.rect.center, self.radius)
        self.rect.x = random.randrange(WIDTH - self.rect.width)
        self.rect.y = random.randrange(-100, -40)
        self.speedy = random.randrange(speedy_mob_min, speedy_mob_max)
        self.speedx = random.randrange(-2, 2)
        self.rot = 0
        self.rot_speed = random.randrange(-8, 8)
        self.last_update = pygame.time.get_ticks()

    def rotate(self):
        now = pygame.time.get_ticks()
        if now - self.last_update > 50:
            self.last_update = now
            self.rot = (self.rot + self.rot_speed) % 360
            new_image = pygame.transform.rotate(self.image_orig, self.rot)
            old_center = self.rect.center
            self.image = new_image
            self.rect = self.image.get_rect()
            self.rect.center = old_center

    def update(self):
        self.rotate()
        self.rect.x += self.speedx
        self.rect.y += self.speedy
        if self.rect.top > HEIGHT + 10 or self.rect.left < -45 or self.rect.right > WIDTH + 45:
            self.rect.x = random.randrange(WIDTH - self.rect.width)
            self.rect.y = random.randrange(-100, -40)
            self.speedy = random.randrange(speedy_mob_min, speedy_mob_max)

class Poele(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image_orig = pygame.transform.scale(poele_img, (33, 50))
        self.image = self.image_orig.copy()
        self.rect = self.image.get_rect()
        self.rect.bottom = y + 85
        self.rect.centerx = x + 35
        self.speedy = -7
        self.speedx = 0.5

    def update(self):
        self.rect.y += self.speedy
        self.rect.x += self.speedx
        if self.rect.bottom < 0:
            self.kill()

class Couteau(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image_orig = pygame.transform.scale(couteau_img, (14, 50))
        self.image = self.image_orig.copy()
        self.rect = self.image.get_rect()
        self.rect.bottom = y + 85
        self.rect.centerx = x - 35
        self.speedy = -7
        self.rot = 0
        self.rot_speed = 6
        self.last_update = pygame.time.get_ticks()

    def rotate(self):
        now = pygame.time.get_ticks()
        if now - self.last_update > 50:
            self.last_update = now
            self.rot = (self.rot + self.rot_speed) % 360
            new_image = pygame.transform.rotate(self.image_orig, self.rot)
            old_center = self.rect.center
            self.image = new_image
            self.rect = self.image.get_rect()
            self.rect.center = old_center


    def update(self):
        self.rotate()
        self.rect.y += self.speedy
        if self.rect.bottom <0:
            self.kill()

class Oeuf_ex(pygame.sprite.Sprite):
    def __init__(self, center):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(oeufex_img, (50, 50))
        self.rect = self.image.get_rect()
        self.rect.center = center
        self.frame = 0
        self.last_update = pygame.time.get_ticks()
        self.delay = 700

    def update(self):
        now = pygame.time.get_ticks()
        if now - self.last_update > self.delay:
            self.kill()

class Tomate_ex(pygame.sprite.Sprite):
    def __init__(self, center):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(tomateex_img, (54, 50))
        self.rect = self.image.get_rect()
        self.rect.center = center
        self.last_update = pygame.time.get_ticks()
        self.delay = 700

    def update(self):
        now = pygame.time.get_ticks()
        if now - self.last_update > self.delay:
            self.kill()

class Powup(pygame.sprite.Sprite):
    def __init__(self, center):
        pygame.sprite.Sprite.__init__(self)
        self.type = random.choice(['lenteur' , 'dopage'])
        self.image_orig = powups_images[self.type ]
        self.image = self.image_orig.copy()
        self.rect = self.image.get_rect()
        self.rect.center = center
        self.speedy = 2

    def update(self):
        self.rect.y += self.speedy
        if self.rect.bottom < 0:
            self.kill()


#Grapgics
background_img = pygame.image.load('Sprites/fondjeu.png').convert()
background = pygame.transform.scale(background_img, (WIDTH, HEIGHT))
background_rect = background.get_rect()
player_img = pygame.image.load("Sprites/perso.png")
poele_img = pygame.image.load("Sprites/poele.png")
oeuf1_img = pygame.image.load("Sprites/oeuf1.png")
couteau_img = pygame.image.load("Sprites/couteau.png")
tomateex_img = pygame.image.load("Sprites/tomate0.png")
oeufex_img = pygame.image.load("Sprites/oeuf1.png")
persod_img = pygame.image.load("Sprites/persoR.png")
persog_img = pygame.image.load("Sprites/persol.png")

powups_images = {}
powups_images['lenteur'] = pygame.transform.scale(pygame.image.load('Sprites/hotdog.png'),(45,25))
powups_images['dopage'] = pygame.image.load('Sprites/sodafinal.png')

mobs_images = {}
mobs_images['tomate'] = pygame.image.load('Sprites/tomate.png')
mobs_images['oeuf'] = pygame.image.load('Sprites/oeuf.png')
mob_choice = ['m1', 'm2']


# Sounds
music = pygame.mixer.Sound('Sounds/soundtrack.ogg')
shoot_snd = pygame.mixer.Sound('Sounds/lancer.wav')
pow_snd = pygame.mixer.Sound('Sounds/powerup.wav')


all_sprites = pygame.sprite.Group()
Player = Player()
all_sprites.add(Player)
poeles = pygame.sprite.Group()
couteaux = pygame.sprite.Group()
oeufs = pygame.sprite.Group()
tomates = pygame.sprite.Group()
powups = pygame.sprite.Group()
score = 0
score_q = 1
powerup_time = 5000

fichier=open("record.txt","r")
fichier.read()
fichier.seek(0)
high=fichier.readline()


for i in range(nb_mobs):
    mob_c()

music.play(loops = -1)
# Boucle Jeu
running = True
while running:
    # keep loop running at the right speed
    #back_snd.play()
    clock.tick(FPS)
    # Process input (events)
    for event in pygame.event.get():
        # check for closing window
        if event.type == pygame.QUIT:
            running = False
        if event.type == KEYUP:
            if event.key == K_SPACE:
                Player.image = pygame.transform.scale(player_img, (110, 88))
            if event.key == K_LALT:
                Player.image = pygame.transform.scale(player_img, (110, 88))



    # Update
    all_sprites.update()

    hits = pygame.sprite.groupcollide(oeufs, poeles, True, True)
    for hit in hits:
        score += 5
        b = Oeuf_ex(hit.rect.center)
        all_sprites.add(b)
        if random.random() > 0.85:
            pow = Powup(hit.rect.center)
            all_sprites.add(pow)
            powups.add(pow)
        mob_c()

    hits = pygame.sprite.groupcollide(tomates, couteaux, True, True)
    for hit in hits:
        score += 5
        b = Tomate_ex(hit.rect.center)
        all_sprites.add(b)
        if random.random() > 0.85:
            pow = Powup(hit.rect.center)
            all_sprites.add(pow)
            powups.add(pow)
        mob_c()

    hits = pygame.sprite.spritecollide(Player, oeufs, False, pygame.sprite.collide_circle)
    if hits:
        high_score()
        running = False

    hits = pygame.sprite.spritecollide(Player, tomates, False, pygame.sprite.collide_circle)
    if hits:
        high_score()
        running = False

    hits = pygame.sprite.spritecollide(Player, powups, True)
    for hit in hits:
        pow_snd.play()
        if hit.type == 'lenteur':
            speedy_mob_max = 4
            speedy_mob_min = 1


        elif hit.type == 'dopage' :
            Player.power_time = pygame.time.get_ticks()
            Player.power += 1

    if score == score_q*25:
        score_q += 1
        mob_c()

    # Rendu
    screen.blit(background, background_rect)
    all_sprites.draw(screen)

    # Text
    draw_text(screen, str(score), 25, (WIDTH/2)+10, 10, WHITE)
    draw_text(screen, 'Shoot power :', 17, 70, 75, WHITE)
    draw_text(screen, str(Player.power), 17, 133, 75, WHITE)
    draw_text(screen, str(high), 25, 9.66*WIDTH/10, 10, WHITE)
    # Rafraichissement
    pygame.display.flip()

pygame.quit()
