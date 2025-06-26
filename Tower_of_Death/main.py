import pygame
import animations
import constant
from game import Game

# Inicializar Pygame
pygame.init()
screen = pygame.display.set_mode((constant.SCREEN_WIDTH, constant.SCREEN_HEIGHT))
pygame.display.set_caption("Tower of Death")

# Cargar assets
tile_set = animations.load_assets()
pygame.display.set_icon(animations.WINDOW_ICON)

# Ejecutar el juego
game = Game(screen)
game.start()
