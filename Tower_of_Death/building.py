import pygame
import constant
import color
import animations
import time

class Building:
    def __init__(self, x, y):
        self.shape = pygame.Rect(0, 0, constant.TOWER_WIDTH, constant.TOWER_HEIGHT)
        self.shape.midbottom = (x, y)
        self.image = animations.TOWER_IMAGE
        self.scaled_image = pygame.transform.scale(self.image, (constant.TOWER_WIDTH, constant.TOWER_HEIGHT))

        self.hitbox = pygame.Rect(0, 0, constant.TOWER_HITBOX_WIDTH, constant.TOWER_HITBOX_HEIGHT)
        self.hitbox.midbottom = (x + 64, y)

        # Outline (puede servir para feedback in-game)
        self.mask = pygame.mask.from_surface(self.scaled_image)
        self.outline = self.mask.outline()
        self.outline_timer = 0
        
    def draw(self, screen):
        screen.blit(self.scaled_image, self.shape)
        #pygame.draw.rect(screen, color.RED, self.hitbox, 1 )

        # Mostrar outline si está activo
        if time.time() < self.outline_timer:
            self.draw_outline(screen, color.RED)

    def draw_outline(self, screen, color):
        # Ajusto la posición del contorno al centro actual
        adjusted_outline = [(x + self.shape.left, y + self.shape.top) for (x, y) in self.outline]
        pygame.draw.lines(screen, color, True, adjusted_outline, 3)

    def trigger_outline(self, duration=0.5):  # default: medio segundo
        self.outline_timer = time.time() + duration