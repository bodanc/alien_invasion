import pygame
from pygame.sprite import Sprite


class Bullet(Sprite):
    """A class to manage the bullets fired from the ship."""

    def __init__(self, ai_game):
        """Create a bullet object at the ship's current position."""
        super().__init__()
        self.screen = ai_game.screen
        self.settings = ai_game.settings
        self.color = self.settings.bullet_color

        # Create a bullet rect. at coordinates (0, 0) and then set the correct position (top middle of the ship rect).
        self.rect = pygame.Rect(0, 0, self.settings.bullet_width, self.settings.bullet_height)
        self.rect.midtop = ai_game.ship.rect.midtop

        # Store the bullet's position as a decimal value to allow for more precision when changing the bullet speed.
        self.y = float(self.rect.y)

    def update(self):
        """Move the bullet up, along the y-axis."""

        # Update the decimal value representing the position of the bullet.
        # When a bullet is fired, it moves up the screen, which corresponds to a *decrease* in the y-coord. value!
        self.y -= self.settings.bullet_speed
        # Update the rectangle's position.
        self.rect.y = self.y

    def draw_bullet(self):
        """Draw the bullet to the screen."""
        pygame.draw.rect(self.screen, self.color, self.rect)
