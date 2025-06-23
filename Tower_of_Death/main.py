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
import fonts

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
game_started = False
menu_active = True
game_over = False

# Background
background = Background()

# HUD
hud = HUD()

# Consola de sonido
soundboard = Soundboard()
soundboard.play_next_track()

# Menu
menu = Menu(constant.SCREEN_WIDTH, constant.SCREEN_HEIGHT)

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

# Creo al personaje
hero = Hero(constant.HERO_SPAWN_X, constant.HERO_SPAWN_Y, animations.ANIM_HERO_IDLE)

# Lista de enemigos
enemies = []
skeletons = []
ghosts = []
souls = []
enemy_spawn_timer = 0

# Contadores de Score
ghosts_killed = 0
skeletons_killed = 0

# Funcion para spawnear enemigos
def spawn_enemy(level = 1):
    level = level
    if len(skeletons) < level * 2:

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
    
    if level == 1 and len(ghosts) < constant.MAX_GHOSTS:
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
        
def fade_in(screen, speed=2):
    fade_surface = pygame.Surface((constant.SCREEN_WIDTH, constant.SCREEN_HEIGHT))
    fade_surface.fill((0, 0, 0))
    for alpha in range(255, -1, -speed):
        fade_surface.set_alpha(alpha)
        update_and_draw(delta_time)  # Dibuja la escena actual
        screen.blit(fade_surface, (0, 0))
        pygame.display.update()
        pygame.time.delay(10)

def fade_out(screen, speed=1):
    fade_surface = pygame.Surface((constant.SCREEN_WIDTH, constant.SCREEN_HEIGHT))
    fade_surface.fill((0, 0, 0))
    for alpha in range(0, 256, speed):
        fade_surface.set_alpha(alpha)
        update_and_draw(delta_time)  # Dibuja la escena actual
        screen.blit(fade_surface, (0, 0))
        pygame.display.update()
        pygame.time.delay(10)

