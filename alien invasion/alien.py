import pygame
from pygame.sprite import Sprite

class Alien(Sprite):
    def __init__(self, game, x, y):
        super().__init__()
        self.settings = game.settings
        self.screen = game.screen
        self.image = pygame.image.load("images/alien.bmp").convert_alpha()
        self.image = pygame.transform.scale(self.image, (78, 54))

        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

        self.x = float(self.rect.x)

    def check_edges(self):
        screen_rect = self.screen.get_rect()
        return self.rect.right >= screen_rect.right or self.rect.left <= 0

    def update(self):
        self.x += self.settings.alien_speed * self.settings.fleet_direction
        self.rect.x = int(self.x)

    def draw(self):
        self.screen.blit(self.image, self.rect)
