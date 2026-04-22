import pygame
import random
pygame.init()
WIDTH, HEIGHT = 600, 400
CELL_SIZE = 20
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Snake Game")
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
ORANGE = (255, 165, 0)
YELLOW = (255, 255, 0)
WHITE = (255, 255, 255)
clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 30)
snake = [(100, 100), (80, 100), (60, 100)]
direction = (CELL_SIZE, 0)
def generate_food_position():
    while True:
        x = random.randint(0, (WIDTH - CELL_SIZE) // CELL_SIZE) * CELL_SIZE
        y = random.randint(0, (HEIGHT - CELL_SIZE) // CELL_SIZE) * CELL_SIZE
        if (x, y) not in snake:
            return (x, y)
class Food:
    def __init__(self):
        self.position = generate_food_position()
        self.weight = random.choice([1, 2, 3])
        self.spawn_time = pygame.time.get_ticks()
        self.lifetime = random.randint(3000, 7000)  
    def is_expired(self):
        return pygame.time.get_ticks() - self.spawn_time > self.lifetime
    def get_color(self):
        if self.weight == 1:
            return RED
        elif self.weight == 2:
            return ORANGE
        else:
            return YELLOW
food = Food()
score = 0
level = 1
speed = 7
running = True
while running:
    screen.fill(BLACK)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    keys = pygame.key.get_pressed()
    if keys[pygame.K_UP] and direction != (0, CELL_SIZE):
        direction = (0, -CELL_SIZE)
    if keys[pygame.K_DOWN] and direction != (0, -CELL_SIZE):
        direction = (0, CELL_SIZE)
    if keys[pygame.K_LEFT] and direction != (CELL_SIZE, 0):
        direction = (-CELL_SIZE, 0)
    if keys[pygame.K_RIGHT] and direction != (-CELL_SIZE, 0):
        direction = (CELL_SIZE, 0)
    head = (snake[0][0] + direction[0], snake[0][1] + direction[1])
    if (
        head[0] < 0 or head[0] >= WIDTH or
        head[1] < 0 or head[1] >= HEIGHT
    ):
        print("Game Over: Hit the wall")
        running = False
    if head in snake:
        print("Game Over: Hit yourself")
        running = False
    snake.insert(0, head)
    if food.is_expired():
        food = Food()
    if head == food.position:
        score += food.weight
        food = Food()
        if score % 4 == 0:
            level += 1
            speed += 2
    else:
        snake.pop()
    for segment in snake:
        pygame.draw.rect(screen, GREEN, (*segment, CELL_SIZE, CELL_SIZE))
    pygame.draw.rect(screen, food.get_color(), (*food.position, CELL_SIZE, CELL_SIZE))
    score_text = font.render(f"Score: {score}", True, WHITE)
    level_text = font.render(f"Level: {level}", True, WHITE)
    screen.blit(score_text, (10, 10))
    screen.blit(level_text, (10, 40))
    pygame.display.flip()
    clock.tick(speed)
pygame.quit()