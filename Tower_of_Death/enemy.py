import pygame
import color
import constant
import animations
import random
import pygame
import color
import constant
import animations
import random

class Enemy:
    def __init__(self, x, y, width, height, hitbox_width, hitbox_height, souls):
        # Atributos:
        self.alive = True
        self.dying = False # sirve para las animaciones
        self.flip = False
        self.direction = random.choice([-1, 1])  # Con esto randomizo la dirección inicial del enemigo, idealmente después esto dependerá de dónde esté el objetivo.
        self.souls = souls
        self.collisioned = False # Si choco contra la torre

        # Forma
        self.shape = pygame.Rect(0, 0, width, height)
        self.shape.midbottom = (x, y)

        # Hitbox
        self.hitbox = pygame.Rect(0, 0, hitbox_width, hitbox_height)
        self.hitbox.midbottom = self.shape.midbottom

        # Animación (debe asignarla la subclase)
        self.animation = []
        self.frame_index = 0
        self.update_time = pygame.time.get_ticks()
        self.image = None

        # Bloqueo de animaciones (por ejemplo, para esperar a que termine una animación antes de continuar)
        self.anim_locked = False

    def draw(self, screen):
        flipped_image = pygame.transform.flip(self.image, self.flip, False)
        screen.blit(flipped_image, self.shape)
        #pygame.draw.rect(screen, color.RED, self.hitbox, 1)

    def reset_frame_index(self):
        self.frame_index = 0

    def update(self):
        if not self.dying and not self.anim_locked:
            self.move()
            # Detecto si toca los bordes de la pantalla e invierto la dirección
            if self.shape.left <= 0:
                self.direction = 1
            elif self.shape.right >= constant.SCREEN_WIDTH:
                self.direction = -1

        self.update_animation()

    def update_animation(self, cooldown=150):
        # Velocidad base de las animaciones
        if self.frame_index < len(self.animation):
            self.image = self.animation[self.frame_index]
            if pygame.time.get_ticks() - self.update_time >= cooldown:
                self.frame_index += 1
                self.update_time = pygame.time.get_ticks()
        else:
            if self.anim_locked:
                self.on_animation_unlock()
                self.anim_locked = False
            self.reset_frame_index()

    def move(self):
        self.shape.x += self.direction
        self.flip = self.direction > 0
        self.update_hitboxes()

    def update_hitboxes(self):
        self.hitbox.x = self.shape.x
        self.hitbox.bottom = self.shape.bottom

    def destroy(self):
        # Elimino hitbox para evitar colisiones
        self.hitbox.width = 0
        self.hitbox.height = 0
        pygame.event.post(pygame.event.Event(constant.SKELETON_DEATH_EVENT))

        # Inicia la animación de muerte
        if not self.dying:
            self.animation = animations.ANIM_ENEMY_DEATH
            self.frame_index = 0
            self.update_time = pygame.time.get_ticks()
            self.dying = True
            self.anim_locked = True  # Bloqueo hasta que termine la animación de muerte

    def on_animation_unlock(self):
        # Este método se llama automáticamente cuando finaliza una animación
        if self.dying and not self.collisioned:
            soul = Soul(self.shape.centerx, self.shape.centery, [constant.SCREEN_WIDTH / 2, constant.SCREEN_HEIGHT / 2])
            self.souls.append(soul)
            self.alive = False
        # Me aseguro que termine la animación de muerte
        elif self.dying:
            self.alive = False
    
    def draw_overlay(self, screen):
        # Clonamos la imagen original con formato alpha
        overlay_image = self.scaled_image.copy()

        # Creamos una superficie roja con alfa y la mezclamos con la imagen
        red_tint = pygame.Surface(overlay_image.get_size(), pygame.SRCALPHA)
        red_tint.fill((255, 0, 0, 100))  # Rojo semitransparente

        # Usamos BLEND_RGBA_MULT para aplicar el tinte solo donde hay pixeles visibles
        overlay_image.blit(red_tint, (0, 0), special_flags=pygame.BLEND_RGBA_MULT)

        # Dibujamos la imagen final con tinte sobre la pantalla
        screen.blit(overlay_image, self.shape.topleft)  

