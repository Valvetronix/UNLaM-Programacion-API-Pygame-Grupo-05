import pygame
import constant
import fonts

# Fade in / Fade Out
def fade_transition(screen, draw_callback, fade_in=True, speed=2):
    fade_surface = pygame.Surface((constant.SCREEN_WIDTH, constant.SCREEN_HEIGHT))
    fade_surface.fill((0, 0, 0))

    if fade_in:
        alpha_range = range(255, -1, -speed)
    else:
        alpha_range = range(0, 256, speed)

    for alpha in alpha_range:
        draw_callback()
        fade_surface.set_alpha(alpha)
        screen.blit(fade_surface, (0, 0))
        pygame.display.update()
        pygame.time.delay(10)

# Pantalla Game Over
def show_game_over_screen(screen, score, skeletons_killed, ghosts_killed, level):
    font_big = pygame.font.SysFont(fonts.PATH_CAUDEX_BOLD, 64)
    font_small = pygame.font.SysFont(fonts.PATH_CAUDEX_REGULAR, 32)

    game_over_text = font_big.render("Game Over", True, (255, 255, 255))
    skeletons_text = font_small.render(f"Esqueletos destruidos: {skeletons_killed}", True, (255, 255, 255))
    ghosts_text = font_small.render(f"Fantasmas destruidos: {ghosts_killed}", True, (255, 255, 255))
    level_text = font_small.render(f"Nivel alcanzado: {level}", True, (255, 255, 255))
    score_text = font_big.render(f"Tu puntaje: {score}", True, (255, 255, 255))
    press_key_text = font_small.render("Presioná la tecla espacio para continuar...", True, (200, 200, 200))

    fade_surface = pygame.Surface((constant.SCREEN_WIDTH, constant.SCREEN_HEIGHT))
    fade_surface.fill((0, 0, 0))

    alpha = 0
    while alpha < 255:
        fade_surface.set_alpha(alpha)
        screen.blit(fade_surface, (0, 0))
        screen.blit(game_over_text, game_over_text.get_rect(center=(constant.SCREEN_WIDTH//2, 200)))
        screen.blit(skeletons_text, skeletons_text.get_rect(center=(constant.SCREEN_WIDTH//2, 400)))
        screen.blit(ghosts_text, ghosts_text.get_rect(center=(constant.SCREEN_WIDTH//2, 500)))
        screen.blit(level_text, level_text.get_rect(center=(constant.SCREEN_WIDTH//2, 600)))
        screen.blit(score_text, score_text.get_rect(center=(constant.SCREEN_WIDTH//2, 800)))
        pygame.display.update()
        alpha += 5
        pygame.time.delay(100)

    # Esperar a que se presione espacio
    waiting = True
    while waiting:
        screen.fill((0, 0, 0))
        screen.blit(game_over_text, game_over_text.get_rect(center=(constant.SCREEN_WIDTH//2, 200)))
        screen.blit(skeletons_text, skeletons_text.get_rect(center=(constant.SCREEN_WIDTH//2, 400)))
        screen.blit(ghosts_text, ghosts_text.get_rect(center=(constant.SCREEN_WIDTH//2, 500)))
        screen.blit(level_text, level_text.get_rect(center=(constant.SCREEN_WIDTH//2, 600)))
        screen.blit(score_text, score_text.get_rect(center=(constant.SCREEN_WIDTH//2, 800)))
        screen.blit(press_key_text, press_key_text.get_rect(center=(constant.SCREEN_WIDTH//2, 1000)))
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                waiting = False