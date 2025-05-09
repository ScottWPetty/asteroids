import pygame
from circleshape import CircleShape
from shot import Shot
from life import Life
from constants import PLAYER_RADIUS, PLAYER_TURN_SPEED, PLAYER_SPEED, PLAYER_SHOOT_SPEED, PLAYER_SHOOT_COOLDOWN

class Player(CircleShape):

    # constructor
    def __init__(self, x, y): # (x, y) = center point of player triangle
        super().__init__(x, y, PLAYER_RADIUS)
        self.rotation = 0   # the direction the player is facing
        self.shot_timer = 0 # cooldown timer for shooting
        self.life = Life()
        self.i_frames = 0


    # method to calculate the player triangle
    # returns a list of points of the triangle
    def player_triangle(self):

        # forward and right used to derive the three points
        forward = pygame.Vector2(0, 1).rotate(self.rotation)
        right = pygame.Vector2(0, 1).rotate(self.rotation + 90) * self.radius / 1.5
        a = self.position + forward * self.radius
        b = self.position - forward * self.radius - right
        c = self.position - forward * self.radius + right
        return [a, b, c]

    # override the draw method of CircleShape to draw player triangle
    # pygame.draw.polygon(surface, color, points, width)
    # uses points from triangle() method
    def draw(self, screen):
        pygame.draw.polygon(screen, "white", self.player_triangle(), 2)
        self.life.draw(screen)
        

    # method to rotate the player triangle
    def rotate(self, dt):
        self.rotation += PLAYER_TURN_SPEED * dt
    
    # method to get movement key inputs and update game logic
    def update(self, dt):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_a]:
            self.rotate(dt * -1) 
        if keys[pygame.K_d]:
            self.rotate(dt)
        if keys[pygame.K_w]:
            self.move(dt)
        if keys[pygame.K_s]:
            self.move(dt * -1)

        # check if shooting is off cooldown
        if self.shot_timer <= 0:
            # check if player tried to shoot
            if keys[pygame.K_SPACE]:
                self.shoot()
                # reset shooting cooldown
                self.shot_timer = PLAYER_SHOOT_COOLDOWN
        else:   
            # decrement the cooldown timer
            self.shot_timer -= dt

    # method to get new position for movement
    def move(self, dt):
        forward = pygame.Vector2(0, 1).rotate(self.rotation)
        self.position += forward * PLAYER_SPEED * dt

    # method to create Shot objects (bullets)
    def shoot(self):
        shot = Shot(self.position.x, self.position.y)
        shot.velocity = pygame.Vector2(0, 1).rotate(self.rotation) * PLAYER_SHOOT_SPEED

    def get_lives(self):
        return self.life.get_lives()
    
    def remove_life(self):
        self.life.remove_life()
    
    def add_life(self):
        self.life.add_life()

    def has_i_frames(self):
        if self.i_frames > 0:
            return True
        else:
            return False
    
    def decrement_i_frames(self, dt):
        if self.i_frames > 0:
            self.i_frames -= dt
    
    def reset_i_frames(self):
        self.i_frames = 2