import pygame
import animations
import constant
import color
from hero import Hero
from enemy import Skeleton
from building import Building
import random

# Inicializar Pygame
pygame.init()

# Crear Pantalla
screen = pygame.display.set_mode((constant.SCREEN_WIDTH, constant.SCREEN_HEIGHT)) 
pygame.display.set_caption("Soy una ventana!")

# Reloj interno
clock = pygame.time.Clock()

# Variables del personaje
hero = Hero(400, constant.SCREEN_HEIGHT, animations.anim_hero_idle)

# Lista de enemigos
enemies = []
souls = []

# Tower of Death
tower = Building(constant.SCREEN_WIDTH / 2, constant.SCREEN_HEIGHT)

# Funcion para spawnear enemigos
def spawn_enemy():
    if len(enemies) < constant.MAX_ENEMIES:
        # Genero un enemigo con una coordenada random en el eje X
        enemy = Skeleton(random.randint(0, constant.SCREEN_WIDTH), constant.SCREEN_HEIGHT, souls)
        # Lo agrego a la lista de enemigos
        enemies.append(enemy)

# Ejecuto el juego
run = True
while run:
    # FPS
    clock.tick(constant.FPS)

    # Actualizo al Heroe
    hero.update()

    # Llamo a la funcion para spawnear enemigos
    spawn_enemy()

    # Fondo
    screen.fill(color.BACKGROUNG_COLOR)

    # Torre
    tower.draw(screen)

    # Heroe
    hero.draw(screen)

    # Recorro la lista de enemigos
    for enemy in enemies:
        # Detecto la colision del ataque del Heroe con el Enemigo
        if hero.attack_hitbox.colliderect(enemy.hitbox):
            enemy.destroy()

        # Una vez muerto lo remuevo de la lista de enemigos
        if not enemy.alive:
            enemies.remove(enemy)

        # Si esta vivo sigue actualizandose y dibujandose
        else:
            enemy.update()
            enemy.draw(screen)

    # Recorro la lista de Almas
    for soul in souls[:]:
        soul.update()
        soul.draw(screen)
        if soul.arrived:
            souls.remove(soul)
    
    # Eventos
    for event in pygame.event.get():
        # Boton de ataque
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                hero.attack()
        # Cerrar el juego
        if event.type == pygame.QUIT:
            run = False

    # Controles de movimiento
    keys = pygame.key.get_pressed()
    if keys[pygame.K_a] or keys[pygame.K_LEFT]:
        hero.move(-1, 0)
    elif keys[pygame.K_d] or keys[pygame.K_RIGHT]:
        hero.move(1, 0)
    else:
        hero.idle()

    pygame.display.update()

pygame.quit()