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
                        "LEFT_MOUSE_KEY_PRESS": False}

        self.DISPLAY_W, self.DISPLAY_H = 1200, 720
    

        self.game_canvas = pygame.Surface((self.DISPLAY_W, self.DISPLAY_H))
        self.window = pygame.display.set_mode(((self.DISPLAY_W, self.DISPLAY_H)))

        self.BLUE, self.RED, self.YELLOW, self.BROWN = (0, 0, 0), (255, 255, 255), (255, 255, 0), (130, 77, 47)

        self.helper = Helper(self)

        self.dt, self.prev_time = 0.0, 0.0

        self.state_stack = []
        self.title_screen = MainMenu(self)
        self.title_screen.enter_state()
        pygame.display.set_caption('Space Gobblet')
        self.icon = pygame.image.load("assets/sprites/tiles/tileswhite2.png")
        pygame.display.set_icon(self.icon)
        self.font_name = "assets/font/f.TTF"
        
        # menus background
        self.menubg = pygame.image.load("assets/background/background(space).png")
        
        # background music
        self.music_player = MusicPlayer()
        self.music_track = 'assets/sound/background music.mp3'
        self.music_player.load_track(self.music_track)
        self.music_player.play()

    def game_loop(self):

        while self.running:
            self.get_dt()
            self.update_events()
            self.update()
            self.render()

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
        pygame.event.pump()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_a or event.key == pygame.K_LEFT:
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
                if event.key == pygame.K_a or event.key == pygame.K_LEFT:
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
