import pygame

class Soundboard:
    def __init__(self):
        pygame.mixer.init()
        
        # Diccionario de sonidos
        self.sounds = {
            "attack": pygame.mixer.Sound("Assets/Sounds/melee_attack_1.wav"),
            "zombie_death": pygame.mixer.Sound("Assets/Sounds/zombieDeath1.wav"),
            "jump": pygame.mixer.Sound("Assets/Sounds/jump.wav"),
            "land": pygame.mixer.Sound("Assets/Sounds/land.wav")
        }

        # Seteo volumen
        for sound in self.sounds.values():
            sound.set_volume(0.4)

        # Música
        self.music_path = "Assets/Music/theme.ogg"
        self.music_volume = 0.3
        pygame.mixer.music.set_volume(self.music_volume)

    def play_sound(self, sound):
        if sound in self.sounds:
            self.sounds[sound].play()
        else:
            print(f"[SFX] Sonido '{sound}' no encontrado.")

    def play_music(self, loop=True):
        pygame.mixer.music.load(self.music_path)
        pygame.mixer.music.play(-1 if loop else 0)

    def stop_music(self):
        pygame.mixer.music.stop()

    def pause_music(self):
        pygame.mixer.music.pause()

    def resume_music(self):
        pygame.mixer.music.unpause()

    def set_music_volume(self, volume):
        self.music_volume = max(0.0, min(1.0, volume))
        pygame.mixer.music.set_volume(self.music_volume)

    def set_sfx_volume(self, volume):
        for sound in self.sounds.values():
            sound.set_volume(volume)
    