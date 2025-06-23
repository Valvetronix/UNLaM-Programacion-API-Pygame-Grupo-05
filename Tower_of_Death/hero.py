import pygame
import animations
import constant
import color
import time

class Hero:
    def __init__(self, x, y, animation):
        # Atributos
        self.__level = 1
        self.__experience = 0
        self.__max_experience = 100
        self.__speed = 5
        self.__attack_speed = 80
        self.__flip = False
        self.__anim_locked = False
        self.__is_attacking = False
        self.__pressing_down = False
        self.jumped = False
        self.coyote_counter = 0
        self.coyote_timer = 0.1 # Segundos
        self.air_attack_hold = False

        # SALTO
        self.vel_y = 0
        self.gravity = 1
        self.jump_strength = -20
        self.on_ground = True
        
        # Cargo la animación inicial
        self.animation = animation
        self.frame_index = 0
        self.update_time = pygame.time.get_ticks()
        self.image = self.animation[self.frame_index]

        # Construyo el rect del héroe a partir de la imagen
        self.shape = pygame.Rect(0, 0, constant.HERO_WIDTH, constant.HERO_HEIGHT)
        self.shape.midbottom = (x, y)

        # Hitbox (HERO)
        self.hitbox = pygame.Rect(0, 0, constant.HERO_HITBOX_WIDTH, constant.HERO_HITBOX_HEIGHT)
        self.hitbox.midbottom = (x, y)
        self.hitbox_offset_x = 90

        # Hitbox (WEAPON)
        self.attack_hitbox = pygame.Rect(0, 0, constant.HERO_ATTACK_HITBOX_WIDTH, constant.HERO_ATTACK_HITBOX_HEIGHT)
        self.attack_hitbox_active = False

        # Barra de experiencia
        self.experience_bar = pygame.Rect(32, 32, constant.SCREEN_WIDTH - 64, 10)
        self.experience_bar_fill = pygame.Rect(32, 32, self.experience, 10)

        # Animacion
        self.animation = animation
        self.frame_index = 0
        # Lambda para resetear el frame_index a 0 luego de finalizar una animación
        self.reset_frame_index = lambda: setattr(self, 'frame_index', 0)
        self.update_time = pygame.time.get_ticks()
        self.image = self.animation[self.frame_index]

        # Outline (puede servir para feedback in-game)
        self.mask = pygame.mask.from_surface(self.image)
        self.outline = self.mask.outline()

    ### Encapsulamiento ###
    @property
    def experience(self):
        return self.__experience
    
    @property
    def max_experience(self):
        return self.__max_experience
        
    @experience.setter
    def experience(self, value):
        self.__experience = max(0, min(value, self.__max_experience))
        if self.experience >= self.__max_experience:
            self.level_up()

    @property
    def level(self):
        return self.__level
    
    @property
    def pressing_down(self):
        return self.__pressing_down
    
    @pressing_down.setter
    def pressing_down(self, value):
        self.__pressing_down = value

    def level_up(self):
        self.__level += 1
        self.__experience = 0
        self.__max_experience += 25     
        # EVENTO LEVEL UP
        pygame.event.post(pygame.event.Event(constant.LEVEL_UP_EVENT))

    def update(self, delta_time, platforms=[]):
        # Velocidad base de las animaciones
        cooldown_animation = 150
        # Velocidad de la animacion de ataque
        if self.__is_attacking:
            cooldown_animation = self.__attack_speed
        
        # Gravedad
        self.on_ground = False
            
        if not self.on_ground or self.vel_y < 0:
            self.vel_y += self.gravity
            self.shape.y += self.vel_y
            self.update_hitboxes()

         # Chequeo colision con el suelo   
        if self.hitbox.bottom >= constant.GROUND_HEIGHT:
            self.shape.bottom = constant.GROUND_HEIGHT
            self.vel_y = 0
            self.on_ground = True
            self.update_hitboxes()
        
        # Chequeo colisión con plataformas
        for platform in platforms:
            if self.hitbox.colliderect(platform.rect) and self.vel_y >= 0 and not self.pressing_down:
                if self.hitbox.bottom - self.vel_y <= platform.rect.top + 5: #coyote running
                    self.shape.bottom = platform.rect.top
                    self.vel_y = 0
                    self.on_ground = True
                    self.update_hitboxes()

        # Coyote Time
        if self.on_ground:
            self.coyote_counter = self.coyote_timer
        else:
            self.coyote_counter -= delta_time
    
        # Animación 

        # Actualizacion de frames de la animacion
        if pygame.time.get_ticks() - self.update_time >= cooldown_animation:
            self.frame_index += 1
            self.update_time = pygame.time.get_ticks()

        # Cuando finaliza la animación
        if self.frame_index >= len(self.animation):
            self.reset_frame_index()
            if self.__is_attacking and not self.on_ground:
                self.frame_index = len(self.animation) - 1
                self.air_attack_hold = True  # <- activo congelamiento en el ultimo frame de la animacion de ataque en el aire hasta que toque el suelo.
            else:
                self.reset_frame_index()
                if self.__anim_locked:
                    self.__anim_locked = False
                if self.attack_hitbox_active:
                    self.attack_hitbox_active = False
                    self.attack_hitbox.width = 0    # <- aca elimino el hitbox del ataque, si no seguiría en el ultimo lugar.
                    self.attack_hitbox.height = 0
                    self.__is_attacking = False

        self.image = self.animation[self.frame_index]
        
        if not self.__is_attacking:
            if not self.on_ground:
                if self.vel_y < 0 and self.jumped:
                    self.change_animation(animations.ANIM_HERO_JUMP)
                elif self.vel_y >= 0:
                    self.change_animation(animations.ANIM_HERO_FALL)
            else:
                if self.animation != animations.ANIM_HERO_RUN and self.animation != animations.ANIM_HERO_IDLE:
                    self.change_animation(animations.ANIM_HERO_IDLE)

        # Update de la barra llena de experiencia:
        self.experience_bar_fill = pygame.Rect(32, 32, self.experience, 10)

        # Hitbox
        self.update_hitboxes()
            
        # Outline
        self.mask = pygame.mask.from_surface(self.image)
        self.outline = self.mask.outline()
                
    def draw(self, screen):
        # Heroe / flip(imagen, bool si flipea x, bool si flipea y)
        flipped_image = pygame.transform.flip(self.image, self.__flip, False)
        screen.blit(flipped_image, self.shape)

        # Hitbox (HERO)
        #pygame.draw.rect(screen, color.RED, self.hitbox, 1)

        #pygame.draw.rect(screen, color.RED, self.shape, 1)

        # Hitbox (WEAPON)
        #if self.attack_hitbox_active:
        #    pygame.draw.rect(screen, color.RED, self.attack_hitbox, 2)

    def update_hitboxes(self):
        if self.__flip:
            self.hitbox.x = self.shape.x + self.hitbox_offset_x - 20
        else:
            self.hitbox.x = self.shape.x + self.hitbox_offset_x
        self.hitbox.bottom = self.shape.bottom
        if self.attack_hitbox_active:
            if self.__flip:
                self.attack_hitbox.midright = self.hitbox.midleft
            else:
                self.attack_hitbox.midleft = self.hitbox.midright

    def move(self, axis_x, axis_y):
        if axis_x !=  0 and not self.__anim_locked or not self.on_ground:            
            if axis_x < 0:
                self.__flip = True
            if axis_x > 0:
                self.__flip = False
            self.shape.x += axis_x * self.__speed
            #self.shape.y += axis_y * self.speed (el movimiento en el eje Y no lo usamos por el momento)
            if self.on_ground:
                self.animation = animations.ANIM_HERO_RUN

    def attack(self):
        if not self.__anim_locked:
            self.__anim_locked = True
            self.__is_attacking = True
            self.reset_frame_index()
            self.animation = animations.ANIM_HERO_ATTACK
            self.attack_hitbox_active = True
            self.attack_hitbox.width = constant.HERO_ATTACK_HITBOX_WIDTH
            self.attack_hitbox.height = constant.HERO_ATTACK_HITBOX_HEIGHT
            # EVENTO ATAQUE (para el sonido)
            pygame.event.post(pygame.event.Event(constant.ATTACK_EVENT))
             
    def change_animation(self, animation):
        if self.animation != animation and not self.__anim_locked:
            self.reset_frame_index()
            self.animation = animation

    def draw_outline(self, screen, color):
        outline = self.outline
        if self.__flip:
            outline = [(self.image.get_width() - x, y) for (x, y) in self.outline]
        # Ajusto la posición del contorno al centro actual
        adjusted_outline = [(x + self.shape.left, y + self.shape.top) for (x, y) in outline]
        pygame.draw.lines(screen, color, True, adjusted_outline, 2)
        
    def jump(self):
        if (self.on_ground or self.coyote_counter > 0) and not self.__anim_locked:
            self.vel_y = self.jump_strength
            self.on_ground = False
            self.jumped = True
            self.animation = animations.ANIM_HERO_JUMP
            # EVENTO SALTO (para el sonido)
            pygame.event.post(pygame.event.Event(constant.JUMP_EVENT))

    def reset(self):
        self.__init__(constant.HERO_SPAWN_X, constant.HERO_SPAWN_Y, animations.ANIM_HERO_IDLE)

