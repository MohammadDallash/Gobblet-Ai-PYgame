import time
import pygame

class MusicPlayer:
    def __init__(self):
        pygame.mixer.init()
        self.current_track = None
        self.background_sound = pygame.mixer.Sound('assets/sound/background music.mp3')
        self.sfx = pygame.mixer.Sound('assets/sound/move_piece.mp3')
        self.win_sound = pygame.mixer.Sound('assets/sound/win sound.mp3')
        self.master_volume = 1.0

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
        self.master_volume = volume
        # Set the volume of the music (0.0 to 1.0)
        self.background_sound.set_volume(self.master_volume)
        
    def check_music(self):
        if(self.master_volume==0 or pygame.mixer.Channel(0).get_busy() == False):
            return False
        else:
            return True
    
    def play_sfx(self):
        self.sfx.set_volume(self.master_volume)
        pygame.mixer.Channel(1).play(self.sfx)

    def play_win_sound(self):
        self.win_sound.set_volume(self.master_volume)
        pygame.mixer.Channel(0).play(self.win_sound,loops=-1)
        
    def play_background_sound(self):
        self.background_sound.set_volume(self.master_volume)
        pygame.mixer.Channel(0).play(self.background_sound,loops=-1)
        

