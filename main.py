# importing
import pygame
pygame.init()
from random import randint

# settings
FPS = 60
score = 0
LM_score = 0
clock = pygame.time.Clock()

wind_w, wind_h = 700, 500
window = pygame.display.set_mode((wind_w , wind_h))
pygame.display.set_caption("SHOOTER")

background = pygame.image.load("bg.jfif")
background = pygame.transform.scale(background, (wind_w , wind_h))

# music
pygame.mixer.music.load("music.mp3")
pygame.mixer.music.set_volume(0.3)
pygame.mixer.music.play(-1)

vistrel = pygame.mixer.Sound("vistrel.mp3")

# classes
class Sprite:
    def __init__(self , x , y , w , h, img):
        self.img = img
        self.rect = pygame.Rect(x, y, w, h)
        self.img = pygame.transform.scale(self.img , (w, h))
    
    def draw(self):
        window.blit(self.img , (self.rect.x, self.rect.y))
        
class Player(Sprite):
    def __init__(self , x , y , w , h , img1, img2 , speed):
        super().__init__(x, y, w, h, img1)
        self.img_r = self.img
        self.img_l = pygame.transform.scale(img2, (w, h))
        self.speed = speed
        self.speed = speed
    
    def move(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_a]:
            self.img = self.img_l
            if self.rect.x > 0:
                self.rect.x -= self.speed
        if keys[pygame.K_d]:
            self.img = self.img_r
            if self.rect.right < wind_w:
                self.rect.x += self.speed
    
    def FIRE(self):
        BULLETS.append(Bullet(self.rect.centerx, self.rect.top, 25, 50, bullet_img, 3))
        vistrel.play()

class Enemy(Sprite):
    def __init__(self , x , y , w , h , img1 , speed):
        super().__init__(x, y, w, h, img1)
        self.speed = speed
    
    def move(self):
        global LM_score
        self.rect.y += self.speed
        self.rect.x += self.speed * randint(-difficult_coof, difficult_coof)
        if self.rect.y >= wind_h:
            LM_score += 1
            self.rect.y = randint(-250, -50)
            self.rect.x = randint(0, wind_w-50)
        
    def die(self):
        global score
        self.rect.y = randint(-250, -50)
        self.rect.x = randint(0, wind_w-50)
        score += 1

class Meteor(Sprite):
    def __init__(self , x , y , w , h , img1 , speed, hp):
        super().__init__(x, y, w, h, img1)
        self.speed = speed
        self.hp = hp
    
    def move(self):
        global LM_score
        self.rect.y += self.speed
        self.rect.x += self.speed * randint(-difficult_coof, difficult_coof)
        if self.rect.y >= wind_h:
            LM_score += 1
            self.rect.y = randint(-250, -50)
            self.rect.x = randint(0, wind_w-50)
    
    def take_damage(self):
        global score
        if self.hp >= 1:
            self.hp -= 1
        else:
            self.rect.y = randint(-250, -50)
            self.rect.x = randint(0, wind_w-50)
            score += 1
            
class Bullet(Sprite):
    def __init__(self, x, y, w, h, img, speed):
        super().__init__(x, y, w, h, img)
        self.speed = speed
    
    def move(self):
        self.rect.y -= self.speed
        self.rect.x += self.speed * randint(-difficult_coof, difficult_coof)
        if self.rect.bottom <= 0:
            BULLETS.remove(self)

# variables & lists
difficult_coof = 1
font = pygame.font.SysFont("Comfortaa" , 50)
font2 = pygame.font.SysFont("Comfortaa" , 20)
font3 = pygame.font.SysFont("Comfortaa" , 35)
score_font = pygame.font.SysFont("Comfortaa" , 35)
lose_font = pygame.font.SysFont("Comfortaa" , 35)
win = font.render("You win!", True, (0, 100, 0))
lose = font.render("You lose(", True, (100, 0, 0))
reset = font.render("Press R to reset", True, (255, 255, 255))
score_txt = font.render(str(score), True, (255, 255, 255))

p_img1 = pygame.image.load("Player.png")
p_img2 = pygame.transform.flip(p_img1, True, False)
player = Player(35, 400, 50, 40, p_img1, p_img2, 5)

enemy_img = pygame.image.load("govno.png")
meteor_img = pygame.image.load("meteor.png")
bullet_img = pygame.image.load("bullet.png")
ENEMIES = []
METEORS = []
BULLETS = []
for i in range(5):
    a = randint(0, 1)
    if a == 1:
        ENEMIES.append(Enemy(randint(0, wind_w-50), randint(-250, -50), 50, 40, enemy_img, 3))
    else:
        METEORS.append(Meteor(randint(0, wind_w-50), randint(-250, -50), 50, 40, meteor_img, 3, 3))

# game loop
game = True
finish = False
while game:
    if not finish:
        window.blit(background, (0, 0))
        score_txt = font.render(str(score), True, (255, 255, 255))
        window.blit(score_txt, (0, 0))
        LM_score_txt = font.render(str(LM_score), True, (255, 255, 255))
        window.blit(LM_score_txt, (0, wind_h-35))
        
        if any(player.rect.colliderect(enemy.rect) for enemy in ENEMIES) or any(player.rect.colliderect(meteor.rect) for meteor in METEORS) or LM_score >= 50:
            window.blit(lose, (200, 200))
            window.blit(reset, (200, 250))
            finish = True
            
        player.draw()
        player.move()
        for enemy in ENEMIES:
            if any(enemy.rect.colliderect(bullet.rect) for bullet in BULLETS):
                enemy.die()
                BULLETS.remove(bullet)
            enemy.draw()
            enemy.move()
        
        for meteor in METEORS:
            if any(meteor.rect.colliderect(bullet.rect) for bullet in BULLETS):
                meteor.take_damage()
                BULLETS.remove(bullet)
            meteor.draw()
            meteor.move()
        
        for bullet in BULLETS:
            bullet.draw()
            bullet.move()
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            finish = True
        
        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            player.FIRE()
            
            
        if event.type == pygame.KEYDOWN and event.key == pygame.K_r and finish == True:
            finish = False
            score = 0
            LM_score = 0
            player = Player(35, 400, 50, 40, p_img1, p_img2, 5)
            ENEMIES = []
            METEORS = []
            BULLETS = []
            for i in range(5):
                a = randint(0, 1)
                if a == 1:
                    ENEMIES.append(Enemy(randint(0, wind_w-50), randint(-250, -50), 50, 40, enemy_img, 3))
                else:
                    METEORS.append(Meteor(randint(0, wind_w-50), randint(-250, -50), 50, 40, meteor_img, 3, 3))
    
    pygame.display.update()
    clock.tick(FPS)
    