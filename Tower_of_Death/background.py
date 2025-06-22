import pygame
import animations
import constant

class Background:
    def __init__(self):
        self.level = 0

    def draw_background(self, screen, level = 0):
        self.level = level

        if self.level == 0:
            background_image = animations.BACKGROUND_IMAGE
            screen.blit(pygame.transform.scale(background_image, (constant.SCREEN_WIDTH, constant.SCREEN_HEIGHT)), (0, 0))

            mountain_width = constant.SCREEN_WIDTH / 2
            mountain_height = constant.SCREEN_HEIGHT / 2
            mountain_image = pygame.transform.scale(animations.MOUNTAINS_IMAGE, (mountain_width, mountain_height))

            for i in range(4):
                x = i * mountain_image.get_width()
                y = constant.SCREEN_HEIGHT - mountain_height
                screen.blit(mountain_image, (x, y))

            graveyard_width = constant.SCREEN_WIDTH
            graveyard_height = constant.SCREEN_HEIGHT/3
            graveyard_image = pygame.transform.scale(animations.GRAVEYARD_IMAGE, (graveyard_width, graveyard_height))
            screen.blit(graveyard_image, (0, constant.SCREEN_HEIGHT - graveyard_height))
