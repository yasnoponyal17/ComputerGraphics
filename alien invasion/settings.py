class Settings:
    def __init__(self):
        self.screen_width = 1300
        self.screen_height = 900
        self.bg_color = (8, 12, 35)

        self.ship_speed = 6.0
        self.bullet_speed = 9.0
        self.bullet_width = 4
        self.bullet_height = 16
        self.bullet_color = (255, 230, 90)
        self.bullets_allowed = 5

        self.alien_speed = 1.5
        self.fleet_drop_speed = 35
        self.fleet_direction = 1
        self.alien_points = 67

        self.ship_limit = 3
        self.fps = 60

    def increase_speed(self):
        self.ship_speed *= 1.12
        self.bullet_speed *= 1.08
        self.alien_speed *= 1.12
        self.alien_points *= 2
