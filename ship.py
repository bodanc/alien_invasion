# The 'ship' module contains the Ship class, which manages most of the behavior of the player's ship.

import pygame


class Ship:
    """A class to manage the player's ship."""

    # 2 parameters: the 'self' reference and a ref. to the current instance of the AlienInvasion class.
    def __init__(self, ai_game):
        """Initialize the ship, and set its starting position."""
        # Assign the game screen to an attribute of Ship so it can be easily accessed by the Ship methods.
        self.screen = ai_game.screen
        self.settings = ai_game.settings

        # Access the screen's rectangle attribute with the get_rect() method to correctly place the Ship on the screen.
        self.screen_rect = ai_game.screen.get_rect()

        # Load the ship image and get its rectangle.
        # pygame.image.load() returns a surface representing the ship, which is assigned to the self.image attribute.
        self.image = pygame.image.load('images/ship.bmp')
        self.rect = self.image.get_rect()

        # Start each new ship at the bottom center of the screen.
        self.rect.midbottom = self.screen_rect.midbottom

        # Store a decimal value for the ship's horizontal position.
        self.x = float(self.rect.x)

        # Movement flags
        self.moving_right = False
        self.moving_left = False

    # A method to draw the image of the ship at the position specified by self.rect
    def blitme(self):
        """Draw the ship at its current location."""
        self.screen.blit(self.image, self.rect)

    def update(self):
        """Update the ship's position based on the movement flags."""

        # Update the ship's x-coord. value, not the rect.
        if self.moving_right and self.rect.right < self.screen_rect.right:
            self.x += self.settings.ship_speed
        if self.moving_left and self.rect.left > 0:
            self.x -= self.settings.ship_speed

        # Update the rect. object from self.x
        self.rect.x = self.x

    def center_ship(self):
        """Center the ship on the screen."""
        self.rect.midbottom = self.screen_rect.midbottom
        self.x = float(self.rect.x)
