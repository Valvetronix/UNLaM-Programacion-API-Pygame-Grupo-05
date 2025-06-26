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
from transitions import fade_transition, show_game_over_screen

class Game:
    def __init__(self, screen):
        self.screen = screen
        self.clock = pygame.time.Clock()

        # booleans
        self.game_started = False
        self.menu_active = True
        self.game_over = False

        # Fondo
        self.background = Background()

        # HUD
        self.hud = HUD()

        # Consola de sonido
        self.soundboard = Soundboard()
        self.soundboard.play_next_track()

        # Menu
        self.menu = Menu(constant.SCREEN_WIDTH, constant.SCREEN_HEIGHT)

        # Torre
        self.tower = Building(constant.SCREEN_WIDTH / 2 - 64, constant.SCREEN_HEIGHT)

        # Plataformas
        PLATFORM_HEIGHT_CONSTANT = 180
        PLATFORM_HEIGHT_1 = constant.SCREEN_HEIGHT - PLATFORM_HEIGHT_CONSTANT
        PLATFORM_HEIGHT_2 = constant.SCREEN_HEIGHT - PLATFORM_HEIGHT_CONSTANT * 2
        PLATFORM_HEIGHT_3 = constant.SCREEN_HEIGHT - PLATFORM_HEIGHT_CONSTANT * 3

        PLATFORM_WIDTH_CONSTANT = 240
        PLATFORM_CENTER = constant.SCREEN_WIDTH / 2
        PLATFORM_LEFT_WIDTH_1 = PLATFORM_CENTER - PLATFORM_WIDTH_CONSTANT
        PLATFORM_RIGHT_WIDTH_1 = PLATFORM_CENTER + PLATFORM_WIDTH_CONSTANT

        self.platforms = [
            Platform(PLATFORM_CENTER, PLATFORM_HEIGHT_2, 100, 20),
            Platform(PLATFORM_LEFT_WIDTH_1, PLATFORM_HEIGHT_1, 100, 20),
            Platform(PLATFORM_LEFT_WIDTH_1, PLATFORM_HEIGHT_3, 100, 20),
            Platform(PLATFORM_RIGHT_WIDTH_1, PLATFORM_HEIGHT_1, 100, 20),
            Platform(PLATFORM_RIGHT_WIDTH_1, PLATFORM_HEIGHT_3, 100, 20),
        ]

        # Creo al personaje
        self.hero = Hero(constant.HERO_SPAWN_X, constant.HERO_SPAWN_Y, animations.ANIM_HERO_IDLE)

        # Listas de enemigos y almas
        self.enemies = []
        self.skeletons = []
        self.ghosts = []
        self.souls = []
        self.enemy_spawn_timer = 0

        # Contadores de Score
        self.ghosts_killed = 0
        self.skeletons_killed = 0

    # Funcion para spawnear enemigos
    def spawn_enemy(self, level = 1):
        if len(self.skeletons) < level * 2:
            spawn_zone = random.choice([0, 3])
            spawn_zone_width = constant.SCREEN_WIDTH // 4

            x_min = spawn_zone * spawn_zone_width
            x_max = x_min + spawn_zone_width
            x_pos = random.randint(x_min, x_max)

            enemy = Skeleton(x_pos, constant.GROUND_HEIGHT, self.souls)
            self.enemies.append(enemy)

        if level == 1 and len(self.ghosts) < constant.MAX_GHOSTS:
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
            enemy = Ghost(x_pos, y_pos, self.souls, (constant.SCREEN_WIDTH/2))
            self.enemies.append(enemy)

    def update_and_draw(self, delta_time):
        if self.menu_active:
            self.menu.draw_menu(self.screen)

        if self.game_started:
            self.background.draw_background(self.screen)
            self.tower.update()
            self.tower.draw(self.screen)

            for platform in self.platforms:
                platform.draw(self.screen)

            ground_image = animations.GROUND_IMAGE
            self.screen.blit(ground_image, (0, constant.GROUND_TILE_HEIGHT))

            if not self.game_over:
                self.hero.update(delta_time, self.platforms)
                self.hero.draw(self.screen)

            self.hud.update()
            self.hud.update_stats(self.hero.experience, self.hero.max_experience)
            self.hud.draw(self.screen)

            for enemy in self.enemies[:]:
                if self.hero.attack_hitbox.colliderect(enemy.hitbox):
                    if isinstance(enemy, Skeleton):
                        self.skeletons_killed += 1
                    elif isinstance(enemy, Ghost):
                        self.ghosts_killed += 1
                    enemy.destroy()

                if self.tower.hitbox.colliderect(enemy.hitbox):
                    self.tower.trigger_overlay()
                    enemy.collisioned = True
                    enemy.destroy()
                    self.tower.receive_damage()

                if not enemy.alive:
                    self.enemies.remove(enemy)
                else:
                    enemy.update()
                    enemy.draw(self.screen)

            for soul in self.souls[:]:
                if soul.alive:
                    soul.update()
                    soul.draw(self.screen)
                    if soul.arrived:
                        self.hero.experience += soul.value
                        self.souls.remove(soul)
                else:
                    self.souls.remove(soul)

    def start(self):
        run = True
        while run:
            delta_time = self.clock.tick(constant.FPS) / 1000
            self.update_and_draw(delta_time)

            if self.game_started and not self.game_over:
                self.enemy_spawn_timer += delta_time
                if self.enemy_spawn_timer >= 3:
                    self.spawn_enemy()
                    self.enemy_spawn_timer = 0

            if self.game_over:
                for enemy in self.enemies:
                    enemy.destroy()
                for soul in self.souls:
                    soul.destroy()

            events = pygame.event.get()
            for event in events:
                if event.type == pygame.QUIT:
                    run = False

                if event.type == constant.MUSIC_END_EVENT:
                    self.soundboard.play_next_track()

                if self.game_started and not self.game_over:
                    if event.type == pygame.KEYDOWN and event.key == pygame.K_w:
                        self.hero.jump()
                    if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                        self.hero.attack()
                    if event.type == constant.LEVEL_UP_EVENT:
                        self.hud.level_alert(self.hero.level)
                    if event.type == constant.GAME_OVER_EVENT:
                        self.hud.game_over_alert()
                        fade_transition(self.screen, lambda: self.update_and_draw(delta_time), fade_in=False)
                        score = self.hero.experience
                        show_game_over_screen(self.screen, score, self.skeletons_killed, self.ghosts_killed, self.hero.level)
                        self.soundboard.update_music_queue(self.soundboard.music_menu_queue)
                        self.soundboard.play_next_track()
                        self.reset_game()
                    if event.type == constant.ATTACK_EVENT:
                        self.soundboard.play_sound("attack")
                    if event.type == constant.JUMP_EVENT:
                        self.soundboard.play_sound("jump")
                    if event.type == constant.SKELETON_DEATH_EVENT:
                        sound = random.choice([1,2,3,4])
                        self.soundboard.play_sound("hit_1")
                        self.soundboard.play_sound(f"zombie_death_{sound}")

                else:
                    if event.type == pygame.KEYDOWN:
                        if event.key in [pygame.K_LEFT, pygame.K_a]:
                            self.menu.selected = (self.menu.selected - 1) % len(self.menu.menu_items)
                        elif event.key in [pygame.K_RIGHT, pygame.K_d]:
                            self.menu.selected = (self.menu.selected + 1) % len(self.menu.menu_items)
                        elif event.key in [pygame.K_SPACE, pygame.K_RETURN]:
                            choice = self.menu.menu_items[self.menu.selected]
                            if choice == "Start":
                                self.game_over = False
                                self.game_started = True
                                self.menu_active = False
                                self.soundboard.update_music_queue(self.soundboard.music_game_queue)
                                self.soundboard.play_next_track()
                                fade_transition(self.screen, lambda: self.update_and_draw(delta_time), fade_in=True)
                            elif choice == "Credits":
                                print("Mostrar créditos...")
                            elif choice == "Quit":
                                run = False

            if self.game_started and not self.game_over:
                keys = pygame.key.get_pressed()
                self.hero.pressing_down = keys[pygame.K_s] or keys[pygame.K_DOWN]
                if keys[pygame.K_a] or keys[pygame.K_LEFT]:
                    if self.hero.hitbox.x >= 0:
                        self.hero.move(-1, 0)
                elif keys[pygame.K_d] or keys[pygame.K_RIGHT]:
                    if self.hero.hitbox.x <= constant.SCREEN_WIDTH:
                        self.hero.move(1, 0)
                else:
                    if self.hero.on_ground:
                        self.hero.change_animation(animations.ANIM_HERO_IDLE)

            pygame.display.update()

        pygame.quit()
        print("Fin!")

    def reset_game(self):
        self.game_started = False
        self.menu_active = True
        self.enemies.clear()
        self.skeletons.clear()
        self.ghosts.clear()
        self.souls.clear()
        self.hero.reset()
        self.tower = Building(constant.SCREEN_WIDTH / 2 - 64, constant.SCREEN_HEIGHT)
        self.skeletons_killed = 0
        self.ghosts_killed = 0