import sys
import pygame
from pygame.sprite import Group
from settings import Settings
from ship import Ship
from bullet import Bullet
from alien import Alien

class AlienInvasion:
    def __init__(self):
        pygame.init()
        self.settings = Settings()
        self.screen = pygame.display.set_mode(
            (self.settings.screen_width, self.settings.screen_height))
        pygame.display.set_caption("Инопланетное вторжение")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont("arial", 24)
        self.big_font = pygame.font.SysFont("arial", 52)

        self.ship = Ship(self)
        self.bullets = Group()
        self.aliens = Group()
        self.score = 0
        self.level = 1
        self.ships_left = self.settings.ship_limit
        self.game_active = True
        self.create_fleet()

    def create_fleet(self):
        alien = Alien(self, 0, 0)
        available_width = self.settings.screen_width - 2 * alien.rect.width
        columns = available_width // (2 * alien.rect.width)
        rows = max(2, (self.settings.screen_height - 420) //
                   (2 * alien.rect.height))
        for row in range(rows):
            for col in range(columns):
                x = alien.rect.width + 2 * alien.rect.width * col
                y = alien.rect.height + 2 * alien.rect.height * row
                self.aliens.add(Alien(self, x, y))

    def run(self):
        while True:
            self.clock.tick(self.settings.fps)
            self.check_events()
            if self.game_active:
                self.ship.update()
                self.update_bullets()
                self.update_aliens()
            self.update_screen()

    def check_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key in (pygame.K_RIGHT, pygame.K_d):
                    self.ship.moving_right = True
                elif event.key in (pygame.K_LEFT, pygame.K_a):
                    self.ship.moving_left = True
                elif event.key == pygame.K_SPACE:
                    self.fire_bullet()
                elif event.key == pygame.K_r and not self.game_active:
                    self.restart()
            elif event.type == pygame.KEYUP:
                if event.key in (pygame.K_RIGHT, pygame.K_d):
                    self.ship.moving_right = False
                elif event.key in (pygame.K_LEFT, pygame.K_a):
                    self.ship.moving_left = False

    def fire_bullet(self):
        if len(self.bullets) < self.settings.bullets_allowed and self.game_active:
            self.bullets.add(Bullet(self))
            self.ship.shooting = True
            self.ship.shooting_time = 8

    def update_bullets(self):
        self.bullets.update()
        for bullet in list(self.bullets):
            if bullet.rect.bottom <= 0:
                self.bullets.remove(bullet)
        collisions = pygame.sprite.groupcollide(
            self.bullets, self.aliens, True, True)
        for aliens in collisions.values():
            self.score += self.settings.alien_points * len(aliens)
        if not self.aliens:
            self.level += 1
            self.settings.increase_speed()
            self.bullets.empty()
            self.create_fleet()

    def update_aliens(self):
        if any(alien.check_edges() for alien in self.aliens):
            self.settings.fleet_direction *= -1
            for alien in self.aliens:
                alien.rect.y += self.settings.fleet_drop_speed
        self.aliens.update()
        if pygame.sprite.spritecollideany(self.ship, self.aliens):
            self.lose_ship()
        if any(alien.rect.bottom >= self.screen.get_height() for alien in self.aliens):
            self.lose_ship()

    def lose_ship(self):
        if self.ships_left > 0:
            self.ships_left -= 1
            self.aliens.empty()
            self.bullets.empty()
            self.ship = Ship(self)
            self.create_fleet()
            pygame.time.delay(500)
        else:
            self.game_active = False

    def restart(self):
        self.settings = Settings()
        self.score = 0
        self.level = 1
        self.ships_left = self.settings.ship_limit
        self.ship = Ship(self)
        self.bullets.empty()
        self.aliens.empty()
        self.game_active = True
        self.create_fleet()

    def update_screen(self):
        self.screen.fill(self.settings.bg_color)
        for bullet in self.bullets:
            bullet.draw()
        for alien in self.aliens:
            alien.draw()
        self.ship.draw()
        info = self.font.render(
            f"Счёт: {self.score}   Уровень: {self.level}   "
            f"Корабли: {self.ships_left}", True, (240, 240, 255))
        self.screen.blit(info, (20, 15))
        if not self.game_active:
            title = self.big_font.render("ИГРА ОКОНЧЕНА", True, (255, 100, 100))
            hint = self.font.render("Нажмите R, чтобы начать заново", True,
                                    (240, 240, 255))
            self.screen.blit(title, title.get_rect(center=self.screen.get_rect().center))
            self.screen.blit(hint, hint.get_rect(
                center=(self.screen.get_rect().centerx,
                        self.screen.get_rect().centery + 65)))
        pygame.display.flip()

if __name__ == "__main__":
    AlienInvasion().run()
