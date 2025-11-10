import pygame
import mido

GENERATED_FILE_NAME="output.mid"

class SoundManager():
    def __init__(self):
        self._initialized = False
        self._is_playing = False
        self._is_paused = False
        
        try:
            pygame.init()
            pygame.mixer.init()
            self._initialized = True
        except pygame.error as e:
            print(f"Erro ao inicializar o SoundManager: {e}")
            print("A funcionalidade de áudio pode não funcionar.")
            
    def play_music(self, e):
        if not self._initialized:
            print("SoundManager não foi inicializado. Não é possível tocar música.")
            return

        try:
            pygame.mixer.music.load(GENERATED_FILE_NAME)
            pygame.mixer.music.play()
            self._is_playing = True
            self._is_paused = False
        except pygame.error as e:
            print(f"Erro ao carregar ou tocar o arquivo '{GENERATED_FILE_NAME}': {e}")
            self._is_playing = False
            
    def pause_music(self, e):
        """Pausa ou retoma a música."""
        if not self._initialized or not self._is_playing:
            # Não faz nada se a música não estiver tocando
            return

        if self._is_paused:
            # Se já está pausado, retoma (unpause)
            pygame.mixer.music.unpause()
            self._is_paused = False
        else:
            # Se está tocando, pausa
            pygame.mixer.music.pause()
            self._is_paused = True

    def reset_music(self, e):
        """Para a música e rebobina para o início."""
        if not self._initialized:
            return
        
        pygame.mixer.music.stop()
        pygame.mixer.music.rewind()
        self._is_playing = False
        self._is_paused = False