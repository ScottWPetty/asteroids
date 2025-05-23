import pygame
import os
import random
from circleshape import CircleShape
from shot import Shot
from life import Life
from constants import PLAYER_RADIUS, PLAYER_TURN_SPEED, PLAYER_SPEED, PLAYER_SHOOT_SPEED, PLAYER_SHOOT_COOLDOWN

class Player(CircleShape):

    # constructor
    def __init__(self, x, y, joystick): # (x, y) = center point of player triangle
        super().__init__(x, y, PLAYER_RADIUS)
        self.rotation = 0   # the direction the player is facing
        self.shot_timer = 0 # cooldown timer for shooting
        self.life = Life()
        self.i_frames = 0
        self.player_color = "white"
        self.i_frame_color = [255, 0, 0]
        self.i_frame_color_dimming = True # controls oscillating character brightness when using i-frames
        
        # controller input
        self.joystick = joystick

        # movement
        self.current_player_turn_speed = 0
        self.current_player_speed = 0

        # sounds
        self.shoot_sounds = []
        for file_name in os.listdir("sounds/weapon_1"):
            file_path = os.path.join("sounds/weapon_1", file_name)
            self.shoot_sounds.append(pygame.mixer.Sound(file_path))
        

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
        if self.has_i_frames():
            pygame.draw.polygon(screen, self.i_frame_color, self.player_triangle(), 2)
            self.life.draw(screen)
        else:
            pygame.draw.polygon(screen, self.player_color, self.player_triangle(), 2)
            self.life.draw(screen)
        

    # method to rotate the player triangle
    def rotate(self, dt):
        self.rotation += PLAYER_TURN_SPEED * dt
    
    # method to get movement key inputs and update game logic
    def update(self, dt):
        keys = pygame.key.get_pressed()
        button_states = [self.joystick.get_button(i) for i in range(self.joystick.get_numbuttons())]
        hat = self.joystick.get_hat(0)
        if keys[pygame.K_a] or hat == (-1, 0) or hat == (-1, 1) or hat == (-1, -1):
            self.rotate(dt * -1) 
        if keys[pygame.K_d] or hat == (1, 0) or hat == (1, 1) or hat == (1, -1):
            self.rotate(dt)
        if keys[pygame.K_w] or hat == (0, 1) or hat == (1, 1) or hat == (-1 , 1):
            self.move(dt)
        if keys[pygame.K_s] or hat == (0, -1) or hat == (1, -1) or hat == (-1, -1):
            self.move(dt * -1)

        # check if shooting is off cooldown
        if self.shot_timer <= 0:
            # check if player tried to shoot
            if keys[pygame.K_SPACE] or button_states[0]:
                self.shoot()
                sound = random.choice(self.shoot_sounds)
                sound.play()

                # reset shooting cooldown
                self.shot_timer = PLAYER_SHOOT_COOLDOWN
        else:   
            # decrement the cooldown timer
            self.shot_timer -= dt

    # method to get new position for movement
    def move(self, dt):
        forward = pygame.Vector2(0, 1).rotate(self.rotation)

        # to add acceleration replace PLAYER_SPEED with an increasing value that caps a PLAYER_SPEED
        # i.e. member variables: current speed, acceleration.
        # use current speed and increment by acceleration until current speed == PLAYER_SPEED
        # need to constantly travel at current speed. start at 0 at beginning of game
        # also need to constantly travel in the same direction and just offset it by the current speed while facing another direction
        # this is tricky because current speed is different for different directions at any given time
        # idk how to implement this might need to look it up.
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
            if self.i_frame_color_dimming == True:
                self.i_frame_color[0] -= 4
                if self.i_frame_color[0] <= 50:
                    self.i_frame_color_dimming = False
            if self.i_frame_color_dimming == False:
                self.i_frame_color[0] += 4
                if self.i_frame_color[0] >= 250:
                    self.i_frame_color_dimming = True

    def reset_i_frames(self):
        self.i_frames = 2