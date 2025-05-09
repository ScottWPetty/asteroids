import pygame
import math
from constants import SCREEN_WIDTH

class Life():
    def __init__(self):
        self.lives = 3
        self.last_position = (SCREEN_WIDTH - 30, 30)
        self.radius = 20
        
    def get_triangles(self):
        triangles = []
        for i in range(self.lives):
            x = self.last_position[0] - i * 40
            y = self.last_position[1]
            angle_1 = math.radians(60)
            angle_2 = math.radians(120)
            a = (x, y - self.radius)
            b = (
                x + math.cos(angle_1) * self.radius,
                y + math.sin(angle_1) * self.radius
            )
            c = (
                x + math.cos(angle_2) * self.radius,
                y + math.sin(angle_2) * self.radius
            )
            triangles.append([a, b, c])
        return triangles
    
    def draw(self, screen):
        font = pygame.font.SysFont(None, 36)
        text = font.render("Lives: ", True, "white")
        text_rect = text.get_rect()
        text_rect.center = (SCREEN_WIDTH - 170, 30)
        screen.blit(text, text_rect)
        triangles = self.get_triangles()
        for i in range(len(triangles)):
            pygame.draw.polygon(screen, "white", triangles[i], 2)
    
    def remove_life(self):
        self.lives -= 1

    def add_life(self):
        if self.lives < 3:
            self.lives += 1

    def get_lives(self):
        return self.lives