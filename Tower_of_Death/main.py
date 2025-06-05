import pygame
import animations
import constant
from hero import Hero
from enemy import Skeleton
from building import Building
import random
from hud import HUD
from menu import Menu

# Inicializar Pygame
pygame.init()

# Crear Pantalla
screen = pygame.display.set_mode((constant.SCREEN_WIDTH, constant.SCREEN_HEIGHT)) 
pygame.display.set_caption("Tower of Death")

# Cargo los assets
animations.load_assets()

# Icono de la ventana
pygame.display.set_icon(animations.WINDOW_ICON)

# Reloj interno
clock = pygame.time.Clock()

# booleans
ingame = False

# HUD
hud = HUD()

# Creo el menú
menu = Menu(constant.SCREEN_WIDTH, constant.SCREEN_HEIGHT)

# Creo al personaje
hero = Hero(400, constant.SCREEN_HEIGHT - constant.GROUND_HEIGHT, animations.ANIM_HERO_IDLE)

# Lista de enemigos
enemies = []
souls = []

# Tower of Death
tower = Building(constant.SCREEN_WIDTH / 2 - 64, constant.SCREEN_HEIGHT)

# Funcion para spawnear enemigos
def spawn_enemy():
    if len(enemies) < constant.MAX_ENEMIES:

        # Elijio entre la primer (0) o cuarta seccion (3) de la pantalla para asignar a la zona de spawn
        spawn_zone = random.choice([0, 3])
        spawn_zone_width = constant.SCREEN_WIDTH // 4
        
        # Calcular los límites del tercio elegido
        x_min = spawn_zone * spawn_zone_width
        x_max = x_min + spawn_zone_width

        # Genero una posicion random dentro de la zona de spawn
        x_pos = random.randint(x_min, x_max)

        # Genero un enemigo con una coordenada random en el eje X
        enemy = Skeleton(x_pos, constant.SCREEN_HEIGHT - constant.GROUND_HEIGHT, souls)
        # Lo agrego a la lista de enemigos
        enemies.append(enemy)

def draw_background():
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



def update_and_draw():
    # Dibujo el menuuu
    if not ingame:
        menu.draw_menu(screen)
    
    if ingame:
        # Fondo
        draw_background()

        # Torre
        tower.draw(screen)

        # Tierra
        ground_image = animations.GROUND_IMAGE
        screen.blit(ground_image, (0, constant.SCREEN_HEIGHT - 96))

        # Heroe
        hero.update()
        hero.draw(screen)

        # HUD
        hud.update()
        hud.update_stats(hero.experience, hero.max_experience)
        hud.draw(screen)

        # Recorro la lista de enemigos
        for enemy in enemies:
            # Detecto la colision del ataque del Heroe con el Enemigo
            if hero.attack_hitbox.colliderect(enemy.hitbox):
                enemy.destroy()

            # Detecto si impacta la torre
            if tower.hitbox.colliderect(enemy.hitbox):
                tower.trigger_outline()
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
                hero.experience += soul.value
                souls.remove(soul)


# Ejecuto el juego
run = True
while run:
    clock.tick(constant.FPS)

    update_and_draw()

    if ingame:
        spawn_enemy()

    # Obtenemos los eventos UNA sola vez por frame
    events = pygame.event.get()

    for event in events:
        if event.type == pygame.QUIT:
            run = False

        if ingame:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    hero.attack()

            if event.type == constant.LEVEL_UP_EVENT:
                hud.level_alert(hero.level)

            if event.type == constant.GAME_OVER_EVENT:
                hud.game_over_alert()

        else:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    menu.selected = (menu.selected - 1) % len(menu.menu_items)
                elif event.key == pygame.K_RIGHT:
                    menu.selected = (menu.selected + 1) % len(menu.menu_items)
                elif event.key == pygame.K_SPACE or event.key == pygame.K_RETURN:
                    choice = menu.menu_items[menu.selected]
                    if choice == "Start":
                        ingame = True
                    elif choice == "Credits":
                        print("Mostrar créditos...")
                    elif choice == "Quit":
                        run = False

    if ingame:
        keys = pygame.key.get_pressed()
        if keys[pygame.K_a] or keys[pygame.K_LEFT]:
            hero.move(-1, 0)
        elif keys[pygame.K_d] or keys[pygame.K_RIGHT]:
            hero.move(1, 0)
        else:
            hero.idle()

    pygame.display.update()

pygame.quit()
print("Fin!")