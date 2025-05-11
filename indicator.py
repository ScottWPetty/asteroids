import pygame
import math
from constants import SCREEN_HEIGHT, SCREEN_WIDTH


class Indicator():
    def __init__(self):
        self.x = SCREEN_WIDTH // 2 - 150
        self.y = SCREEN_HEIGHT // 2
        self.radius = 20
    
    def triangle(self):
        angle_1 = math.radians(150)
        angle_2 = math.radians(210)
        a = (self.x + self.radius, self.y)
        b = (
            self.x + math.cos(angle_1) * self.radius,
            self.y + math.sin(angle_1) * self.radius
        )
        c = (
            self.x + math.cos(angle_2) * self.radius,
            self.y + math.sin(angle_2) * self.radius
        )
        return [a, b, c]
    
    def draw(self, screen):
        pygame.draw.polygon(screen, "white", self.triangle(), 2)
    
    def indicator_up(self):
        self.y -= 60
    
    def indicator_down(self):
        self.y += 60

