import pygame
from indicator import Indicator
from constants import SCREEN_HEIGHT, SCREEN_WIDTH

class Menu():
    def __init__(self, options, joystick):
        self.indicator = Indicator()
        self.selection_index = 0
        self.selection_timer = 0.5
        self.selection = ""
        self.options = []
        for option in options:
            self.options.append(option)
        
        # controller support
        self.joystick = joystick
        
        # sounds
        self.indicator_sound = pygame.mixer.Sound("sounds/indicator_sound/Blip5.wav")
        self.indicator_sound.set_volume(.5)
        self.select_sound = pygame.mixer.Sound("sounds/indicator_sound/Blip7.wav")
        self.select_sound.set_volume(.5)
    
    def draw(self, screen):
        # sub-classes override
        pass
    
    def update(self, dt):
        keys = pygame.key.get_pressed()
        button_states = [self.joystick.get_button(i) for i in range(self.joystick.get_numbuttons())]
        hat = self.joystick.get_hat(0)
        # check if selection timer is finished
        if self.selection_timer <= 0:
            if keys[pygame.K_w] or hat == (0, 1):
                if self.selection_index > 0:
                    self.selection_index -= 1
                    self.indicator.indicator_up()
                    self.indicator_sound.play()
                    self.selection_timer = 0.1
            if keys[pygame.K_s] or hat == (0, -1):
                if self.selection_index < len(self.options) - 1:
                    self.selection_index += 1
                    self.indicator.indicator_down()
                    self.indicator_sound.play()
                    self.selection_timer = 0.1
            if keys[pygame.K_RETURN] or button_states[0]:
                self.selection_timer = 0.1
                self.selection = self.options[self.selection_index]
                self.select_sound.play()

        else:   
            # decrement the selection timer
            self.selection_timer -= dt
    
    def get_selection(self):
        return self.selection
    
    def set_selection(self, selection):
        self.selection = selection