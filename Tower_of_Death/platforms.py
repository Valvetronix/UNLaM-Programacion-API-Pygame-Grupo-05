import pygame
import color

class Platform:
    def __init__(self, x, y, width, height):
        self.image = pygame.Surface((width, height))
        self.image.fill((110, 110, 110))

        self.rect = self.image.get_rect()
        self.rect.center = (x, y)

    def draw(self, screen):
        screen.blit(self.image, self.rect)
        pygame.draw.rect(screen, (255, 0, 0), self.rect, 2)