class Skeleton(Enemy):
    def __init__(self, x, y, souls):
        super().__init__(
            x, y,
            constant.SKELETON_WIDTH, constant.SKELETON_HEIGHT,
            constant.SKELETON_HITBOX_WIDTH, constant.SKELETON_HITBOX_HEIGHT, souls
        )

        # Animación de aparición desde el suelo
        self.animation = animations.ANIM_SKELETON_RISE
        self.image = self.animation[self.frame_index]
        self.anim_locked = True  # Bloqueo inicial hasta que termine la animación de awake
        self.souls = souls

    def on_animation_unlock(self):
        if self.dying and not self.collisioned:
            soul = Soul(self.shape.centerx, self.shape.centery, [constant.SCREEN_WIDTH / 2, constant.SCREEN_HEIGHT / 2])
            self.souls.append(soul)
            self.alive = False
        elif self.dying:
            self.alive = False 
        else:
            self.animation = animations.ANIM_SKELETON_WALK
            self.reset_frame_index()

    def move(self):
        # Asigno la animación de caminar antes de mover
        self.animation = animations.ANIM_SKELETON_WALK
        super().move()

class Ghost(Enemy):
    #def __init__(self, x, y, width, height, hitbox_width, hitbox_height, base_color, souls):
    def __init__(self, x, y, souls, target_position):
        super().__init__(
            x, y,
            constant.GHOST_WIDTH, constant.GHOST_HEIGHT,
            constant.GHOST_HITBOX_WIDTH, constant.GHOST_HITBOX_HEIGHT, souls
        )
        self.animation = animations.ANIM_GHOST_FLY
        self.image = self.animation[self.frame_index]
        self.target_position = target_position
        self.speed = 3
    
    def move(self):
        # Calculo la dirección hacia el objetivo
        if self.target_position > self.shape.centerx:
            self.direction = 1
        elif self.target_position < self.shape.centerx:
            self.direction = -1

        self.shape.x += self.direction * self.speed
        self.flip = self.direction < 0
        self.update_hitboxes()

class Soul:
    def __init__(self, x, y, target_position, speed=4, value=10):
        self.animation = animations.ANIM_SOUL
        self.frame_index = 0
        self.update_time = pygame.time.get_ticks()
        self.image = self.animation[self.frame_index]
        self.position = pygame.Vector2(x, y)
        self.target = pygame.Vector2(target_position)
        self.speed = speed
        self.value = value
        self.arrived = False
        self.shape = self.image.get_rect(midbottom=(x, y))
        self.alive = True

    def update(self):
        # Animación
        cooldown = 150
        self.image = self.animation[self.frame_index]
        if pygame.time.get_ticks() - self.update_time >= cooldown:
            self.frame_index = (self.frame_index + 1) % len(self.animation)
            self.update_time = pygame.time.get_ticks()

        # Movimiento
        if not self.arrived:
            direction = self.target - self.position
            distance = direction.length()
            if distance < self.speed:
                self.arrived = True
            else:
                direction = direction.normalize()
                self.position += direction * self.speed
                self.shape.center = (round(self.position.x), round(self.position.y))

    def draw(self, screen):
        # Dirección de movimiento
        direction = self.target - self.position
        if direction.length() > 0:
            angle = -direction.angle_to(pygame.Vector2(0, -1))  # Comparado con arriba
        else:
            angle = 0

        # Frame actual de la animación
        self.image = self.animation[self.frame_index]

        # Rotar la imagen
        rotated_image = pygame.transform.rotate(self.image, angle)

        # Obtener rect rotado con el pivote en el centro inferior
        rotated_rect = rotated_image.get_rect(midbottom=self.shape.midbottom)

        # Dibujar el sprite rotado
        screen.blit(rotated_image, rotated_rect)

    def destroy(self):
        self.alive = False

    