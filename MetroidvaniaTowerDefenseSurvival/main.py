import pygame
import animations
import constant
import color
from hero import Hero

# Inicializar Pygame
pygame.init()

# Crear Pantalla
screen = pygame.display.set_mode((constant.SCREEN_WIDTH, constant.SCREEN_HEIGHT)) 
pygame.display.set_caption("Soy una ventana!")

# Variables del personajea
hero = Hero(400, 600, animations.anim_hero_idle)

# Reloj interno
clock = pygame.time.Clock()

run = True
while run:
    # FPS
    clock.tick(constant.FPS)
    
    # Fondo
    screen.fill(color.BACKGROUNG_COLOR)
    
    # Dibujo al Heroe
    hero.draw(screen)
    
    # Movimiento y Animaciones
    if not hero.anim_locked:
        if hero.is_moving_left and not hero.is_moving_right:
            hero.move(-constant.VELOCITY, 0)
        elif hero.is_moving_right and not hero.is_moving_left:
            hero.move(constant.VELOCITY, 0)   
        else:
           hero.idle()

    if hero.is_aura_activated:
        hero.draw_outline(screen, color.GREEN)

    hero.update()

    # Eventos
    for event in pygame.event.get():
        # Cerrar el juego
        if event.type == pygame.QUIT:
            run = False

        # CONTROLES
        # Cuando pulso la tecla:
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_a:
                hero.is_moving_left = True
            if event.key == pygame.K_d:
                hero.is_moving_right = True
            if event.key == pygame.K_SPACE:
                hero.attack()
            if event.key == pygame.K_1:
                hero.is_aura_activated = True

        # Cuando suelto la tecla:
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_a:
                hero.is_moving_left = False
            if event.key == pygame.K_d:
                hero.is_moving_right = False

    pygame.display.update()

pygame.quit()