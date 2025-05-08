import pygame
from score import Score
from constants import SCREEN_HEIGHT, SCREEN_WIDTH

class Leaderboard():
    def __init__(self):
        self.title_font = pygame.font.SysFont(None, 50)
        self.score_font = pygame.font.SysFont(None, 36)
        self.title = "LEADERBOARD"
        self.score = Score()
        self.scores = self.score.get_scores()
    
    def draw(self, screen):
        text = self.title_font.render(self.title, True, "white")
        text_rect = text.get_rect()
        text_rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 4)
        screen.blit(text, text_rect)
        for i in range(len(self.scores)):
            text = self.score_font.render(f"{i + 1}. {self.scores[i][0]:<12} {self.scores[i][1]:>6}", True, "white")
            text_rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 3 + i * 50)
            screen.blit(text, text_rect)
        text = self.score_font.render(f"PRESS ANY KEY TO RETURN", True, "white")
        text_rect = text.get_rect()
        text_rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT - 40)
        screen.blit(text, text_rect)