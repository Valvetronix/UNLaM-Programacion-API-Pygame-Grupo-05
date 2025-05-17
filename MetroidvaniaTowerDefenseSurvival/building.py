import pygame
import constant
import color

class Building:
    def __init__(self, x, y):
        self.shape = pygame.Rect(0, 0, constant.TOWER_WIDTH, constant.SCREEN_HEIGHT)
        self.shape.midbottom = (x, y)

    def draw(self, screen):
        pygame.draw.rect(screen, color.BLUE, self.shape)