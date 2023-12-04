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

        self.actions = {"left": False, "right": False, "up" : False, "down" : False, "Esc" : False, "enter": False, "LEFT_MOUSE_KEY_PRESS":False}


        self.DISPLAY_W, self.DISPLAY_H = 1280, 720


        self.game_canvas = pygame.Surface((self.DISPLAY_W, self.DISPLAY_H))
        self.window = pygame.display.set_mode(((self.DISPLAY_W, self.DISPLAY_H)))



        self.BLACK, self.WHITE, self.YELLOW = (0, 0, 0), (255, 255, 255), (255, 255, 0)

        self.helper = Helper(self)

        self.dt, self.prev_time = 0.0, 0.0



        self.state_stack = []
        self.title_screen = MainMenu(self)
        self.title_screen.enter_state()
   


        self.font_name = "assets/font/f.TTF"



        # self.main_menu = MainMenu(self)
        # self.options = OptionsMenu(self)
        # self.credits = CreditsMenu(self)
        # self.state_stack.append(self.main_menu)

       
        
        # self.music_player = MusicPlayer()
        # self.music_player.load_track("assets\sound\deep-cinematic-ballad_medium-178309.mp3")
        # self.music_player.play()
        
        # self.sprite_sheet = Spritesheet("assets/sprites/trainer_sheet.png")
        # self.sprites = [
        #     {"name": "trainer1.png", "x": self.DISPLAY_W // 4, "y": self.DISPLAY_H // 4, "width": 128, "height": 128, "dynamic": False},
        #     {"name": "trainer2.png", "x": self.DISPLAY_W // 2, "y": self.DISPLAY_H // 2, "width": 128, "height": 128, "dynamic": True},
        #     # Add more sprites as needed
        # ]
        # self.initial_sprite_position = None  # Store the initial position of the dragged sprite
        # self.dragged_sprite = None  # Keep track of the currently dragged sprite
        
        
    def game_loop(self):
        
        while self.running:
            self.get_dt()
            self.update_events()
            self.update()
            self.render()

    
            
            #self.update_sprite_position()###############
            
           ## self.display.fill(self.BLACK)
            ##self.helper.draw_text(self , "hooo", 20, self.DISPLAY_W / 2, self.DISPLAY_H / 2)
          ##  self.window.blit(self.display, (0, 0))

            # Draw all sprites
            # for sprite in self.sprites:
            #     self.window.blit(self.sprite_sheet.parse_sprite(sprite["name"]), (sprite["x"], sprite["y"]))
    def update(self):
        self.state_stack[-1].update(self.dt,self.actions)
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
        self.window.blit(pygame.transform.scale(self.game_canvas,(self.DISPLAY_W ,  self.DISPLAY_H)), (0,0))
        
        pygame.display.flip() #It controls when and how changes made in your code will be visible on the screen



    # def update_sprite_position(self):
    #     if self.KEY_PRESS:
    #         # Check if any sprite is being clicked
    #         for sprite in self.sprites:
    #             sprite_rect = pygame.Rect(
    #                 sprite["x"],
    #                 sprite["y"],
    #                 sprite["width"],
    #                 sprite["height"]
    #             )
    #             if sprite_rect.collidepoint(pygame.mouse.get_pos()):
    #                 self.dragged_sprite = sprite
    #                 self.initial_sprite_position = (sprite["x"], sprite["y"])

    #         # Move the dragged sprite to the mouse position
    #         if self.dragged_sprite and self.dragged_sprite["dynamic"]:
    #             mouse_x, mouse_y = pygame.mouse.get_pos()
    #             self.dragged_sprite["x"], self.dragged_sprite["y"] = mouse_x - self.dragged_sprite["width"] / 2, mouse_y - self.dragged_sprite["height"] / 2
    #     else:
    #         if not self.check_allowed() and self.dragged_sprite:
    #             # Reset the dragged sprite to its initial position
            
    #             self.dragged_sprite["x"], self.dragged_sprite["y"] = self.initial_sprite_position
    #             self.dragged_sprite = None  # Reset dragged sprite

    # def check_allowed(self):
    #     # Implement the conditions under which the dragged sprite is allowed to be placed
    #     pass # Remove this line when you start implementing
    #     return True


    def update_events(self):
        pygame.event.pump()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_a or event.key == pygame.K_LEFT :
                    self.actions['left'] = True
                if event.key == pygame.K_d or event.key == pygame.K_RIGHT:
                    self.actions['right'] = True
                if event.key == pygame.K_w or event.key == pygame.K_UP:
                    self.actions['up'] = True
                if event.key == pygame.K_s or event.key == pygame.K_DOWN:
                    self.actions['down'] = True
                if event.key == pygame.K_ESCAPE:
                    self.actions['Esc'] = True
                if event.key == pygame.K_RETURN:
                    self.actions['enter'] = True
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_a or event.key == pygame.K_LEFT :
                    self.actions['left'] = False
                if event.key == pygame.K_d or event.key == pygame.K_RIGHT:
                    self.actions['right'] = False
                if event.key == pygame.K_w or event.key == pygame.K_UP:
                    self.actions['up'] = False
                if event.key == pygame.K_s or event.key == pygame.K_DOWN:
                    self.actions['down'] = False
                if event.key == pygame.K_ESCAPE:
                    self.actions['Esc'] = False
                if event.key == pygame.K_RETURN:
                    self.actions['enter'] = False
            if event.type == pygame.MOUSEBUTTONUP:
                if not pygame.mouse.get_pressed()[0]:
                   self.actions["LEFT_MOUSE_KEY_PRESS"] = False

            if pygame.mouse.get_pressed()[0]:  # left click
               self.actions["LEFT_MOUSE_KEY_PRESS"] = True