import pygame
from menu import *
from sprite import Spritesheet
from music import MusicPlayer
class Game():
    def __init__(self):
        pygame.init()

        self.running, self.playing = True, False
        self.UP_KEY, self.DOWN_KEY, self.START_KEY, self.BACK_KEY = False, False, False, False
        self.DISPLAY_W, self.DISPLAY_H = 500, 300
        self.display = pygame.Surface((self.DISPLAY_W, self.DISPLAY_H))
        self.window = pygame.display.set_mode(((self.DISPLAY_W, self.DISPLAY_H)))
        self.font_name = "8-BIT WONDER.TTF"
        self.BLACK, self.WHITE = (0, 0, 0), (255, 255, 255)
        self.main_menu = MainMenu(self)
        self.options = OptionsMenu(self)
        self.credits = CreditsMenu(self)
        self.curr_menu = self.main_menu
        self.KEY_PRESS = False
        self.music_player = MusicPlayer()
        self.music_player.load_track("deep-cinematic-ballad_medium-178309.mp3")
        self.music_player.play()
        self.sprite_sheet = Spritesheet("trainer_sheet.png")
        self.sprites = [
            {"name": "trainer1.png", "x": self.DISPLAY_W // 4, "y": self.DISPLAY_H // 4, "width": 128, "height": 128, "dynamic": False},
            {"name": "trainer2.png", "x": self.DISPLAY_W // 2, "y": self.DISPLAY_H // 2, "width": 128, "height": 128, "dynamic": True},
            # Add more sprites as needed
        ]
        self.initial_sprite_position = None  # Store the initial position of the dragged sprite
        self.dragged_sprite = None  # Keep track of the currently dragged sprite
        

    def game_loop(self):
        
        while self.playing:
            pygame.event.pump()
            self.check_events()
            if self.START_KEY:
                self.playing = False
            self.update_sprite_position()
            self.display.fill(self.BLACK)
            self.draw_text("hooo", 20, self.DISPLAY_W / 2, self.DISPLAY_H / 2)
            self.window.blit(self.display, (0, 0))

            # Draw all sprites
            for sprite in self.sprites:
                self.window.blit(self.sprite_sheet.parse_sprite(sprite["name"]), (sprite["x"], sprite["y"]))

            pygame.display.update()
            self.reset_keys()

    def update_sprite_position(self):
        if self.KEY_PRESS:
            # Check if any sprite is being clicked
            for sprite in self.sprites:
                sprite_rect = pygame.Rect(
                    sprite["x"],
                    sprite["y"],
                    sprite["width"],
                    sprite["height"]
                )
                if sprite_rect.collidepoint(pygame.mouse.get_pos()):
                    self.dragged_sprite = sprite
                    self.initial_sprite_position = (sprite["x"], sprite["y"])

            # Move the dragged sprite to the mouse position
            if self.dragged_sprite and self.dragged_sprite["dynamic"]:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                self.dragged_sprite["x"], self.dragged_sprite["y"] = mouse_x - self.dragged_sprite["width"] / 2, mouse_y - self.dragged_sprite["height"] / 2
        else:
            if not self.check_allowed() and self.dragged_sprite:
                # Reset the dragged sprite to its initial position
            
                self.dragged_sprite["x"], self.dragged_sprite["y"] = self.initial_sprite_position
                self.dragged_sprite = None  # Reset dragged sprite

    def check_allowed(self):
        # Implement the conditions under which the dragged sprite is allowed to be placed
        pass # Remove this line when you start implementing
        return True


    def check_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running, self.playing = False, False
                self.curr_menu.run_display = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    self.START_KEY = True
                if event.key == pygame.K_BACKSPACE:
                    self.BACK_KEY = True
                if event.key == pygame.K_DOWN:
                    self.DOWN_KEY = True
                if event.key == pygame.K_UP:
                    self.UP_KEY = True
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_RETURN:
                    self.START_KEY = False
                if event.key == pygame.K_BACKSPACE:
                    self.BACK_KEY = False
                if event.key == pygame.K_DOWN:
                    self.DOWN_KEY = False
                if event.key == pygame.K_UP:
                    self.UP_KEY = False
            if event.type == pygame.MOUSEBUTTONUP:
                if not pygame.mouse.get_pressed()[0]:
                    self.KEY_PRESS = False

            if pygame.mouse.get_pressed()[0]:  # left click
                self.KEY_PRESS = True

    def reset_keys(self):
        self.UP_KEY, self.DOWN_KEY, self.START_KEY, self.BACK_KEY, self.KEY_PRESS = False, False, False, False, False


    def draw_text(self, text, size, x, y):
        font = pygame.font.Font(self.font_name, size)
        text_surface = font.render(text, True, self.WHITE)
        text_rect = text_surface.get_rect()
        text_rect.center = (x, y)
        self.display.blit(text_surface, text_rect)
        return text_rect
    def window_resulotion(self, width, height):
        self.DISPLAY_W, self.DISPLAY_H = width, height
        self.display = pygame.Surface((self.DISPLAY_W, self.DISPLAY_H))
        self.window = pygame.display.set_mode(((self.DISPLAY_W, self.DISPLAY_H)))