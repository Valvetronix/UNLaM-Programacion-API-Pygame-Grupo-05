import pygame
import color
import constant
import animations
import random

class Enemy:
    def __init__(self, x, y):
        # Variables:
        self.alive = True
        self.dying = False
        self.awake = False
        self.flip = False
        self.direction = random.choice([-1, 1]) # Con esto randomizo la direccion inicial del enemigo, idealmente despues esto dependera de donde este el objetivo del enemigo.

        # Forma
        self.shape = pygame.Rect(0, 0, constant.SKELETON_WIDTH, constant.SKELETON_HEIGHT)
        self.shape.midbottom = (x, y)
        self.color = color.GREEN

        # Hitbox
        self.hitbox = pygame.Rect(0, 0, constant.ENEMY_HITBOX_WIDTH, constant.ENEMY_HITBOX_HEIGHT)
        self.hitbox.midbottom = self.shape.midbottom

        # Animacion
        self.animation = animations.anim_skeleton_rise
        self.frame_index = 0
        self.update_time = pygame.time.get_ticks()
        self.image = self.animation[self.frame_index]

    def draw(self, screen):
        flipped_image = pygame.transform.flip(self.image, self.flip, False)
        screen.blit(flipped_image, self.shape)
        pygame.draw.rect(screen, color.RED, self.hitbox, 1)

    def reset_frame_index(self):
        self.frame_index = 0

    def update(self):
        # Velocidad base de las animaciones
        cooldown_animation = 150

        # Actualizacion de frames de la animacion
        if self.frame_index < len(self.animation):
            self.image = self.animation[self.frame_index]
            if pygame.time.get_ticks() - self.update_time >= cooldown_animation:
                self.frame_index += 1
                self.update_time = pygame.time.get_ticks()

        else:   # Cuando finaliza la animación
            if self.frame_index >= len(self.animation):
                if not self.awake:
                    self.awake = True
                if self.dying:
                    self.alive = False  # Me aseguro que termine la animacion de muerte                
                else:
                    self.reset_frame_index()

        if not self.dying and self.awake:
            self.walk()
            # Detecto si toca los bordes de la pantalla e invierto la direccion
            if self.shape.left <= 0:
                self.direction = 1
            elif self.shape.right >= constant.SCREEN_WIDTH:
                self.direction = -1
            
    def walk(self):
        self.animation = animations.anim_skeleton_walk
        self.shape.x += self.direction
        self.flip = self.direction > 0
        self.update_hitboxes()

    def update_hitboxes(self):
        self.hitbox.x = self.shape.x
        self.hitbox.bottom = self.shape.bottom

    def destroy(self):
        # elimino hitbox para evitar colisiones
        self.hitbox.width = 0
        self.hitbox.height = 0

        # inicia la animacion de muerte
        if not self.dying:
            self.animation = animations.anim_enemy_death
            self.frame_index = 0
            self.update_time = pygame.time.get_ticks()
            self.dying = True

