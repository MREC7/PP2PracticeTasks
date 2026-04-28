import pygame
import random

WIDTH, HEIGHT = 400, 600

class Player(pygame.sprite.Sprite):
    def __init__(self, skin="default"):
        super().__init__()
        self.skin = skin
        self.load_image()
        self.rect = self.image.get_rect(center=(200, 500))

    def load_image(self):
        if self.skin == "alt":
            self.image = pygame.image.load("Player1.png").convert_alpha()
        else:
            self.image = pygame.image.load("Player.png").convert_alpha()

    def set_skin(self, skin):
        self.skin = skin
        self.load_image()

    def move(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and self.rect.left > 0:
            self.rect.x -= 5
        if keys[pygame.K_RIGHT] and self.rect.right < WIDTH:
            self.rect.x += 5

class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("Enemy.png").convert_alpha()
        self.rect = self.image.get_rect()
        self.reset()

    def reset(self, player_x=None):
        while True:
            x = random.randint(40, WIDTH - 40)
            if player_x is None or abs(x - player_x) > 60:
                self.rect.center = (x, 0)
                break

    def move(self, speed):
        self.rect.y += speed
        if self.rect.top > HEIGHT:
            self.reset()

class Coin(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("Coin.png").convert_alpha()
        self.rect = self.image.get_rect()
        self.spawn()

    def spawn(self):
        self.rect.center = (random.randint(40, WIDTH - 40), 0)

    def move(self, speed):
        self.rect.y += speed
        if self.rect.top > HEIGHT:
            self.spawn()


class PowerUp(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.type = random.choice(["nitro", "shield", "repair"])

        self.image = pygame.Surface((20, 20))
        if self.type == "nitro":
            self.image.fill((0, 255, 255))
        elif self.type == "shield":
            self.image.fill((255, 255, 0))
        else:
            self.image.fill((255, 0, 255))

        self.rect = self.image.get_rect()
        self.spawn()
        self.spawn_time = pygame.time.get_ticks()

    def spawn(self):
        self.rect.center = (random.randint(40, WIDTH - 40), 0)
        self.spawn_time = pygame.time.get_ticks()

    def move(self, speed):
        self.rect.y += speed
        if self.rect.top > HEIGHT:
            self.spawn()

    def is_expired(self):
        return pygame.time.get_ticks() - self.spawn_time > 5000


class Obstacle(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.type = random.choice(["oil", "barrier"])

        self.image = pygame.Surface((40, 40))
        if self.type == "oil":
            self.image.fill((50, 50, 50))
        else:
            self.image.fill((200, 0, 0))

        self.rect = self.image.get_rect()
        self.spawn()

    def spawn(self):
        self.rect.center = (random.randint(40, WIDTH - 40), 0)

    def move(self, speed):
        self.rect.y += speed
        if self.rect.top > HEIGHT:
            self.spawn()