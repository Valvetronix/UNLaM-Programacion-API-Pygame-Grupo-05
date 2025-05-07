import pygame
import animations
import constant
import color
from hero import Hero
from enemy import Enemy

# Inicializar Pygame
pygame.init()

# Crear Pantalla
screen = pygame.display.set_mode((constant.SCREEN_WIDTH, constant.SCREEN_HEIGHT)) 
pygame.display.set_caption("Soy una ventana!")

# Variables del personajea
hero = Hero(400, 600, animations.anim_hero_idle)

# Enemigo
enemy = Enemy(700, 600)

# Reloj interno
clock = pygame.time.Clock()

run = True
while run:
    # FPS
    clock.tick(constant.FPS)

    # Actualizo las animaciones
    hero.update()

    # DIBUJO
    # Fondo
    screen.fill(color.BACKGROUNG_COLOR)   
    # Heroe
    hero.draw(screen)
    # Enemigo
    enemy.draw(screen)
    
    # Movimiento y Animaciones

    # Colisiones
    if hero.attack_hitbox.colliderect(enemy.hitbox):
        enemy.color = color.RED
    else:
        enemy.color = color.GREEN



    # Eventos
    for event in pygame.event.get():
        # Control ataque
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                hero.attack()
        # Cerrar el juego
        if event.type == pygame.QUIT:
            run = False

    # Controles
    keys = pygame.key.get_pressed()
    if keys[pygame.K_a] or keys[pygame.K_LEFT]:
        hero.move(-1, 0)
    elif keys[pygame.K_d] or keys[pygame.K_RIGHT]:
        hero.move(1, 0)
    else:
        hero.idle()

    pygame.display.update()

pygame.quit()