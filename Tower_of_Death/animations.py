import pygame
import constant

def scale_image(image, scale):
    scaled_image = pygame.transform.scale(image, 
                                      (image.get_width() * scale, 
                                      image.get_height() * scale))
    return scaled_image

def append_frames(route, animation, frame_count):
    for frame in range (1, frame_count+1):
        image = pygame.image.load(f"{route}{frame}.png")
        image = scale_image(image, constant.SCALE)
        animation.append(image)

def change_animation(character, animation):
    if character.frame_index > len(animation):
        character.reset_frame_index()
    character.animation = animation

def load_assets():
    global ANIM_HERO_IDLE, ANIM_HERO_RUN, ANIM_HERO_ATTACK
    global ANIM_SKELETON_RISE, ANIM_SKELETON_WALK, ANIM_ENEMY_DEATH, ANIM_SOUL
    global TOWER_IMAGE, BACKGROUND_IMAGE, MOUNTAINS_IMAGE, GRAVEYARD_IMAGE, WINDOW_ICON, GROUND_IMAGE, ANIM_HERO_JUMP, ANIM_HERO_FALL, ANIM_GHOST_FLY

    # Icono de la ventana
    WINDOW_ICON = pygame.image.load(r"Assets\Icons\window-icon.png")

    # Torre
    TOWER_IMAGE = pygame.image.load(r"Assets\Environment\sliced-objects\statue.png").convert_alpha()

    # Background
    BACKGROUND_IMAGE = pygame.image.load(r"Assets\Environment\background.png").convert_alpha()
    MOUNTAINS_IMAGE = pygame.image.load(r"Assets\Environment\mountains.png").convert_alpha()
    GRAVEYARD_IMAGE = pygame.image.load(r"Assets\Environment\graveyard.png").convert_alpha()
    GROUND_IMAGE = pygame.image.load(r"Assets\Environment\ground.png").convert_alpha()

    # Animaciones del Heroe

    ANIM_HERO_IDLE = []
    append_frames(r"Assets\Sprites\hero\hero-idle\hero-idle-", ANIM_HERO_IDLE, 4)

    ANIM_HERO_RUN = []
    append_frames(r"Assets\Sprites\hero\hero-run\hero-run-", ANIM_HERO_RUN, 6)

    ANIM_HERO_ATTACK = []
    append_frames(r"Assets\Sprites\hero\hero-attack\hero-attack-", ANIM_HERO_ATTACK, 5)

    ANIM_HERO_JUMP = []
    append_frames(r"Assets\Sprites\hero\hero-jump\hero-jump-", ANIM_HERO_JUMP, 4)

    ANIM_HERO_FALL = []
    append_frames(r"Assets\Sprites\hero\hero-fall\hero-fall-", ANIM_HERO_FALL, 2)

    # Animaciones del Esqueleto

    ANIM_SKELETON_RISE = []
    append_frames(r"Assets\Sprites\skeleton-rise\skeleton-rise-", ANIM_SKELETON_RISE, 4)

    ANIM_SKELETON_WALK = []
    append_frames(r"Assets\Sprites\skeleton\skeleton-", ANIM_SKELETON_WALK, 8)

    # Animaciones del fantasma

    ANIM_GHOST_FLY = []
    append_frames(r"Assets\Sprites\ghost/ghost-", ANIM_GHOST_FLY, 4)

    # Animacion general de muerte enemigo

    ANIM_ENEMY_DEATH = []
    append_frames(r"Assets\Sprites\enemy-death\enemy-death-", ANIM_ENEMY_DEATH, 5)

    ANIM_SOUL = []
    append_frames(r"Assets\Sprites\soul\soul-", ANIM_SOUL, 10)