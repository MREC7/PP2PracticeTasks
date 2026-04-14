import pygame
from clock import MickeyClock
pygame.init()
WIDTH, HEIGHT = 1280, 720
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Mickey Clock")
clock = pygame.time.Clock()
mickey_clock = MickeyClock(screen)
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    screen.fill((255, 255, 255))
    mickey_clock.draw()
    pygame.display.flip()
    clock.tick(60)
pygame.quit()