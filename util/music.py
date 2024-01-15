import pygame


class MusicPlayer:
    def __init__(self):
        pygame.mixer.init()
        self.current_track = None

    def load_track(self, track_path):

        pygame.mixer.music.load(track_path)
        self.current_track = track_path

    def play(self, loop=-1):
        pygame.mixer.Channel(0).play(pygame.mixer.Sound(self.current_track),loops=-1)

    def pause(self):
        pygame.mixer.music.pause()

    def unpause(self):
        pygame.mixer.music.unpause()

    def stop(self):
        pygame.mixer.Channel(0).stop()

    def set_volume(self, volume):
        # Set the volume of the music (0.0 to 1.0)
        pygame.mixer.music.set_volume(volume)
        
    def check_music(self):
        return pygame.mixer.music.get_busy()
    
    def play_sfx(self,sfx_path):
        pygame.mixer.Channel(1).play(pygame.mixer.Sound(sfx_path))
