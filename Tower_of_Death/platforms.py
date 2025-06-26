import pygame
import color
import constant

PLATFORM_HEIGHT_CONSTANT = 180
PLATFORM_HEIGHT_1 = constant.SCREEN_HEIGHT - PLATFORM_HEIGHT_CONSTANT
PLATFORM_HEIGHT_2 = constant.SCREEN_HEIGHT - PLATFORM_HEIGHT_CONSTANT * 2
PLATFORM_HEIGHT_3 = constant.SCREEN_HEIGHT - PLATFORM_HEIGHT_CONSTANT * 3

PLATFORM_WIDTH_CONSTANT = 240
PLATFORM_CENTER = constant.SCREEN_WIDTH / 2
PLATFORM_LEFT_WIDTH_1 = PLATFORM_CENTER - PLATFORM_WIDTH_CONSTANT
PLATFORM_RIGHT_WIDTH_1 = PLATFORM_CENTER + PLATFORM_WIDTH_CONSTANT

class Platform:
    def __init__(self, x, y, width, height):
        self.image = pygame.Surface((width, height))
        self.image.fill((110, 110, 110))

        self.rect = self.image.get_rect()
        self.rect.center = (int(x), int(y))  

    def draw(self, screen):
        screen.blit(self.image, self.rect)

platforms_1 = [
    #Platform(PLATFORM_CENTER, PLATFORM_HEIGHT_1, 100, 20),
    Platform(PLATFORM_CENTER, PLATFORM_HEIGHT_2, 100, 20),
    #Platform(PLATFORM_CENTER, PLATFORM_HEIGHT_3, 100, 20),
    Platform(PLATFORM_LEFT_WIDTH_1, PLATFORM_HEIGHT_1, 100, 20),
    #Platform(PLATFORM_WIDTH_1, PLATFORM_HEIGHT_2, 100, 20),
    Platform(PLATFORM_LEFT_WIDTH_1, PLATFORM_HEIGHT_3, 100, 20),
    Platform(PLATFORM_RIGHT_WIDTH_1, PLATFORM_HEIGHT_1, 100, 20),
    Platform(PLATFORM_RIGHT_WIDTH_1, PLATFORM_HEIGHT_3, 100, 20),
]

platforms_2 = []