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

        # Fuente
        self.font = pygame.font.Font("MetroidvaniaTowerDefenseSurvival\Assets\Fonts\Caudex-Regular.ttf", 96)
        self.text_timer = 0
        self.text = ""
        
        # Forma del personaje
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
        self.update_time = pygame.time.get_ticks()
        self.image = self.animation[self.frame_index]

        # Outline (puede servir para feedback in-game)
        self.mask = pygame.mask.from_surface(self.image)
        self.outline = self.mask.outline()

    ### Encapsulamiento ###
    @property
    def experience(self):
        return self.__experience
        
    @experience.setter
    def experience(self, value):
        self.__experience = max(0, min(value, self.__max_experience))
        if self.experience >= self.__max_experience:
            self.level_up()

    @property
    def level(self):
        return self.__level

    def level_up(self):
        self.__level += 1
        self.__experience = 0
        self.__max_experience += 25  # Aumentar dificultad
        self.text = "Level up"
        self.trigger_text()
        print(f"Subiste al nivel {self.__level}")

    def trigger_text(self, duration = 5):  # default: medio segundo
        self.text_timer = time.time() + duration
        
    def reset_frame_index(self):
        self.frame_index = 0

    def update(self):
        # Velocidad base de las animaciones
        cooldown_animation = 150
        # Velocidad de la animacion de ataque
        if self.__is_attacking:
            cooldown_animation = self.__attack_speed

        # Actualizacion de frames de la animacion
        self.image = self.animation[self.frame_index]
        if pygame.time.get_ticks() - self.update_time >= cooldown_animation:
            self.frame_index += 1
            self.update_time = pygame.time.get_ticks()

        # Cuando finaliza la animación
        if self.frame_index >= len(self.animation):
            self.reset_frame_index()
            # Deja de estar anim_locked
            if self.__anim_locked:
                self.__anim_locked = False
            # Remuevo hitbox de ataque
            if self.attack_hitbox_active:
                self.attack_hitbox_active = False
                # Con esto elimino el hitbox, de otra forma seguiría estando en el ultimo lugar donde ataco
                self.attack_hitbox.width = 0
                self.attack_hitbox.height = 0
                self.__is_attacking = False

        # Update de la barra llena de experiencia:
        self.experience_bar_fill = pygame.Rect(32, 32, self.experience, 10)
            
        # Outline
        self.mask = pygame.mask.from_surface(self.image)
        self.outline = self.mask.outline()
                
    def draw(self, screen):
        # Heroe / flip(imagen, bool si flipea x, bool si flipea y)
        flipped_image = pygame.transform.flip(self.image, self.__flip, False)
        screen.blit(flipped_image, self.shape)

        # Hitbox (HERO)
        self.update_hitboxes()
        #pygame.draw.rect(screen, color.RED, self.hitbox, 1)

        # Hitbox (WEAPON)
        #if self.attack_hitbox_active:
        #    pygame.draw.rect(screen, color.RED, self.attack_hitbox, 2)

        # Barra de Experiencia:
        pygame.draw.rect(screen, color.GRAY, self.experience_bar)
        fill_width = (self.experience / self.__max_experience) * self.experience_bar.width
        self.experience_bar_fill = pygame.Rect(self.experience_bar.left, self.experience_bar.top, fill_width, self.experience_bar.height)
        pygame.draw.rect(screen, color.GREEN, self.experience_bar_fill)

        # Texto en pantalla
        if time.time() < self.text_timer:
            
            text_to_show = self.font.render(self.text, True, (color.WHITE))
            text_pos = text_to_show.get_rect()
            text_pos.center = (constant.SCREEN_WIDTH / 2, constant.SCREEN_HEIGHT / 4)
            screen.blit(text_to_show, text_pos)

    def update_hitboxes(self):
        if self.__flip:
            self.hitbox.x = self.shape.x + self.hitbox_offset_x - 20    # Número mágico para evitar que el hitbox quede desplazado al darse vuelta el personaje (TO DO: Encontrar una solucion y evitar el hardcodeo)
        else:
            self.hitbox.x = self.shape.x + self.hitbox_offset_x
        self.hitbox.bottom = self.shape.bottom
        if self.attack_hitbox_active:
            if self.__flip:
                self.attack_hitbox.midright = self.hitbox.midleft
            else:
                self.attack_hitbox.midleft = self.hitbox.midright

    def move(self, axis_x, axis_y):
        if not self.__anim_locked:            
            if axis_x < 0:
                self.__flip = True
            if axis_x > 0:
                self.__flip = False
            self.shape.x += axis_x * self.__speed
            #self.shape.y += axis_y * self.speed (el movimiento en el eje Y no lo usamos por el momento)
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
    
    def idle(self):
        if self.animation != animations.ANIM_HERO_IDLE and not self.__anim_locked:
            self.reset_frame_index()
            self.animation = animations.ANIM_HERO_IDLE

    def draw_outline(self, screen, color):
        outline = self.outline
        if self.__flip:
            outline = [(self.image.get_width() - x, y) for (x, y) in self.outline]
        # Ajusto la posición del contorno al centro actual
        adjusted_outline = [(x + self.shape.left, y + self.shape.top) for (x, y) in outline]
        pygame.draw.lines(screen, color, True, adjusted_outline, 2)
        

