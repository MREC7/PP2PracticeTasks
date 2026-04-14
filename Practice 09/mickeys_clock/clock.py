import pygame
import datetime
class MickeyClock:
    def __init__(self, screen):
        self.screen = screen
        self.clock_img = pygame.image.load("images/mickeyclock.png").convert_alpha()
        self.minute_hand = pygame.image.load("images/minute_hand.png").convert_alpha()
        self.second_hand = pygame.image.load("images/second_hand.png").convert_alpha()
        self.center = self.clock_img.get_rect(center=screen.get_rect().center).center
    def get_time_angles(self):
        now = datetime.datetime.now()
        seconds = now.second
        minutes = now.minute
        sec_angle = -6 * seconds
        min_angle = -6 * minutes
        return sec_angle, min_angle
    def rotate_hand(self, image, angle):
        rotated = pygame.transform.rotate(image, angle)
        rect = rotated.get_rect(center=self.center)
        return rotated, rect
    def draw(self):
        clock_rect = self.clock_img.get_rect(center=self.center)
        self.screen.blit(self.clock_img, clock_rect)
        sec_angle, min_angle = self.get_time_angles()
        sec_img, sec_rect = self.rotate_hand(self.second_hand, sec_angle)
        min_img, min_rect = self.rotate_hand(self.minute_hand, min_angle)
        self.screen.blit(sec_img, sec_rect)
        self.screen.blit(min_img, min_rect)