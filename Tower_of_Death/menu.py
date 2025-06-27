import pygame
import sys
from fonts import PATH_CAUDEX_REGULAR, PATH_CAUDEX_BOLD
from color import WHITE, GRAY, BLACK
# abajo pondriamos la foto linkdeada
# title_image = pygame.image.load("ruta/a/tu/imagen.png").convert_alpha()
# title_image = pygame.transform.scale(title_image, (ancho_deseado, alto_deseado))

class Menu():
    def __init__(self, screen_width, screen_height, background):
        # Opciones del menú
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.background = background

        self.regular_font = pygame.font.Font(PATH_CAUDEX_REGULAR, 24)
        self.bold_font = pygame.font.Font(PATH_CAUDEX_BOLD, 24)

        self.menu_items = ["Start", "Credits", "Quit"]
        self.selected = 0
        pass

    def draw_menu(self, screen):
        # en las siguientes 2 lineas de codigo se quitaria el asterisco una vz tengamos la foto deel titulo del juego y se modificaria eso
        # img_x = SCREEN_WIDTH
        screen.blit(self.background, (0, 0))

        # nos da la seleccion de las 3 opciones que esten en el centro de la pantalla
        total_width = 0
        texts = []

        #screen.fill(BLACK)

        for item in self.menu_items:
            text = self.regular_font.render(item, True, GRAY)
            texts.append(text)
            total_width += text.get_width()

        spacing = 60  # espacio entre opciones
        total_width += spacing * (len(self.menu_items) - 1)

        start_x = (self.screen_width - total_width) // 2
        y = self.screen_height // 2

        for i, text in enumerate(texts):
            x = start_x + sum(t.get_width() + spacing for t in texts[:i])
            color = WHITE if i == self.selected else GRAY
            text = self.bold_font.render(self.menu_items[i], True, color)
            screen.blit(text, (x, y))

            
            if i == self.selected:
                underline_rect = pygame.Rect(x, y + text.get_height() + 5, text.get_width(), 5)
                pygame.draw.rect(screen, WHITE, underline_rect)

        pygame.display.flip()