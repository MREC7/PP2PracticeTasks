import pygame
class Ball:
    def __init__(self, x, y, radius=25, step=20):
        self.x = x
        self.y = y
        self.radius = radius
        self.step = step
    def move(self, dx, dy, width, height):
        new_x = self.x + dx
        new_y = self.y + dy
        if new_x - self.radius >= 0 and new_x + self.radius <= width:
            self.x = new_x
        if new_y - self.radius >= 0 and new_y + self.radius <= height:
            self.y = new_y
    def draw(self, screen):
        pygame.draw.circle(
            screen,
            (255, 0, 0),
            (self.x, self.y),
            self.radius
        )