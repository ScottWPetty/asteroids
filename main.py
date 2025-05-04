import pygame
from constants import *

def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

    # game loop
    while True:

        # check if user closed the window.
        # if they do, exit the game loop
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
        
        # fill screen with black color
        screen.fill("black")

        # refresh the screen; (always do this last)
        pygame.display.flip() 

    print(f"Starting Asteroids!")
    print(f"Screen width: {SCREEN_WIDTH}")
    print(f"Screen height: {SCREEN_HEIGHT}")

if __name__ == "__main__":
    main()