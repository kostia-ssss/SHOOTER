import pygame
pygame.init()
from random import randint


FPS = 60
clock = pygame.time.Clock()

wind_w, wind_h = 700, 500
window = pygame.display.set_mode((wind_w , wind_h))
pygame.display.set_caption("SHOOTER")

background = pygame.image.load("bg.jfif")
background = pygame.transform.scale(background, (wind_w , wind_h))

pygame.mixer.music.load("music.mp3")
pygame.mixer.music.set_volume(0.3)
pygame.mixer.music.play(-1)

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


class Enemy(Sprite):
    def __init__(self , x , y , w , h , img1 , speed):
        super().__init__(x, y, w, h, img1)
        self.speed = speed
    
    def move(self):
        self.rect.y += self.speed
        if self.rect.y >= wind_h:
            self.rect.y = randint(-250, -50)
            self.rect.x = randint(0, wind_w-50)

font = pygame.font.SysFont("Comfortaa" , 50)
font2 = pygame.font.SysFont("Comfortaa" , 20)
font3 = pygame.font.SysFont("Comfortaa" , 35)
win = font.render("You win!", True, (0, 100, 0))
lose = font.render("You lose(", True, (100, 0, 0))
reset = font.render("Press R to reset", True, (0, 0, 0))

p_img1 = pygame.image.load("Player.png")
p_img2 = pygame.transform.flip(p_img1, True, False)
player = Player(35, 400, 50, 40, p_img1, p_img2, 5)

enemy_img = pygame.image.load("govno.png")
ENEMIES = []
for i in range(5):
    ENEMIES.append(Enemy(randint(0, wind_w-50), randint(-250, -50), 50, 40, enemy_img, 3))

game = True
finish = False
while game:
    if not finish:
        window.blit(background, (0, 0))
        
        if any(player.rect.colliderect(enemy.rect) for enemy in ENEMIES):
            window.blit(lose, (200, 200))
            window.blit(reset, (200, 250))
            finish = True
            
        player.draw()
        player.move()
        for enemy in ENEMIES:
            enemy.draw()
            enemy.move()
        
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            finish = True
            
        if event.type == pygame.KEYDOWN and event.key == pygame.K_r and finish == True:
            finish = False
            player = Player(35, 400, 50, 40, p_img1, p_img2, 5)
            for i in range(10):
                ENEMIES.append(Enemy(0, -50, 50, 40, pygame.image.load("govno.png"), 3))
    
    pygame.display.update()
    clock.tick(FPS)