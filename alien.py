import pygame
from pygame.sprite import Sprite


class Alien(Sprite):
    # A class to represent a single alien in the fleet.

    def __init__(self, ai_settings, screen):
        super(Alien, self).__init__()
        self.screen = screen
        self.ai_settings = ai_settings
        self.image = pygame.image.load('images/alien1.png')

        # Load the alien image and set its rect attribute.

        self.rect = self.image.get_rect()

        # Start each new alien near the toop left of the screen.
        self.alien_number = ai_settings.alien_number
        self.rect.x = self.rect.width
        self.rect.y = self.rect.height

        # Store the alien's exact positon.
        self.x = float(self.rect.x)

    def check_edges(self):
        # Return True if alien is at edge of screen.
        screen_rect = self.screen.get_rect()
        if self.rect.right >= screen_rect.right:
            return True
        elif self.rect.left <= 0:
            return True



    def update(self):
        # Move the alien right
        self.x += (self.ai_settings.alien_speed_factor *
               self.ai_settings.fleet_direction)
        self.rect.x = self.x


    def blitme(self):
        # Draw the alien at its current location
        self.screen.blit(self.image, self.rect)


class Alien2(Sprite):
    # A class to represent a single alien in the fleet.

    def __init__(self, ai_settings, screen):
        super(Alien2, self).__init__()
        self.screen = screen
        self.ai_settings = ai_settings
        self.image = pygame.image.load('images/alien2.png')

        # Load the alien image and set its rect attribute.

        self.rect = self.image.get_rect()

        # Start each new alien near the toop left of the screen.
        self.rect.x = self.rect.width
        self.rect.y = self.rect.height

        # Store the alien's exact positon.
        self.x = float(self.rect.x)

    def check_edges(self):
        # Return True if alien is at edge of screen.
        screen_rect = self.screen.get_rect()
        if self.rect.right >= screen_rect.right:
            return True
        elif self.rect.left <= 0:
            return True



    def update(self):
        # Move the alien right
        self.x += (self.ai_settings.alien_speed_factor *
               self.ai_settings.fleet_direction)
        self.rect.x = self.x


    def blitme(self):
        # Draw the alien at its current location
        self.screen.blit(self.image, self.rect)


class Alien3(Sprite):
    # A class to represent a single alien in the fleet.

    def __init__(self, ai_settings, screen):
        super(Alien3, self).__init__()
        self.screen = screen
        self.ai_settings = ai_settings
        self.image = pygame.image.load('images/alien3.png')

        # Load the alien image and set its rect attribute.

        self.rect = self.image.get_rect()

        # Start each new alien near the toop left of the screen.
        self.rect.x = self.rect.width
        self.rect.y = self.rect.height

        # Store the alien's exact positon.
        self.x = float(self.rect.x)

    def check_edges(self):
        # Return True if alien is at edge of screen.
        screen_rect = self.screen.get_rect()
        if self.rect.right >= screen_rect.right:
            return True
        elif self.rect.left <= 0:
            return True



    def update(self):
        # Move the alien right
        self.x += (self.ai_settings.alien_speed_factor *
               self.ai_settings.fleet_direction)
        self.rect.x = self.x


    def blitme(self):
        # Draw the alien at its current location
        self.screen.blit(self.image, self.rect)


class UFO(Sprite):
    # A class to represent a single alien in the fleet.

    def __init__(self, ai_settings, screen):
        super(UFO, self).__init__()
        self.screen = screen
        self.ai_settings = ai_settings
        self.image = pygame.image.load('images/ufo.png')
        self.alien_number = 0

        # Load the alien image and set its rect attribute.

        self.rect = self.image.get_rect()

        # Start each new alien near the toop left of the screen.
        self.rect.x = self.rect.width
        self.rect.y = self.rect.height

        # Store the alien's exact positon.
        self.x = float(self.rect.x)

    def check_edges(self):
        # Return True if alien is at edge of screen.
        screen_rect = self.screen.get_rect()
        if self.rect.right >= screen_rect.right:
            return True
        elif self.rect.left <= 0:
            return True



    def update(self):
        # Move the alien right
        self.x += self.ai_settings.alien_speed_factor
        self.rect.x = self.x


    def blitme(self):
        # Draw the alien at its current location
        self.screen.blit(self.image, self.rect)

