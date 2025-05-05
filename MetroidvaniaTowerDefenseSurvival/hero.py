import pygame
import animations
import constant
import color

class Hero():
    def __init__(self, x, y, animation):
        # Forma del personaje
        self.shape = pygame.Rect(0, 0, constant.HERO_WIDTH, constant.HERO_HEIGHT)
        self.shape.midbottom = (x, y)

        # Animacion
        self.animation = animation
        self.frame_index = 0
        self.update_time = pygame.time.get_ticks()
        self.image = self.animation[self.frame_index]

        # Hitbox
        self.hitbox = pygame.Rect(0, 0, constant.HERO_HITBOX_WIDTH, constant.HERO_HITBOX_HEIGHT)
        self.hitbox.midbottom = self.shape.midbottom
        self.hitbox_offset_x = 70
        
        # Outline
        self.mask = pygame.mask.from_surface(self.image)
        self.outline = self.mask.outline()

        self.flip = False
        self.is_moving_left = False
        self.is_moving_right = False
        self.anim_locked = False
        self.is_aura_activated = False

    def reset_frame_index(self):
        self.frame_index = 0

    def update(self):
        cooldown_animation = 150
        self.image = self.animation[self.frame_index]
        if pygame.time.get_ticks() - self.update_time >= cooldown_animation:
            self.frame_index += 1
            self.update_time = pygame.time.get_ticks()
        if self.frame_index >= len(self.animation):
            self.reset_frame_index()
            if self.anim_locked:
                self.anim_locked = False
        self.mask = pygame.mask.from_surface(self.image)
        self.outline = self.mask.outline()
                
    def draw(self, screen):
        self.hitbox.x = self.shape.x + self.hitbox_offset_x
        self.hitbox.y = self.shape.y
        pygame.draw.rect(screen, color.BLUE, self.hitbox, 1)
        flipped_image = pygame.transform.flip(self.image, self.flip, False)
        screen.blit(flipped_image, self.shape)

    def draw_outline(self, screen, color):
        outline = self.outline
        if self.flip:
            outline = [(self.image.get_width() - x, y) for (x, y) in self.outline]

        # Ajustamos la posición del contorno al centro actual
        adjusted_outline = [(x + self.shape.left, y + self.shape.top) for (x, y) in outline]
        pygame.draw.lines(screen, color, True, adjusted_outline, 2)


    def move(self, delta_x, delta_y):
        if not self.anim_locked:
            if delta_x < 0:
                self.flip = True
            if delta_x > 0:
                self.flip = False
            self.shape.x += delta_x
            self.shape.y += delta_y
            self.animation = animations.anim_hero_run

    def attack(self):
        if not self.anim_locked:
            self.anim_locked = True
            self.reset_frame_index()
            self.animation = animations.anim_hero_attack
    
    def idle(self):
        if self.animation != animations.anim_hero_idle:
            self.reset_frame_index()
            self.animation = animations.anim_hero_idle

