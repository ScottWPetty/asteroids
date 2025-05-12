import pygame
import os
import random
from circleshape import CircleShape
from constants import ASTEROID_MIN_RADIUS

# Asteroid inherets from CircleShape
class Asteroid(CircleShape):
    def __init__(self, x, y, radius, color):
        super().__init__(x, y, radius)
        self.color = color

        # sounds
        self.hit_sounds = []
        for file_name in os.listdir("sounds/enemy_hit"):
            file_path = os.path.join("sounds/enemy_hit", file_name)
            self.hit_sounds.append(pygame.mixer.Sound(file_path))

    # draw/render the Asteroid object to the screen
    def draw(self, screen):
        pygame.draw.circle(screen, self.color, self.position, self.radius, 2)

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
            asteroid_1 = Asteroid(self.position.x, self.position.y, radius, self.color)
            asteroid_2 = Asteroid(self.position.x, self.position.y, radius, self.color)

            # set the velocity of the new asteroids using the two vectors
            # increase the speed by scaling the vectors up a little
            asteroid_1.velocity = vector_1 * 1.5
            asteroid_2.velocity = vector_2 * 1.5
        
        # kill the original asteroid
        sound = random.choice(self.hit_sounds)
        self.kill()
        sound.set_volume(0.6)
        sound.play()
        