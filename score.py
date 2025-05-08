import pygame

class Score():
    def __init__(self):
        self.current_score = 0
        self.scores = []
        self.score_font = pygame.font.SysFont(None, 36)
        try:
            with open("scores.txt", "r") as file:
                for line in file:
                    try:
                        name, score = line.split(",")
                        self.scores.append((name, int(score)))
                    except ValueError:
                        print(f"Skipping bad line: {line.strip()}")
        except FileNotFoundError:
            pass

    def increment_score(self):
        self.current_score += 10
    
    def draw(self, screen):
        text_surface = self.score_font.render(f"{self.current_score}", True, "white")
        screen.blit(text_surface, (20, 20))
    
    def save_score(self, player_name):
        self.scores.append((player_name, self.current_score))
        self.scores.sort(key=lambda x: x[1], reverse=True)
        while len(self.scores) > 10:
            del self.scores[-1]
        
        with open("scores.txt", "w") as file:
            for name, score in self.scores:
                file.write(f"{name},{score}\n")
                
    def get_scores(self):
        return self.scores
    
    def get_current_score(self):
        return self.current_score
    
    def check_if_high_score(self):
        if len(self.scores) < 10:
            return True
        elif self.current_score > self.scores[-1][-1]:
            return True
        else:
            return False
        
