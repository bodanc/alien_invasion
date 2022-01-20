class Settings:
    """A class to store all the settings for Alien Invasion."""

    def __init__(self):
        """Initialize all the game settings."""

        # Screen settings
        self.screen_width = 1200
        self.screen_height = 800
        self.bg_color = (230, 230, 230)

        # Ship settings
        self.ship_speed = 0.5

        # Bullet settings
        self.bullet_speed = 1.5
        self.bullet_width = 2
        self.bullet_height = 15
        self.bullet_color = (60, 60, 60)
        self.bullets_allowed = 4

        # Alien settings
        self.alien_speed = 0.3
        self.fleet_drop_speed = 10
        # A fleet direction of 1 represents movement to the right and -1 to the left.
        self.fleet_direction = 1
