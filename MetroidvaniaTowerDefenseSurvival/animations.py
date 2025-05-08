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

# Animaciones del Heroe

anim_hero_idle = []
append_frames("MetroidvaniaTowerDefenseSurvival\Assets\Sprites\hero\hero-idle\hero-idle-", anim_hero_idle, 4)

anim_hero_run = []
append_frames("MetroidvaniaTowerDefenseSurvival\Assets\Sprites\hero\hero-run\hero-run-", anim_hero_run, 6)

anim_hero_attack = []
append_frames("MetroidvaniaTowerDefenseSurvival\Assets\Sprites\hero\hero-attack\hero-attack-", anim_hero_attack, 5)

# Animaciones del Esqueleto

anim_skeleton_rise = []
append_frames("MetroidvaniaTowerDefenseSurvival\Assets\Sprites\skeleton-rise\skeleton-rise-", anim_skeleton_rise, 4)

anim_skeleton_walk = []
append_frames("MetroidvaniaTowerDefenseSurvival\Assets\Sprites\skeleton\skeleton-", anim_skeleton_walk, 8)

# Animacion general de muerte enemigo

anim_enemy_death = []
append_frames("MetroidvaniaTowerDefenseSurvival\Assets\Sprites\enemy-death\enemy-death-", anim_enemy_death, 5)