import pygame
import animations
import constant
from hero import Hero
from enemy import Skeleton, Ghost
from building import Building
import random
from hud import HUD
from menu import Menu
from platforms import Platform
from sound import Soundboard
from background import Background

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

# Background
background = Background()

# HUD
hud = HUD()

# Consola de sonido
soundboard = Soundboard()

# Menu
menu = Menu(constant.SCREEN_WIDTH, constant.SCREEN_HEIGHT)

# Creo al personaje
hero = Hero(400, constant.GROUND_HEIGHT, animations.ANIM_HERO_IDLE)

# Lista de enemigos
enemies = []
skeletons = []
ghosts = []
souls = []
enemy_spawn_timer = 0

# Tower of Death
tower = Building(constant.SCREEN_WIDTH / 2 - 64, constant.SCREEN_HEIGHT)

PLATFORM_HEIGHT_CONSTANT = 180
PLATFORM_HEIGHT_1 = constant.SCREEN_HEIGHT - PLATFORM_HEIGHT_CONSTANT
PLATFORM_HEIGHT_2 = constant.SCREEN_HEIGHT - PLATFORM_HEIGHT_CONSTANT * 2
PLATFORM_HEIGHT_3 = constant.SCREEN_HEIGHT - PLATFORM_HEIGHT_CONSTANT * 3

PLATFORM_WIDTH_CONSTANT = 240

PLATFORM_CENTER = constant.SCREEN_WIDTH / 2
PLATFORM_LEFT_WIDTH_1 = PLATFORM_CENTER - PLATFORM_WIDTH_CONSTANT
PLATFORM_RIGHT_WIDTH_1 = PLATFORM_CENTER + PLATFORM_WIDTH_CONSTANT

platforms = [
    #Platform(PLATFORM_CENTER, PLATFORM_HEIGHT_1, 100, 20),
    Platform(PLATFORM_CENTER, PLATFORM_HEIGHT_2, 100, 20),
    #Platform(PLATFORM_CENTER, PLATFORM_HEIGHT_3, 100, 20),
    Platform(PLATFORM_LEFT_WIDTH_1, PLATFORM_HEIGHT_1, 100, 20),
    #Platform(PLATFORM_WIDTH_1, PLATFORM_HEIGHT_2, 100, 20),
    Platform(PLATFORM_LEFT_WIDTH_1, PLATFORM_HEIGHT_3, 100, 20),

    Platform(PLATFORM_RIGHT_WIDTH_1, PLATFORM_HEIGHT_1, 100, 20),
    Platform(PLATFORM_RIGHT_WIDTH_1, PLATFORM_HEIGHT_3, 100, 20),
]

# Funcion para spawnear enemigos
def spawn_enemy():
    if len(skeletons) < constant.MAX_SKELETONS:

        # Elijo entre la primer (0) o cuarta seccion (3) de la pantalla para asignar a la zona de spawn
        spawn_zone = random.choice([0, 3])
        spawn_zone_width = constant.SCREEN_WIDTH // 4
        
        # Calcular los límites del tercio elegido
        x_min = spawn_zone * spawn_zone_width
        x_max = x_min + spawn_zone_width

        # Genero una posicion random dentro de la zona de spawn
        x_pos = random.randint(x_min, x_max)

        # Genero un enemigo con una coordenada random en el eje X
        enemy = Skeleton(x_pos, constant.GROUND_HEIGHT, souls)
        # Lo agrego a la lista de enemigos
        enemies.append(enemy)
    
    if len(ghosts) < constant.MAX_GHOSTS:
        spawn_point = random.choice([1,2,3,4,5,6])
        if spawn_point == 1:
            x_pos = -50
            y_pos = constant.GHOST_SPAWN_HEIGHT_1
        elif spawn_point == 2:
            x_pos = -50
            y_pos = constant.GHOST_SPAWN_HEIGHT_2
        elif spawn_point == 3:
            x_pos = constant.SCREEN_WIDTH + 50
            y_pos = constant.GHOST_SPAWN_HEIGHT_1 
        elif spawn_point == 4:
            x_pos = -constant.SCREEN_WIDTH + 50
            y_pos = constant.GHOST_SPAWN_HEIGHT_2
        elif spawn_point == 5:
            x_pos = -constant.SCREEN_WIDTH - 50
            y_pos = constant.GHOST_SPAWN_HEIGHT_3
        elif spawn_point == 6:
            x_pos = -constant.SCREEN_WIDTH + 50
            y_pos = constant.GHOST_SPAWN_HEIGHT_3
        enemy = Ghost(x_pos, y_pos, souls, (constant.SCREEN_WIDTH/2))
        enemies.append(enemy)
        



def update_and_draw(delta_time):
    # Dibujo el menu
    if not ingame:
        menu.draw_menu(screen)
    
    if ingame:
        # Fondo
        background.draw_background(screen)

        # Torre
        tower.draw(screen)

        # Plataformas
        for platform in platforms:
            platform.draw(screen)

        # Tierra
        ground_image = animations.GROUND_IMAGE
        screen.blit(ground_image, (0, constant.SCREEN_HEIGHT - 96))     # <-------- Numerito magico

        # Heroe
        hero.update(delta_time, platforms)
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
    delta_time = clock.tick(constant.FPS) / 1000
    
    update_and_draw(delta_time)

    if ingame:
        enemy_spawn_timer += delta_time
        if enemy_spawn_timer >= 3:
            spawn_enemy()
            enemy_spawn_timer = 0

    events = pygame.event.get()

    for event in events:
        if event.type == pygame.QUIT:
            run = False

        if ingame:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_w:
                    hero.jump()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    hero.attack()

            if event.type == constant.LEVEL_UP_EVENT:
                hud.level_alert(hero.level)

            if event.type == constant.GAME_OVER_EVENT:
                hud.game_over_alert()
            if event.type == constant.ATTACK_EVENT:
                soundboard.play_sound("attack")
            if event.type == constant.JUMP_EVENT:
                soundboard.play_sound("jump")
            if event.type == constant.SKELETON_DEATH_EVENT:
                sound = random.choice([1,2,3,4])
                soundboard.play_sound(f"hit_1")
                soundboard.play_sound(f"zombie_death_{sound}")

        # Controles del Menu
        else:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT or event.key == pygame.K_a:
                    menu.selected = (menu.selected - 1) % len(menu.menu_items)
                elif event.key == pygame.K_RIGHT or event.key == pygame.K_d:
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
        hero.pressing_down = keys[pygame.K_s] or keys[pygame.K_DOWN]
        if keys[pygame.K_a] or keys[pygame.K_LEFT]:
            hero.move(-1, 0)
        elif keys[pygame.K_d] or keys[pygame.K_RIGHT]:
            hero.move(1, 0)
        else:
            if hero.on_ground:
                hero.change_animation(animations.ANIM_HERO_IDLE)

    pygame.display.update()

pygame.quit()
print("Fin!")