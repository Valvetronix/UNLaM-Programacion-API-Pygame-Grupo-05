import pygame
import color
import constant

class Enemy():
    def __init__(self, x, y):
        self.shape = pygame.Rect(0, 0, constant.ENEMY_HITBOX_WIDTH, constant.ENEMY_HITBOX_HEIGHT)
        self.shape.midbottom = (x, y)
        self.color = color.GREEN

        # Hitbox
        self.hitbox = pygame.Rect(0, 0, constant.ENEMY_HITBOX_WIDTH, constant.ENEMY_HITBOX_HEIGHT)
        self.hitbox.midbottom = self.shape.midbottom

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.shape)
        pygame.draw.rect(screen, color.RED, self.hitbox, 1)