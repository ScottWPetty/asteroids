import pygame
from circleshape import CircleShape
from constants import SHOT_RADIUS

# Shot class inherits CircleShape
class Shot(CircleShape):
    def __init__(self, x, y):
        super().__init__(x, y, SHOT_RADIUS)     # uses SHOT_RADIUS constant for radius

    # method to render the shot to the screen
    def draw(self, screen):
        pygame.draw.circle(screen, "white", self.position, self.radius, 2)
    
    # method to update the position of the shot
    def update(self, dt):
        self.position += self.velocity * dt