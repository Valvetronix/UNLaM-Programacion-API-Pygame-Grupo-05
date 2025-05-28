import pygame as p
import fonts as f
import color
import constant

class HUD:
    def __init__(self):
        self.font_small = p.font.Font(f.PATH_CAUDEX_REGULAR, 24)
        self.font_large = p.font.Font(f.PATH_CAUDEX_REGULAR, 96)
        self.alert_pos = (constant.SCREEN_WIDTH / 2, constant.SCREEN_HEIGHT / 2 - constant.SCREEN_HEIGHT / 4)
        self.stats_pos = (constant.SCREEN_WIDTH / 2, constant.SCREEN_HEIGHT / 18)
        self.alert_timer = 0
        self.alert_text = ""
        self.experience = 0
        self.max_experience = 1
        self.experience_bar = p.Rect(10, 10, constant.SCREEN_WIDTH - 20, 20)
        self.color = color.WHITE
        self.duration = 1


    def level_alert(self, level):
        self.alert_text = f"Level {level}"
        self.alert_timer = 120
        self.color = color.WHITE
        
    def game_over_alert(self):
        self.alert_text = "Game Over"
        self.alert_timer = 120
        self.color = color.RED

    def update_stats(self, experience, max_experience):
        self.experience = experience
        self.max_experience = max_experience

    def update(self):
        if self.alert_timer > 0:
            self.alert_timer -= self.duration

    def draw(self, screen):
        # Alertas (LEVEL UP / GAME OVER)
        if self.alert_timer > 0:
            alert = self.font_large.render(self.alert_text, True, self.color)
            rect = alert.get_rect(center=(self.alert_pos))
            screen.blit(alert, rect)

        # Stats

        # Barra de Experiencia:
        p.draw.rect(screen, color.GRAY, self.experience_bar)
        fill_width = (self.experience / self.max_experience) * self.experience_bar.width
        self.experience_bar_fill = p.Rect(self.experience_bar.left, self.experience_bar.top, fill_width, self.experience_bar.height)
        p.draw.rect(screen, color.GREEN, self.experience_bar_fill)

        experience_text = f"{self.experience} / {self.max_experience}"
        text_surface = self.font_small.render(experience_text, True, color.WHITE)
        text_rect = text_surface.get_rect(center=self.experience_bar.center)
        screen.blit(text_surface, text_rect)
