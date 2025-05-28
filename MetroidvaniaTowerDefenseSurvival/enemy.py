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
    def __init__(self, x, y, width, height, hitbox_width, hitbox_height, base_color, souls):
        # Atributos:
        self.alive = True
        self.dying = False
        self.flip = False
        self.direction = random.choice([-1, 1])  # Con esto randomizo la dirección inicial del enemigo, idealmente después esto dependerá de dónde esté el objetivo.
        self.souls = souls

        # Forma
        self.shape = pygame.Rect(0, 0, width, height)
        self.shape.midbottom = (x, y)
        self.color = base_color

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

        # Inicia la animación de muerte
        if not self.dying:
            self.animation = animations.ANIM_ENEMY_DEATH
            self.frame_index = 0
            self.update_time = pygame.time.get_ticks()
            self.dying = True
            self.anim_locked = True  # Bloqueo hasta que termine la animación de muerte

    def on_animation_unlock(self):
        # Este método se llama automáticamente cuando finaliza una animación bloqueada
        if self.dying:
            soul = Soul(self.shape.centerx, self.shape.centery, [constant.SCREEN_WIDTH / 2, constant.SCREEN_HEIGHT / 2])
            self.souls.append(soul)
            self.alive = False  # Me aseguro que termine la animación de muerte


class Skeleton(Enemy):
    def __init__(self, x, y, souls):
        super().__init__(
            x, y,
            constant.SKELETON_WIDTH, constant.SKELETON_HEIGHT,
            constant.SKELETON_HITBOX_WIDTH, constant.SKELETON_HITBOX_HEIGHT,
            color.GREEN, souls
        )

        # Animación de aparición desde el suelo
        self.animation = animations.ANIM_SKELETON_RISE
        self.image = self.animation[self.frame_index]
        self.anim_locked = True  # Bloqueo inicial hasta que termine la animación de awake
        self.souls = souls

    def on_animation_unlock(self):
        if self.dying:
            soul = Soul(self.shape.centerx, self.shape.centery, [constant.SCREEN_WIDTH / 2, constant.SCREEN_HEIGHT / 2])
            self.souls.append(soul)
            self.alive = False
        else:
            self.animation = animations.ANIM_SKELETON_WALK
            self.reset_frame_index()

    def move(self):
        # Asigno la animación de caminar antes de mover
        self.animation = animations.ANIM_SKELETON_WALK
        super().move()

class Soul:
    def __init__(self, x, y, target_position, speed=3, value=10):
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

    