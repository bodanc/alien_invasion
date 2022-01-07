import sys
import pygame
from settings import Settings
from ship import Ship


class AlienInvasion:
    """Overall class to manage game assets and behavior."""

    def __init__(self):
        """Initialize the game, and create game resources."""
        # The pygame.init() function initializes the background settings that Pygame needs to work correctly.
        pygame.init()
        # Create an instance of the Settings class and assign it to self.settings
        self.settings = Settings()

        # Create a display window (a 'surface') on which all the game's graphical elements will be drawn.
        self.screen = pygame.display.set_mode((self.settings.screen_width, self.settings.screen_height))
        pygame.display.set_caption('Alien Invasion')

        # Initialize an instance of Ship after the screen has been created.
        # The 'self' argument passed to Ship() refers to the current instance of AlienInvasion.
        self.ship = Ship(self)

    def run_game(self):
        """Starts the main loop for the game."""
        while True:
            # We are looking for new events and updating the screen on each pass through the loop.
            self._check_events()
            # The ship's position will be updated and then used when drawing the ship to the screen by _update_screen()
            self.ship.update()
            self._update_screen()

    def _check_events(self):
        """Respond to keypress and mouse events."""

        # A keypress is registered in Pygame as an event and picked up by the pygame.event.get() method.
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RIGHT:
                    self.ship.moving_right = True
                elif event.key == pygame.K_LEFT:
                    self.ship.moving_left = True
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_RIGHT:
                    self.ship.moving_right = False
                elif event.key == pygame.K_LEFT:
                    self.ship.moving_left = False

    def _update_screen(self):
        """Code for updating images on the screen, and flip to the new screen."""
        # Draw the background.
        self.screen.fill(self.settings.bg_color)
        # Draw the ship on the screen, on top of the background.
        self.ship.blitme()
        # Make the most recently drawn screen visible.
        pygame.display.flip()


if __name__ == '__main__':
    # Initialize a game instance, and run the game.
    ai = AlienInvasion()
    ai.run_game()
