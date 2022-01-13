import sys
import pygame
from bullet import Bullet
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
        self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        self.settings.screen_width = self.screen.get_rect().width
        self.settings.screen_height = self.screen.get_rect().height
        pygame.display.set_caption('Alien Invasion')

        # Initialize an instance of Ship after the screen has been created.
        # The 'self' argument passed to Ship() refers to the current instance of AlienInvasion.
        self.ship = Ship(self)
        # On each pass through the main loop, draw bullets to the screen and update their position.
        self.bullets = pygame.sprite.Group()

    def run_game(self):
        """Starts the main loop for the game."""
        while True:
            # We are looking for new events and updating the screen on each pass through the loop.
            self._check_events()
            # The ship's position will be updated and then used by _update_screen() to draw the ship on the screen.
            self.ship.update()
            # Update the position of all the bullets on each pass through the loop.
            self.bullets.update()

            self._update_screen()

    def _check_events(self):
        """Respond to keypress and mouse events."""

        # A keypress is registered in Pygame as an event and picked up by the pygame.event.get() method.
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                self._check_keydown_events(event)
            elif event.type == pygame.KEYUP:
                self._check_keyup_events(event)

    def _check_keydown_events(self, event):
        """Respond to a keypress event."""
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = True
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = True
        elif event.key == pygame.K_q:
            sys.exit()
        elif event.key == pygame.K_SPACE:
            self._fire_bullet()

    def _check_keyup_events(self, event):
        """Respond to a key release event."""
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = False
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = False

    def _fire_bullet(self):
        """Create a new bullet and add it to the bullets group."""
        new_bullet = Bullet(self)
        self.bullets.add(new_bullet)

    def _update_screen(self):
        """Code for updating images on the screen, and flip to the new screen."""
        # Draw the background.
        self.screen.fill(self.settings.bg_color)
        # Draw the ship on the screen, on top of the background.
        self.ship.blitme()
        for bullet in self.bullets.sprites():
            bullet.draw_bullet()
        # Make the most recently drawn screen visible.
        pygame.display.flip()


if __name__ == '__main__':
    # Initialize a game instance, and run the game.
    ai = AlienInvasion()
    ai.run_game()
