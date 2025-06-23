import pygame
import constant
import animations
import time
import random

class Explosion:
    def __init__(self, x, y, scale=1):
        self.animation = animations.ANIM_ENEMY_DEATH
        self.frame_index = 0
        self.last_update = pygame.time.get_ticks()
        self.scale = scale
        self.image = pygame.transform.scale(self.animation[0], (int(self.animation[0].get_width() * scale), int(self.animation[0].get_height() * scale)))
        self.rect = self.image.get_rect(center=(x, y))
        self.alive = True

    def update(self):
        cooldown = 10
        now = pygame.time.get_ticks()
        if now - self.last_update > cooldown:
            self.frame_index += 1
            self.last_update = now
            if self.frame_index >= len(self.animation):
                self.alive = False
            else:
                frame = self.animation[self.frame_index]
                w = int(frame.get_width() * self.scale)
                h = int(frame.get_height() * self.scale)
                self.image = pygame.transform.scale(frame, (w, h))
                self.rect = self.image.get_rect(center=self.rect.center)

    def draw(self, screen):
        if self.alive:
            screen.blit(self.image, self.rect)


class Building:
    def __init__(self, x, y):
        self.hp = 0
        self.shape = pygame.Rect(0, 0, constant.TOWER_WIDTH, constant.TOWER_HEIGHT)
        self.shape.midbottom = (x, y)
        self.image = animations.TOWER_IMAGE
        self.scaled_image = pygame.transform.scale(self.image, (constant.TOWER_WIDTH, constant.TOWER_HEIGHT))

        self.hitbox = pygame.Rect(0, 0, constant.TOWER_HITBOX_WIDTH, constant.TOWER_HITBOX_HEIGHT)
        self.hitbox.midbottom = (x + 64, y)

        # Overlay
        self.destroying = False
        self.destruction_start = 0
        self.flash_timer = 0
        self.flash_interval = 0.1
        self.show_overlay = False
        self.original_x = self.shape.x

        # Explosiones
        self.explosions = []
        self.big_explosion_played = False

        # Estado final
        self.destroyed = False

    def draw_overlay_on_image(self, screen):
        overlay_image = self.scaled_image.copy()
        red_tint = pygame.Surface(overlay_image.get_size(), pygame.SRCALPHA)
        red_tint.fill((255, 0, 0, 100))
        overlay_image.blit(red_tint, (0, 0), special_flags=pygame.BLEND_RGBA_MULT)
        screen.blit(overlay_image, self.shape.topleft)

    def receive_damage(self):
        self.trigger_overlay()
        self.hp -= 1
        if self.hp <= 0:
            pygame.event.post(pygame.event.Event(constant.GAME_OVER_EVENT))
            self.destroy()
        print("Tower HP:", self.hp)

    def trigger_overlay(self, duration=0.5):
        self.flash_interval = duration

    def destroy(self):
        if not self.destroying:
            self.destroying = True
            self.destruction_start = time.time()
            self.flash_timer = time.time()

    def update(self):
        if self.destroyed:
            return

        if self.destroying:
            elapsed = time.time() - self.destruction_start

            # Vibración horizontal
            self.shape.x = self.original_x + random.randint(-3, 3)
            self.hitbox.x = self.shape.x + 64

            # Caída
            if elapsed <= 10:
                self.shape.y += 1
                self.hitbox.y += 1

            # Titileo rojo
            if time.time() - self.flash_timer > self.flash_interval:
                self.show_overlay = not self.show_overlay
                self.flash_timer = time.time()

            # Explosiones pequeñas
            if elapsed < 8 and random.random() < 0.15:
                px = self.shape.left + random.randint(0, self.shape.width)
                py = self.shape.top + random.randint(0, self.shape.height)
                self.explosions.append(Explosion(px, py, scale=1))

            # Explosión final
            if not self.big_explosion_played and elapsed >= 8:
                self.big_explosion_played = True
                cx, cy = self.shape.center
                self.explosions.append(Explosion(cx, cy, scale=5))

            if elapsed > 10:
                self.destroying = False
                self.destroyed = True
                self.shape.size = (0, 0)
                self.hitbox.size = (0, 0)

        for exp in self.explosions[:]:
            exp.update()
            if not exp.alive:
                self.explosions.remove(exp)

    def draw(self, screen):
        if self.destroyed:
            return

        if self.destroying and self.show_overlay:
            self.draw_overlay_on_image(screen)
        else:
            screen.blit(self.scaled_image, self.shape)

        for exp in self.explosions:
            exp.draw(screen)

