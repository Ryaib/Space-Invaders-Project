import pygame
from pygame.sprite import Sprite


class UFO(Sprite):
    def __init__(self, ai_settings, screen):
        super(UFO, self).__init__()
        self.ai_settings = ai_settings
        self.screen = screen
        self.image = pygame.image.load('images/ufo.png')
        self.rect = self.image.get_rect()
        self.rect.x = -100
        self.rect.y = 0
        self.x = self.rect.x
        self.UFO_SPAWN = False
        self.destroyed = False

    def update(self):
        if self.destroyed:
            self.x = -100
        if not self.destroyed:
            self.x += 0.75
            self.rect.x = self.x

    def blitme(self):
        if not self.destroyed:
            self.screen.blit(self.image, self.rect)
