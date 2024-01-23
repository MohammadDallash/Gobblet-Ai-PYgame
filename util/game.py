import pygame
import os, time, pygame

from util.sprite import *
from util.music import *
from states.mainMenu import *
from util.helpers import *


class Game():
    def __init__(self):
        pygame.init()

        self.running = True
        self.actions = {"left": False, "right": False, "up": False, "down": False, "Esc": False, "enter": False,
                        "LEFT_MOUSE_KEY_PRESS": False, 'backspace': False,"quit": False , "k_v": False}

        self.DISPLAY_W, self.DISPLAY_H = 1200, 720
    

        self.game_canvas = pygame.Surface((self.DISPLAY_W, self.DISPLAY_H))
        self.window = pygame.display.set_mode(((self.DISPLAY_W, self.DISPLAY_H)))

        self.BLUE, self.WHITE, self.YELLOW, self.BROWN, self.RED, self.GREY = (0, 0, 0), (255, 255, 255), (255, 255, 0), (46, 32, 26), (255, 0 ,0), (128,128,128)

        self.helper = Helper(self)

        self.dt, self.prev_time = 0.0, 0.0
        self.ai_difficulty = 3
        self.state_stack = []
        self.global_text_font_size = 40
        self.global_options_text_size = 25
        self.global_title_font_size = 50
        self.global_font_color = self.WHITE
        
        self.global_volume = 0.3
        self.title_screen = MainMenu(self)
        self.title_screen.enter_state()
        pygame.display.set_caption('Space Gobblet')

        if getattr(sys, 'frozen', False):
            # Running as compiled executable
            base_path = sys._MEIPASS
        else:
            # Running as a script
            base_path = os.path.abspath(".")

        assets_path = os.path.join(base_path, "assets")

        self.icon = pygame.image.load(rf"{assets_path}/sprites/tiles/tileswhite2.png")
        pygame.display.set_icon(self.icon)
        self.text_font_name = rf"{assets_path}/font/f.TTF"
        self.title_font_name = rf"{assets_path}/font/f.TTF"
        
        # menus background
        self.menubg = pygame.image.load(rf"{assets_path}/background/background(space).png")
        
        # background music
        self.global_music_player = MusicPlayer(self.global_volume)
        self.music_track = rf'{assets_path}/sound/background music.mp3'
        
        self.global_music_player.load_track(self.music_track)
        self.global_music_player.play()

        self.keys = []

        self.client_socket =   None


    def game_loop(self):

        while self.running:
            self.get_dt()
            self.update_events()
            self.update()
            self.render()
        
        self.close_connection()
    def is_socket_closed(self, sock):
        try:
            # Check if the socket is closed by attempting to get the socket option
            sock.getsockopt(socket.SOL_SOCKET, socket.SO_ERROR)
            return False  # The socket is still open
        except OSError as os_error:
            # Handle the specific OSError indicating the socket is closed
            if os_error.errno == 10038:  # WinError 10038
                return True  # The socket is closed
            else:
                raise  # Reraise the exception if it's not the expected OSError
        except Exception as e:
            # Check if the exception indicates the socket is closed
            if isinstance(e, (socket.error, BrokenPipeError, ConnectionResetError)):
                return True  # The socket is closed
            else:
                raise  # Reraise the exception if it's not a known error

    def close_connection(self):
        if(self.client_socket != None):
            if not self.is_socket_closed(self.client_socket):
                msg = 'byebye'
                try:
                    self.client_socket.send(msg.encode())
                except Exception as e:
                    pass
            try:
                self.client_socket.close()
            except Exception as e:
                pass

    def update(self):
        self.state_stack[-1].update(self.dt, self.actions)
        self.reset_keys()

    def get_dt(self):
        now = time.time()
        self.dt = now - self.prev_time
        self.prev_time = now

    def reset_keys(self):
        for action in self.actions:
            self.actions[action] = False

    def render(self):

        self.state_stack[-1].render(self.game_canvas)
        self.window.blit(pygame.transform.scale(self.game_canvas, (self.DISPLAY_W, self.DISPLAY_H)), (0, 0))

        pygame.display.flip()  # It controls when and how changes made in your code will be visible on the screen
    def update_events(self):
        self.keys = []
        self.actions["LEFT_MOUSE_KEY_PRESS"] = False

        #pygame.event.pump()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.actions['quit'] = True
                self.running = False

            elif event.type == pygame.KEYDOWN:
                self.handle_keydown(event)

            elif event.type == pygame.KEYUP:
                self.handle_keyup(event)

            elif event.type == pygame.MOUSEBUTTONUP:
                self.handle_mouse_button_up(event)

        if pygame.mouse.get_pressed()[0]:  # left click
            self.actions["LEFT_MOUSE_KEY_PRESS"] = True
            time.sleep(0.12)

    def handle_keydown(self, event):
        if event.key in (pygame.K_a, pygame.K_LEFT):
            self.actions['left'] = True
        elif event.key in (pygame.K_d, pygame.K_RIGHT):
            self.actions['right'] = True
        elif event.key in (pygame.K_w, pygame.K_UP):
            self.actions['up'] = True
        elif event.key in (pygame.K_s, pygame.K_DOWN):
            self.actions['down'] = True
        elif event.key == pygame.K_ESCAPE:
            self.actions['Esc'] = True
        elif event.key == pygame.K_RETURN:
            self.actions['enter'] = True
        elif event.key == pygame.K_BACKSPACE:
            self.actions['backspace'] = True
        elif event.key == pygame.K_v and event.mod & pygame.KMOD_CTRL:
            self.actions['k_v'] = True
        
        char = event.unicode
        if char:
            self.handle_char_input(char, event.mod)

    def handle_keyup(self, event):
        if event.key in (pygame.K_a, pygame.K_LEFT):
            self.actions['left'] = False
        elif event.key in (pygame.K_d, pygame.K_RIGHT):
            self.actions['right'] = False
        elif event.key in (pygame.K_w, pygame.K_UP):
            self.actions['up'] = False
        elif event.key in (pygame.K_s, pygame.K_DOWN):
            self.actions['down'] = False
        elif event.key == pygame.K_ESCAPE:
            self.actions['Esc'] = False
        elif event.key == pygame.K_RETURN:
            self.actions['enter'] = False
        elif event.key == pygame.K_BACKSPACE:
            self.actions['backspace'] = False
        elif event.key == pygame.K_v and event.mod & pygame.KMOD_CTRL:
            self.actions['k_v'] = False
        
        

    def handle_char_input(self, char, mod):
        if char.isalpha():
            self.handle_alpha_input(char, mod)
        elif char.isdigit():
            self.keys.append(char)
        # elif char in (pygame.K_SPACE, pygame.K_EXCLAIM, pygame.K_QUOTEDBL, ..., pygame.K_SLASH) and char not in self.keys:
        #     self.keys.append(char)


    def handle_alpha_input(self, char, mod):
        if not mod & pygame.KMOD_SHIFT:
            self.keys = [item for item in self.keys if item != char.lower()]
            self.keys.append(char.lower())
        else:
            self.keys = [item for item in self.keys if item != char.upper()]
            self.keys.append(char.upper())

    def handle_mouse_button_up(self, event):
        if not pygame.mouse.get_pressed()[0]:
            self.actions["LEFT_MOUSE_KEY_PRESS"] = False