# class Building:
#     def __init__(self, x, y):
#         self.hp = 1
#         self.dying = False
#         self.explosion_animation = animations.ANIM_ENEMY_DEATH  # Reutilizamos animación
#         self.explosion_index = 0
#         self.explosion_update_time = 0
#         self.explosion_image = None
#         self.destroyed = False
#         self.shape = pygame.Rect(0, 0, constant.TOWER_WIDTH, constant.TOWER_HEIGHT)
#         self.shape.midbottom = (x, y)
#         self.image = animations.TOWER_IMAGE
#         self.scaled_image = pygame.transform.scale(self.image, (constant.TOWER_WIDTH, constant.TOWER_HEIGHT))

#         self.hitbox = pygame.Rect(0, 0, constant.TOWER_HITBOX_WIDTH, constant.TOWER_HITBOX_HEIGHT)
#         self.hitbox.midbottom = (x + 64, y)

#         # Outline (puede servir para feedback in-game)
#         self.mask = pygame.mask.from_surface(self.scaled_image)
#         self.outline = self.mask.outline()
#         self.outline_timer = 0
        
#     def draw(self, screen):
#         if self.destroyed:
#                 return

#         if self.dying:
#             # Caída de la torre
#             self.shape.y += 5  # Velocidad de caída
#             self.hitbox.y += 5

#             # Reproduzco la explosión
#             now = pygame.time.get_ticks()
#             if now - self.explosion_update_time > 100:  # velocidad de animación
#                 self.explosion_index += 1
#                 if self.explosion_index < len(self.explosion_animation):
#                     self.explosion_image = pygame.transform.scale(
#                         self.explosion_animation[self.explosion_index],
#                         (self.shape.width, self.shape.height)
#                     )
#                     self.explosion_update_time = now
#                 else:
#                     # Fin de la explosión
#                     self.destroyed = True
#                     return

#             # Dibujar explosión
#             if self.explosion_image:
#                 screen.blit(self.explosion_image, self.shape)

#         else:
#             screen.blit(self.scaled_image, self.shape)

#             if time.time() < self.outline_timer:
#                 self.draw_overlay(screen)

#     def draw_outline(self, screen, color):
#         # Ajusto la posición del contorno al centro actual
#         adjusted_outline = [(x + self.shape.left, y + self.shape.top) for (x, y) in self.outline]
#         pygame.draw.lines(screen, color, True, adjusted_outline, 3)

#     def draw_overlay(self, screen):
#         # Clonamos la imagen original con formato alpha
#         overlay_image = self.scaled_image.copy()

#         # Creamos una superficie roja con alfa y la mezclamos con la imagen
#         red_tint = pygame.Surface(overlay_image.get_size(), pygame.SRCALPHA)
#         red_tint.fill((255, 0, 0, 100))  # Rojo semitransparente

#         # Usamos BLEND_RGBA_MULT para aplicar el tinte solo donde hay pixeles visibles
#         overlay_image.blit(red_tint, (0, 0), special_flags=pygame.BLEND_RGBA_MULT)

#         # Dibujamos la imagen final con tinte sobre la pantalla
#         screen.blit(overlay_image, self.shape.topleft)    

#     def trigger_outline(self, duration=0.5):  # default: medio segundo
#         self.outline_timer = time.time() + duration
        
#     def destroy(self):
#         self.dying = True
#         self.explosion_index = 0
#         self.explosion_update_time = pygame.time.get_ticks()
#         self.explosion_image = pygame.transform.scale(
#             self.explosion_animation[0], (self.shape.width, self.shape.height)
#         )  

#     def receive_damage(self):
#         self.trigger_outline()
#         self.hp -= 1
#         if self.hp <= 0:
#             pygame.event.post(pygame.event.Event(constant.GAME_OVER_EVENT))
#             self.destroy()
#         print(self.hp)