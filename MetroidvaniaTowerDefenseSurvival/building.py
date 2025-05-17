import pygame
import constant
import color
import animations

class Building:
    def __init__(self, x, y):
        self.shape = pygame.Rect(0, 0, constant.TOWER_WIDTH, constant.TOWER_HEIGHT)
        self.shape.midbottom = (x, y)
        self.image = animations.TOWER_IMAGE

    def draw(self, screen):
        screen.blit(pygame.transform.scale(self.image, (constant.TOWER_WIDTH, constant.TOWER_HEIGHT)), self.shape)
