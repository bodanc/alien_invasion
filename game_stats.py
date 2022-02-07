class GameStats:
    """Track statistics for Alien Invasion."""

    def __init__(self, ai_game):
        """Initiate the statistics."""
        self.settings = ai_game.settings
        self.reset_stats()

    def reset_stats(self):
        """Initialize statistics that can change as the game progresses."""
        self.ships_left = self.settings.ship_limit