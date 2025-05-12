import pygame
from menu import Menu
from constants import SCREEN_HEIGHT, SCREEN_WIDTH

class Pause(Menu):
    def __init__(self, joystick):
        super().__init__(["Resume", "Leaderboard", "Settings", "Quit to Title"], joystick)
        self.menu_font = pygame.font.SysFont(None, 36)
    
    def draw(self, screen):
        for i in range(len(self.options)):
            text = self.menu_font.render(self.options[i], True, "white")
            text_rect = text.get_rect()
            text_rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + i * 60)
            screen.blit(text, text_rect)
        self.indicator.draw(screen)
    