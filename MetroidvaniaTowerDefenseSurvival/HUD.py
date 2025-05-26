import pygame as p
import fonts as f
import color
import constant

ALERT_X = constant.SCREEN_WIDTH / 2
ALERT_Y = constant.SCREEN_HEIGHT / 2 - constant.SCREEN_HEIGHT / 4

STATS_X = constant.SCREEN_WIDTH / 2
STATS_Y = constant.SCREEN_HEIGHT / 18

class HUD:
    def __init__(self):
        self.font_small = p.font.Font(f.PATH_CAUDEX_REGULAR, 24)
        self.font_large = p.font.Font(f.PATH_CAUDEX_REGULAR, 96)
        self.alert_timer = 0
        self.alert_text = ""
        self.experience = 0
        self.color = color.WHITE

    def level_alert(self, level):
        self.alert_text = f"Level {level}"
        self.alert_timer = 120
        self.color = color.WHITE
        
    def game_over_alert(self):
        self.alert_text = "Game Over"
        self.alert_timer = 120
        self.color = color.RED

    def update_stats(self, experience, max_experience):
        self.experience = f"{experience} / {max_experience}"

    def update(self, duration):
        if self.alert_timer > 0:
            self.alert_timer -= duration

    def draw(self, screen):
        # Alertas (LEVEL UP / GAME OVER)
        if self.alert_timer > 0:
            message = self.font_large.render(self.alert_text, True, self.color)
            rect = message.get_rect(center=(ALERT_X, ALERT_Y))
            screen.blit(message, rect)

        # Stats
        self.font = p.font.Font(f.PATH_CAUDEX_REGULAR, 24)
        stats = self.font_small.render(f"{self.experience}", True, color.WHITE)
        rect = stats.get_rect(center=(STATS_X, STATS_Y))
        screen.blit(stats, rect)
