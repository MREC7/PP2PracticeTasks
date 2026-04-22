import pygame, sys
from pygame.locals import *
import random, time
pygame.init()
FPS = 60
FramePerSec = pygame.time.Clock()
BLUE  = (0, 0, 255)
RED   = (255, 0, 0)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
SCREEN_WIDTH = 400
SCREEN_HEIGHT = 600
SPEED = 5
SCORE = 0
COINS = 0
COINS_FOR_SPEED = 5
font = pygame.font.SysFont("Verdana", 60)
font_small = pygame.font.SysFont("Verdana", 20)
game_over = font.render("Game Over", True, BLACK)
background = pygame.image.load("AnimatedStreet.png")
DISPLAYSURF = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Game")
class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("Enemy.png")
        self.rect = self.image.get_rect()
        self.reset()
    def reset(self):
        self.rect.center = (random.randint(40, SCREEN_WIDTH-40), 0)
    def move(self):
        global SCORE
        self.rect.move_ip(0, SPEED)
        if self.rect.top > SCREEN_HEIGHT:
            SCORE += 1
            self.reset()
class Coin(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.base_image = pygame.image.load("Coin.png")
        self.spawn()
    def spawn(self):      
        self.value = random.choice([1, 2, 3]) 
        size = 20 + self.value * 10
        self.image = pygame.transform.scale(self.base_image, (size, size))
        self.rect = self.image.get_rect()
        self.rect.center = (random.randint(40, SCREEN_WIDTH-40), 0)
    def move(self):
        self.rect.move_ip(0, SPEED)
        if self.rect.top > SCREEN_HEIGHT:
            self.spawn()
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("Player.png")
        self.rect = self.image.get_rect()
        self.rect.center = (160, 520)
    def move(self):
        pressed_keys = pygame.key.get_pressed()
        if self.rect.left > 0 and pressed_keys[K_LEFT]:
            self.rect.move_ip(-5, 0)
        if self.rect.right < SCREEN_WIDTH and pressed_keys[K_RIGHT]:
            self.rect.move_ip(5, 0)
P1 = Player()
E1 = Enemy()
C1 = Coin()
enemies = pygame.sprite.Group(E1)
coins = pygame.sprite.Group(C1)
all_sprites = pygame.sprite.Group(P1, E1, C1)
while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
    DISPLAYSURF.blit(background, (0, 0))
    score_text = font_small.render("Score: " + str(SCORE), True, BLACK)
    DISPLAYSURF.blit(score_text, (10, 10))
    coin_text = font_small.render("Coins: " + str(COINS), True, BLACK)
    DISPLAYSURF.blit(coin_text, (SCREEN_WIDTH - 120, 10))
    for entity in all_sprites:
        DISPLAYSURF.blit(entity.image, entity.rect)
        entity.move()
    collected = pygame.sprite.spritecollideany(P1, coins)
    if collected:
        pygame.mixer.Sound('coinsound.mp3').play()
        COINS += collected.value
        collected.spawn()
        if COINS % COINS_FOR_SPEED == 0:
            SPEED += 1
            print("Speed increased! Current SPEED:", SPEED)
    if pygame.sprite.spritecollideany(P1, enemies):
        pygame.mixer.Sound('crash.wav').play()
        time.sleep(0.5)
        DISPLAYSURF.fill(RED)
        DISPLAYSURF.blit(game_over, (30, 250))
        pygame.display.update()
        for entity in all_sprites:
            entity.kill()
        time.sleep(2)
        pygame.quit()
        sys.exit()
    pygame.display.update()
    FramePerSec.tick(FPS)