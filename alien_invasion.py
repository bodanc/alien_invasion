import sys
import pygame
from alien import Alien
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

        self.aliens = pygame.sprite.Group()
        self._create_fleet()

    def run_game(self):
        """Starts the main loop for the game."""
        while True:
            # The main loop checks for user input, updates the position of the ship and any bullets that were fired.
            self._check_events()
            self.ship.update()
            self._update_bullets()
            # The updated positions are then used to draw a new screen.
            self._update_screen()

    def _check_events(self):
        """Respond to keypress and mouse events."""

        # A keypress is registered in Pygame as an event and picked up by pygame.event.get()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                self._check_keydown_events(event)
            elif event.type == pygame.KEYUP:
                self._check_keyup_events(event)

    def _check_keydown_events(self, event):
        """Respond to a keypress event."""
        if event.key == pygame.K_q:
            sys.exit()
        elif event.key == pygame.K_RIGHT:
            self.ship.moving_right = True
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = True
        elif event.key == pygame.K_SPACE:
            self._fire_bullet()

    def _check_keyup_events(self, event):
        """Respond to a key release event."""
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = False
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = False

    def _fire_bullet(self):
        """Create a new bullet and add it to the 'bullets' pygame.sprite.Group()"""
        if len(self.bullets) < self.settings.bullets_allowed:
            new_bullet = Bullet(self)
            self.bullets.add(new_bullet)

    def _update_bullets(self):
        """Update the position of bullets and get rid of old bullets."""
        # Update the position of each bullet in the 'bullets' group.
        self.bullets.update()

        # Get rid of bullets that have disappeared.
        for bullet in self.bullets.copy():
            if bullet.rect.bottom <= 0:
                self.bullets.remove(bullet)

    def _create_fleet(self):
        """Create the fleet of invading aliens."""
        # Make one lousy alien.
        alien = Alien(self)
        self.aliens.add(alien)

    def _update_screen(self):
        """Code for updating images on the screen, and flip to the new screen."""
        # Draw the background.
        self.screen.fill(self.settings.bg_color)
        # Draw the ship on the screen, on top of the background.
        self.ship.blitme()
        for bullet in self.bullets.sprites():
            bullet.draw_bullet()

        # When calling draw() on a group...?
        self.aliens.draw(self.screen)

        # Make the most recently drawn screen visible.
        pygame.display.flip()


if __name__ == '__main__':
    # Initialize a game instance, and run the game.
    ai = AlienInvasion()
    ai.run_game()