def show_game_over_screen(screen, score):
    font_big = pygame.font.SysFont(fonts.PATH_CAUDEX_BOLD, 64)
    font_small = pygame.font.SysFont(fonts.PATH_CAUDEX_REGULAR, 32)

    game_over_text = font_big.render("Game Over", True, (255, 255, 255))
    skeletons_killed_text = font_small.render(f"Esqueletos destruidos: {skeletons_killed}", True, (255, 255, 255))
    ghosts_killed_text = font_small.render(f"Fantasmas destruidos: {ghosts_killed}", True, (255, 255, 255))
    level_achieved_text = font_small.render(f"Nivel alcanzado: {hero.level}", True, (255, 255, 255))
    score_text = font_big.render(f"Tu puntaje: {score}", True, (255, 255, 255))
    press_key_text = font_small.render("Presioná la tecla espacio para continuar...", True, (200, 200, 200))

    fade_surface = pygame.Surface((constant.SCREEN_WIDTH, constant.SCREEN_HEIGHT))
    fade_surface.fill((0, 0, 0))

    alpha = 0
    while alpha < 255:
        fade_surface.set_alpha(alpha)
        screen.blit(fade_surface, (0, 0))
        screen.blit(game_over_text, game_over_text.get_rect(center=(constant.SCREEN_WIDTH//2, 200)))
        screen.blit(skeletons_killed_text, skeletons_killed_text.get_rect(center=(constant.SCREEN_WIDTH//2, 400)))
        screen.blit(ghosts_killed_text, ghosts_killed_text.get_rect(center=(constant.SCREEN_WIDTH//2, 500)))
        screen.blit(level_achieved_text, level_achieved_text.get_rect(center=(constant.SCREEN_WIDTH//2, 600)))
        screen.blit(score_text, score_text.get_rect(center=(constant.SCREEN_WIDTH//2, 800)))
        pygame.display.update()
        alpha += 5
        pygame.time.delay(100)

    # Esperar cualquier tecla
    waiting = True
    while waiting:
        screen.fill((0, 0, 0))
        screen.blit(game_over_text, game_over_text.get_rect(center=(constant.SCREEN_WIDTH//2, 200)))
        screen.blit(skeletons_killed_text, skeletons_killed_text.get_rect(center=(constant.SCREEN_WIDTH//2, 400)))
        screen.blit(ghosts_killed_text, ghosts_killed_text.get_rect(center=(constant.SCREEN_WIDTH//2, 500)))
        screen.blit(level_achieved_text, level_achieved_text.get_rect(center=(constant.SCREEN_WIDTH//2, 600)))
        screen.blit(score_text, score_text.get_rect(center=(constant.SCREEN_WIDTH//2, 800)))
        screen.blit(press_key_text, press_key_text.get_rect(center=(constant.SCREEN_WIDTH//2, 1000)))
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    waiting = False


def update_and_draw(delta_time):
    global skeletons_killed, ghosts_killed
    # Dibujo el menu
    if menu_active:
        menu.draw_menu(screen)

    if game_started:
        # Fondo
        background.draw_background(screen)

        # Torre
        tower.update()
        tower.draw(screen)

        # Plataformas
        for platform in platforms:
            platform.draw(screen)

        # Tierra
        ground_image = animations.GROUND_IMAGE
        screen.blit(ground_image, (0, constant.GROUND_TILE_HEIGHT))

        # Heroe
        if not game_over:
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
                if isinstance(enemy, Skeleton):
                    skeletons_killed += 1
                    print("Esqueleto")
                elif isinstance(enemy, Ghost):
                    ghosts_killed += 1
                    print("Fantasma")
                
                enemy.destroy()


            # Detecto si impacta la torre
            if tower.hitbox.colliderect(enemy.hitbox):
                tower.trigger_overlay()
                enemy.collisioned = True
                enemy.destroy()
                tower.receive_damage()

            # Una vez muerto lo remuevo de la lista de enemigos
            if not enemy.alive:
                enemies.remove(enemy)

            # Si esta vivo sigue actualizandose y dibujandose
            else:
                enemy.update()
                enemy.draw(screen)

        # Recorro la lista de Almas
        for soul in souls[:]:
            if soul.alive:
                soul.update()
                soul.draw(screen)
                if soul.arrived:
                    hero.experience += soul.value
                    souls.remove(soul)
            else:
                souls.remove(soul)

# Ejecuto el juego
run = True
while run:
    delta_time = clock.tick(constant.FPS) / 1000
    
    update_and_draw(delta_time)

    if game_started and not game_over:
        enemy_spawn_timer += delta_time
        if enemy_spawn_timer >= 3:
            spawn_enemy()
            enemy_spawn_timer = 0

    if game_over:
        for enemy in enemies:
            enemy.destroy()
        for soul in souls:
            soul.destroy()

    events = pygame.event.get()

    for event in events:
        if event.type == pygame.QUIT:
            run = False
        
        if event.type == constant.MUSIC_END_EVENT:
            soundboard.play_next_track()

        if game_started and not game_over:
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
                fade_out(screen)
                score = hero.experience  # Revisar puntaje
                show_game_over_screen(screen, score)

                # Volver al menú
                soundboard.update_music_queue(soundboard.music_menu_queue)
                soundboard.play_next_track()
                game_started = False
                menu_active = True
                enemies.clear()
                skeletons.clear()
                ghosts.clear()
                souls.clear()
                hero.reset()  # Esto requiere que tengas un método para reiniciar al héroe
                tower = Building(constant.SCREEN_WIDTH / 2 - 64, constant.SCREEN_HEIGHT)
                skeletons_killed = 0
                ghosts_killed = 0

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
                        game_over = False
                        game_started = True
                        menu_active = False
                        soundboard.update_music_queue(soundboard.music_game_queue)
                        soundboard.play_next_track()
                        fade_in(screen)
                    elif choice == "Credits":
                        print("Mostrar créditos...")
                    elif choice == "Quit":
                        run = False

    if game_started and not game_over:
        keys = pygame.key.get_pressed()
        hero.pressing_down = keys[pygame.K_s] or keys[pygame.K_DOWN]
        if keys[pygame.K_a] or keys[pygame.K_LEFT]:
            if hero.hitbox.x >= 0: # Limite
                hero.move(-1, 0)
        elif keys[pygame.K_d] or keys[pygame.K_RIGHT]:
            if hero.hitbox.x <= constant.SCREEN_WIDTH: # Limite
                hero.move(1, 0)
        else:
            if hero.on_ground:
                hero.change_animation(animations.ANIM_HERO_IDLE)

    pygame.display.update()

pygame.quit()
print("Fin!")

