import pygame
import random
from circleshape import CircleShape
from constants import ASTEROID_MIN_RADIUS

# Asteroid inherets from CircleShape
class Asteroid(CircleShape):
    def __init__(self, x, y, radius):
        super().__init__(x, y, radius)

    # draw/render the Asteroid object to the screen
    def draw(self, screen):
        pygame.draw.circle(screen, "white", self.position, self.radius, 2)

    def update(self, dt):
        self.position += self.velocity * dt

    # method for splitting the asteroids when shot
    def split(self):
        
        # check if the asteroid is not the smallest kind
        if self.radius > ASTEROID_MIN_RADIUS:

            # get a random angle from 20 to 50
            angle = random.uniform(20, 50)

            # create two vectors by rotating the asteroids velocity by the angle and its opposite
            vector_1 = self.velocity.rotate(angle)
            vector_2 = self.velocity.rotate(-angle)

            # calculate a smaller radius
            radius = self.radius - ASTEROID_MIN_RADIUS

            # create two new asteroid objects at the position of the original with the smaller radius
            asteroid_1 = Asteroid(self.position.x, self.position.y, radius)
            asteroid_2 = Asteroid(self.position.x, self.position.y, radius)

            # set the velocity of the new asteroids using the two vectors
            # increase the speed by scaling the vectors up a little
            asteroid_1.velocity = vector_1 * 1.5
            asteroid_2.velocity = vector_2 * 1.5
        
        # kill the original asteroid
        self.kill()
        