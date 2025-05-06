import pygame
from constants import *
from player import Player
from asteroid import Asteroid
from asteroidfield import AsteroidField
from shot import Shot

def main():

    print(f"Starting Asteroids!")
    print(f"Screen width: {SCREEN_WIDTH}")
    print(f"Screen height: {SCREEN_HEIGHT}")

    #################################################################
    # Initialization Block
    #################################################################
    # initialize the pygame module
    pygame.init()

    # create a window using width and height from constants.py
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

    # clock object to keep track of time
    clock = pygame.time.Clock()

    # delta time variable
    dt = 0

    # create object groups
    updatable = pygame.sprite.Group()   # holds objects that are updatable
    drawable = pygame.sprite.Group()    # holds objects that are drawable
    asteroids = pygame.sprite.Group()   # holds all asteroid objects
    shots = pygame.sprite.Group()       # holds all shot objects

    # set static containers field for classes to the appropriate groups
    Player.containers = (updatable, drawable)
    Asteroid.containers = (asteroids, updatable, drawable)
    AsteroidField.containers = (updatable)
    Shot.containers = (shots, updatable, drawable)

    # instantiate game objects
    # x and y coordinates == center of screen
    player = Player(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)
    asteroid_field = AsteroidField()

    ########################################################################
    # Game Loop
    ########################################################################
    while True:

        # check if user closed the window.
        # if they do, exit the game loop
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
        
        # fill screen with black color
        screen.fill("black")

        # update all objects in updatable
        updatable.update(dt)

        # loop over all drawables and draw them individually
        for object in drawable:
            object.draw(screen)

        # check for collision between player and asteroids
        for asteroid in asteroids:
            if player.collision_occured(asteroid):
                print("Game over!")
                return

        # check for collision between asteroids and bullets
        for asteroid in asteroids:
            for shot in shots:
                if asteroid.collision_occured(shot):
                    asteroid.split()
                    shot.kill()

        # refresh the screen after all game logic for the frame is complete
        pygame.display.flip() 

        # pause the game loop at the end of each iteration to control framerate
        # .tick(x) pauses the loop for 1/x seconds
        # .tick() returns time between .tick() calls in ms 
        dt = clock.tick(60) / 1000  # /1000 to convert ms to s

if __name__ == "__main__":
    main()