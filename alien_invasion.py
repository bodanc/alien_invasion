import sys
from time import sleep
import pygame

from alien import Alien
from bullet import Bullet
from settings import Settings
from game_stats import GameStats
from ship import Ship


class AlienInvasion:
    """Overall class to manage game assets and behavior."""

    def __init__(self):
        """Initialize the game, and create game resources."""
        # The pygame.init() function initializes the background settings that Pygame needs to work correctly.
        pygame.init()
        # Create an instance of the Settings class and assign it to self.settings
        self.settings = Settings()

        # Create a display window (a 'surface') on which all the game's graphical elements (rects) will be drawn.
        self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        self.settings.screen_width = self.screen.get_rect().width
        self.settings.screen_height = self.screen.get_rect().height
        pygame.display.set_caption('Alien Invasion')

        # Create an instance of GameStats to store game statistics.
        self.stats = GameStats(self)

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
            # The main loop checks for user input, updates the position of the ship, any bullets that were fired, as
            # well as that of the alien fleet.
            self._check_events()

            self.ship.update()

            self._update_bullets()

            self._update_aliens()

            # All updated positions are then used to draw a new screen.
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
        """Helper method to update the position of all bullets and to remove old bullets."""
        # Update the position of each bullet in the 'bullets' group.
        self.bullets.update()

        # Get rid of bullets that have disappeared from the game surface.
        for bullet in self.bullets.copy():
            if bullet.rect.bottom <= 0:
                self.bullets.remove(bullet)

        self._check_bullet_alien_collisions()

    def _check_bullet_alien_collisions(self):
        """Respond to bullet-alien collisions."""
        # Check if any of the bullet and alien rects have collided and, if so, remove the bullet and the alien.
        collisions = pygame.sprite.groupcollide(self.bullets, self.aliens, True, True)

        # If the 'aliens' pygame.sprite.Group() is empty, the if statement evaluates to False.
        if not self.aliens:
            # Destroy existing bullets and create a new fleet.
            self.bullets.empty()
            self._create_fleet()

    def _update_aliens(self):
        """Check if the fleet is at an edge,
            then update the positions of all the aliens in the fleet."""
        self._check_fleet_edges()
        self.aliens.update()

        # Look for collisions between aliens and the player's ship.
        if pygame.sprite.spritecollideany(self.ship, self.aliens):
            self._ship_hit()

        # Check for aliens hitting the bottom of the screen after updating the positions of all the aliens and after
        # looking for collisions between the aliens and the player's ship.
        self._check_aliens_bottom()

    def _check_aliens_bottom(self):
        """Check if any of the aliens have reached the bottom of the screen."""
        screen_rect = self.screen.get_rect()
        for alien in self.aliens.sprites():
            if alien.rect.bottom >= screen_rect.bottom:
                # Treat this event the same way as if the ship were hit.
                self._ship_hit()
                break

    def _ship_hit(self):
        """Helper method to handle a ship hit event: update GameStats (ships_left - 1), reinitialize the player's ship,
        the alien fleet and all the bullets, pause the game for a moment, etc."""

        # Decrement ships_left.
        self.stats.ships_left -= 1

        # Remove all remaining aliens and bullets from their respective pygame.sprite.Group().
        self.aliens.empty()
        self.bullets.empty()

        # Create a new fleet and center the ship.
        self._create_fleet()
        self.ship.center_ship()

        sleep(0.5)

    def _create_fleet(self):
        """Helper method to create the fleet of invading aliens."""
        # Create an alien and find the number of aliens that can fit in a row.
        alien = Alien(self)
        alien_width, alien_height = alien.rect.size
        available_space_x = self.settings.screen_width - (2 * alien_width)
        number_aliens_x = available_space_x // (2 * alien_width)

        # Determine the number of rows of aliens that fit on the screen.
        ship_height = self.ship.rect.height
        available_space_y = (self.settings.screen_height - ship_height - (5 * alien_height))
        number_rows = available_space_y // (2 * alien_height)

        # Create the full fleet of aliens
        for row_number in range(number_rows):
            for alien_number in range(number_aliens_x):
                self._create_alien(alien_number, row_number)

    def _create_alien(self, alien_number, row_number):
        """Helper method to create an alien and place it in the Sprite group."""
        alien = Alien(self)
        alien_width, alien_height = alien.rect.size
        alien.x = alien_width + 2 * alien_width * alien_number
        alien.rect.x = alien.x
        alien.rect.y = alien.rect.height + 2 * alien.rect.height * row_number
        self.aliens.add(alien)

    def _check_fleet_edges(self):
        """Respond appropriately if any aliens have reached the edges of the screen."""
        for alien in self.aliens.sprites():
            if alien.check_edges():
                # If any of the sprites in the group are at either edge of the screen, call _change_fleet_direction()
                self._change_fleet_direction()
                break

    def _change_fleet_direction(self):
        """Drop the entire fleet and change the fleet's direction."""
        for alien in self.aliens.sprites():
            alien.rect.y += self.settings.fleet_drop_speed
        self.settings.fleet_direction *= -1

    def _update_screen(self):
        """Helper method for updating images on the screen, and flipping to the new screen."""
        # Draw the background.
        self.screen.fill(self.settings.bg_color)
        # Draw the ship on the screen, on top of the background.
        self.ship.blitme()
        for bullet in self.bullets.sprites():
            bullet.draw_bullet()

        # Pygame draws each element in the group at the position defined by its 'rect' attribute.
        self.aliens.draw(self.screen)

        # Make the most recently drawn screen visible.
        pygame.display.flip()


if __name__ == '__main__':
    # Initialize a game instance, and run the game.
    ai = AlienInvasion()
    ai.run_game()
