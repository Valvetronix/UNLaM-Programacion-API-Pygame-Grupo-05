import pygame
import random
import constant

class Soundboard:
    def __init__(self):
        pygame.mixer.init()
        
        # SFX
        self.sounds = {
            "attack": pygame.mixer.Sound("Assets/Sounds/melee_attack_1.wav"),
            "zombie_death_1": pygame.mixer.Sound("Assets/Sounds/zombieDeath1.wav"),
            "zombie_death_2": pygame.mixer.Sound("Assets/Sounds/zombieDeath2.wav"),
            "zombie_death_3": pygame.mixer.Sound("Assets/Sounds/zombieDeath3.wav"),
            "zombie_death_4": pygame.mixer.Sound("Assets/Sounds/zombieDeath4.wav"),
            "hit_1": pygame.mixer.Sound("Assets/Sounds/hit1.wav"),
            "hit_2": pygame.mixer.Sound("Assets/Sounds/hit2.wav"),
            "hit_3 ": pygame.mixer.Sound("Assets/Sounds/hit3.wav"),
            "hit_4 ": pygame.mixer.Sound("Assets/Sounds/hit4.wav"),
            "jump": pygame.mixer.Sound("Assets/Sounds/jump.wav"),
            "land": pygame.mixer.Sound("Assets/Sounds/land.wav"),
        }

        # Tracks
        self.music = {
            "menu_track_1": "Assets/Music/menu-track-1.ogg",
            "menu_track_2": "Assets/Music/menu-track-2.ogg",
            "menu_track_3": "Assets/Music/menu-track-3.ogg",
            "game_track_1": "Assets/Music/game-track-1.ogg",
            "game_track_2": "Assets/Music/game-track-2.ogg",
            "game_track_3": "Assets/Music/game-track-3.ogg",
            "game_track_4": "Assets/Music/game-track-4.ogg",
            "game_track_5": "Assets/Music/game-track-5.ogg",
            "game_track_6": "Assets/Music/game-track-6.ogg",
            "game_track_7": "Assets/Music/game-track-7.ogg",
            "game_track_8": "Assets/Music/game-track-8.ogg",
            "game_track_9": "Assets/Music/game-track-9.ogg",
            "game_track_10": "Assets/Music/game-track-10.ogg"
        }

        # Queue procedural de tracks
        self.music_queue = ["menu_track_3"]
        self.music_menu_queue = ["menu_track_3"]
        self.music_game_queue = ["game_track_3", "game_track_3", "game_track_8", "game_track_3", "game_track_3", "game_track_7"]
        self.current_track_index = 0

        # Configuraciones de volumen
        for sound in self.sounds.values():
            sound.set_volume(0.4)

        self.music_volume = 0.3
        pygame.mixer.music.set_volume(self.music_volume)

        # Evento al finalizar una pista
        pygame.mixer.music.set_endevent(constant.MUSIC_END_EVENT)

    def play_sound(self, sound):
        if sound in self.sounds:
            self.sounds[sound].play()
        else:
            print(f"[SFX] Sonido '{sound}' no encontrado.")

    def play_next_track(self):
        if not self.music_queue:
            print("[OST] La cola de música está vacía.")
            return

        track_key = self.music_queue[self.current_track_index]
        if track_key in self.music:
            self.music_path = self.music[track_key]
            pygame.mixer.music.load(self.music_path)
            pygame.mixer.music.play()
            print(f"[OST] Reproduciendo '{track_key}'")
            print(f"[DEBUG] Índice actual: {self.current_track_index}")
            self.current_track_index = (self.current_track_index + 1) % len(self.music_queue)
        else:
            print(f"[OST] Track '{track_key}' no encontrado en el diccionario.")

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

    def update_music_queue(self, new_queue):
        """Reemplaza la queue actual con una nueva"""
        self.music_queue = new_queue
        self.current_track_index = 0