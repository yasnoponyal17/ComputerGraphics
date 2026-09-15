import pygame

class Ship:
    def __init__(self, game):
        self.screen = game.screen
        self.settings = game.settings
        self.image = pygame.image.load("images/ship.bmp").convert_alpha()
        self.image = pygame.transform.scale(self.image, (250, 200))
        self.shooting_image = pygame.image.load(
    "images/ship_shoot.bmp"
).convert_alpha()
        self.shooting_image = pygame.transform.scale(
    self.shooting_image, (250, 200)
)

        self.rect = self.image.get_rect()
        self.rect.midbottom = self.screen.get_rect().midbottom

        self.x = float(self.rect.x)
        self.shooting = False
        self.shooting_time = 0
        self.moving_right = False
        self.moving_left = False

    def update(self):
        if self.moving_right and self.rect.right < self.screen.get_width():
            self.x += self.settings.ship_speed
        if self.moving_left and self.rect.left > 0:
            self.x -= self.settings.ship_speed
        self.rect.x = int(self.x)

        if self.shooting_time > 0:
            self.shooting_time -= 1
        else:
            self.shooting = False

    def draw(self):
        if self.shooting:
            self.screen.blit(self.shooting_image, self.rect)
        else:
            self.screen.blit(self.image, self.rect)
