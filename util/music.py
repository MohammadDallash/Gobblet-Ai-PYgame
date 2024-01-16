import pygame

class MusicPlayer:
    def __init__(self):
        pygame.mixer.init()
        self.current_track = None
        self.background_sound = None
        self.sfx = pygame.mixer.Sound('assets/sound/move_piece.mp3')
        self.volume = 1.0

    def load_track(self, track_path):
        pygame.mixer.music.load(track_path)
        self.current_track = track_path
        self.background_sound = pygame.mixer.Sound(self.current_track)


    def play(self, loop=-1):
        pygame.mixer.Channel(0).play(self.background_sound,loops=-1)

    def pause(self):
        pygame.mixer.pause()

    def unpause(self):
        pygame.mixer.unpause()

    def stop(self):
        pygame.mixer.stop()

    def set_volume(self, volume):
        self.volume = volume
        # Set the volume of the music (0.0 to 1.0)
        self.background_sound.set_volume(self.volume)
        
    def check_music(self):
        return pygame.mixer.music.get_busy()
    
    def play_sfx(self):
        self.sfx.set_volume(self.volume)
        pygame.mixer.Channel(1).play(self.sfx)
