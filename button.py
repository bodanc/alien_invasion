import pygame.font


class Button:
    
    def __init__(self, ai_game, msg):
        """Initialize the button attributes."""
        
        self.screen = ai_game.screen
        self.screen_rect = self.screen.get_rect()
        
        # Set the dimensions and properties of the button.
        self.width, self.height = 200, 50
        self.button_color = (50, 50, 50)
        self.text_color = (255, 255, 255)
        self.font = pygame.font.SysFont(None, 48)
        
        # Build the button's rectangle object and center it.
        self.rect = pygame.Rect(0, 0, self.width, self.height)
        self.rect.center = self.screen_rect.center
        
        # Tbe button's message needs to be prepped only once.
        self._prep_msg(msg)

    def _prep_msg(self, msg):
        """Turn the 'msg' string into a rendered image and center the text on the button."""
        # The call to font.render() turns the text stored in 'msg' into an image.
        self.msg_image = self.font.render(msg, True, self.text_color, self.button_color)
        # Create a rectangle from the image.
        self.msg_image_rect = self.msg_image.get_rect()
        # Set the rectangle's center to match the center of the button
        self.msg_image_rect.center = self.rect.center

    def draw_button(self):
        """Method that can be called to display the button onscreen."""
        # Draw the rectangular portion of a blank button.
        self.screen.fill(self.button_color, self.rect)
        # To draw the text image to the screen, blit() needs an image and the rect object associated with the image.
        self.screen.blit(self.msg_image, self.msg_image_rect)
