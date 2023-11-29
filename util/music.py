import pygame
class MusicPlayer:
    def __init__(self):
        pygame.mixer.init()
        self.current_track = None

    def load_track(self, track_path):
        # Load a music track
        pygame.mixer.music.load(track_path)
        self.current_track = track_path

    def play(self, loop=-1):
        # Start playing the loaded track
        pygame.mixer.music.play(loop)

    def pause(self):
        # Pause the currently playing track
        pygame.mixer.music.pause()

    def unpause(self):
        # Unpause the currently paused track
        pygame.mixer.music.unpause()

    def stop(self):
        # Stop the currently playing track
        pygame.mixer.music.stop()

    def set_volume(self, volume):
        # Set the volume of the music (0.0 to 1.0)
        pygame.mixer.music.set_volume(volume)
