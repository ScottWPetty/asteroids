# pygame
import pygame

# constants
from constants import *

# game modules
from player import Player
from asteroid import Asteroid
from asteroidfield import AsteroidField
from shot import Shot
from score import Score
from title import Title
from pause import Pause
from leaderboard import Leaderboard

def main():

    #################################################################
    # Initialization Block
    #################################################################

    # initialize the pygame module
    pygame.mixer.init()
    pygame.init()
    pygame.joystick.init()
    joystick = pygame.joystick.Joystick(0)
    joystick.init()

    # State variables
    TITLE = "Title"
    PAUSE = "Pause"
    PLAYING = "Playing"
    QUIT = "Quit"
    GAME_OVER = "Game Over"
    SCORE_SCREEN = "Score Screen"

    # set initial state to TITLE
    state = TITLE

    # create a window using width and height from constants.py
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.FULLSCREEN)
    pygame.display.set_caption("Spaceballz")

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


    ########################################################################
    # Main Loop
    ########################################################################
    while True:
        if state == TITLE:

            ########################################################################
            # Title Screen Loop
            ########################################################################

            # instantiate Title object
            title = Title(joystick)

            #start music
            pygame.mixer.music.load("sounds/cinematic-halloween-synthesizer-music-248525.mp3")
            pygame.mixer.music.set_volume(0.8)
            pygame.mixer.music.play(-1)

            while state == TITLE:

                # stop the program on window close
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        state = QUIT
                
                # display the title screen
                screen.fill("black")
                title.update(dt)
                title.draw(screen)
                pygame.display.update()
                dt = clock.tick(60) / 1000
                selection = title.get_selection()

                if selection == "Play":

                    # instantiate game objects
                    player = Player(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2, joystick)
                    asteroid_field = AsteroidField()
                    score = Score()
                    state = PLAYING

                    # handle sound
                    pygame.mixer.music.fadeout(1000)
                    pygame.time.delay(1000)
                    pygame.mixer.music.stop()

                if selection == "Quit":
                    state = QUIT

                if selection == "Leaderboard":
                    input_timer = 1

                    while selection == "Leaderboard":

                        # stop the program on window close
                        for event in pygame.event.get():
                            if event.type == pygame.QUIT:
                                state == QUIT
                        
                        # create and display the leaderboard
                        leaderboard = Leaderboard()
                        screen.fill("black")
                        leaderboard.draw(screen)
                        pygame.display.update()
                        dt = clock.tick(60) / 1000

                        # check for input on leaderboard screen
                        if input_timer <= 0:
                            keys = pygame.key.get_pressed()
                            button_states = [joystick.get_button(i) for i in range(joystick.get_numbuttons())]
                            if any(keys) or any(button_states):
                                selection = None
                                title.set_selection("")

                        input_timer -= dt

                if selection == "Settings":
                    pass

        if state == PLAYING:

            ########################################################################
            # Game Loop
            ########################################################################

            # start music
            if pygame.mixer.music.get_busy():
                pygame.mixer.music.set_volume(0.7)
            
            else:
                pygame.mixer.music.load("sounds/high-energy-edm-synthesizer-259761.mp3")
                pygame.mixer.music.set_volume(0.7)
                pygame.mixer.music.play(-1)
            

            while state == PLAYING:

                # stop the program on window close
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        state = QUIT
        
                # fill screen with black color
                screen.fill("black")

                # update all objects in updatable
                updatable.update(dt)

                # check for pause
                keys = pygame.key.get_pressed()
                button_states = [joystick.get_button(i) for i in range(joystick.get_numbuttons())]
                if keys[pygame.K_ESCAPE] or button_states[7]:
                    state = PAUSE

                # loop over all drawables and draw them individually
                for object in drawable:
                    object.draw(screen)
                score.draw(screen)

                # check for collision between player and asteroids
                for asteroid in asteroids:
                    if player.collision_occured(asteroid):
                        lives = player.get_lives()

                        # check if the player is invulnerable
                        if player.has_i_frames():
                            pass

                        
                        elif lives > 1:
                            
                            # start the i_frame cooldown
                            player.reset_i_frames()

                            # take a life away
                            player.remove_life()

                            # sound
                            player_hit = pygame.mixer.Sound("sounds/player_hit/Boom1.wav")
                            player_hit.set_volume(0.8)
                            player_hit.play()

                            # split the asteroid
                            asteroid.split()

                        else:
                            state = GAME_OVER

                # check for collision between asteroids and bullets
                for asteroid in asteroids:
                    for shot in shots:
                        if asteroid.collision_occured(shot):
                            asteroid.split()
                            shot.kill()
                            score.increment_score()

                # i_frame cooldown
                player.decrement_i_frames(dt)

                # refresh the screen after all game logic for the frame is complete
                pygame.display.flip() 

                # pause the game loop at the end of each iteration to control framerate
                # .tick(x) pauses the loop for 1/x seconds
                # .tick() returns time between .tick() calls in ms 
                dt = clock.tick(FRAME_RATE) / 1000  # /1000 to convert ms to s
        
        if state == PAUSE:

            ##############################################################################
            # Pause Menu Loop
            ##############################################################################
            pause = Pause(joystick)

            # handle sound
            pygame.mixer.music.set_volume(0.3)

            while state == PAUSE:

                # stop the program on window close
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        state = QUIT

                screen.fill("black")
                pause.update(dt)
                pause.draw(screen)
                pygame.display.update()
                dt = clock.tick(60) / 1000
                selection = pause.get_selection()

                if selection == "Resume":
                    state = PLAYING

                if selection == "Quit to Title": 
                    state = SCORE_SCREEN

                    for object in updatable:
                        object.kill()

                if selection == "Settings":
                    pass

                if selection == "Leaderboard":
                    input_timer = 1

                    while selection == "Leaderboard":

                        # stop the program on window close
                        for event in pygame.event.get():
                            if event.type == pygame.QUIT:
                                state = QUIT
                    
                        leaderboard = Leaderboard()
                        screen.fill("black")
                        leaderboard.draw(screen)
                        pygame.display.update()
                        dt = clock.tick(60) / 1000
                        
                        # check for input on leaderboard screen
                        if input_timer <= 0:
                            keys = pygame.key.get_pressed()
                            button_states = [joystick.get_button(i) for i in range(joystick.get_numbuttons())]
                            if any(keys) or any(button_states):
                                selection = None
                                pause.set_selection("")
                        
                        input_timer -= dt

        if state == SCORE_SCREEN:

            # check if high score was attained
            if score.check_if_high_score():
                state = SCORE_SCREEN
                for object in updatable:
                    object.kill()

                # get player name and save the score
                active = True
                name = ""
                input_timer = 0.05  # machine too fast

            else:
                # kill all game objects and reset to title screen
                state = TITLE
                active = False

                for object in updatable:
                    object.kill()

            while active:

                # stop the program on window close
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        state == QUIT
                                    
                    if input_timer <= 0:

                        if event.type == pygame.KEYDOWN:
                            input_timer = 0.05
                            if event.key == pygame.K_RETURN:
                                active = False
                                score.save_score(name)
                            elif event.key == pygame.K_BACKSPACE:
                                name = name[:-1]
                            else:
                                if event.unicode.isalnum() or event.unicode == " ":
                                    name += event.unicode

                ### render name entry prompt to screen ###

                # build header surface
                header_font = pygame.font.SysFont(None, 50)
                header_surface = header_font.render(f"New High Score: {score.get_current_score()}", True, "white")
                header_surface_rect = header_surface.get_rect()
                header_surface_rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 3)

                # build prompt surface
                prompt_font = pygame.font.SysFont(None, 36)
                prompt_surface = prompt_font.render("Enter your name", True, "white")
                prompt_surface_rect = prompt_surface.get_rect()
                prompt_surface_rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)

                # build name surface
                name_surface = prompt_font.render(name, True, "white")
                name_surface_rect = name_surface.get_rect()
                name_surface_rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 60)

                # blit everything to the screen
                screen.fill("black")
                screen.blit(header_surface, header_surface_rect)
                screen.blit(prompt_surface, prompt_surface_rect)
                screen.blit(name_surface, name_surface_rect)

                # refresh display
                pygame.display.flip()
                dt = clock.tick(60) / 1000
                input_timer -= dt
            
            state = TITLE

        if state == GAME_OVER:
            
            # sound
            player_death = pygame.mixer.Sound("sounds/player_death/Boom1 (1).wav")
            player_death.set_volume(0.8)
            player_death.play()

            game_over_timer = 4
            player_spin_out_timer = 1.5

            while game_over_timer > 0:
                
                # player spin-out
                if player_spin_out_timer > 0:
                    player.rotate(dt * 4)
                
                else:
                    if player in drawable:
                        player.kill()

                # fill screen with black color
                screen.fill("black")

                # display "game over"
                font = pygame.font.SysFont(None, 50)
                text = font.render(f"GAME OVER", True, "white")
                text_rect = text.get_rect()
                text_rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
                screen.blit(text, text_rect)

                # update all objects in updatable
                updatable.update(dt)

                # draw objects
                for object in drawable:
                    object.draw(screen)
                score.draw(screen)

                pygame.display.flip()
                dt = clock.tick(60) / 1000
                game_over_timer -= dt
                player_spin_out_timer -= dt

            state = SCORE_SCREEN 

        if state == QUIT:
            pygame.quit()
            quit()

if __name__ == "__main__":
    main()