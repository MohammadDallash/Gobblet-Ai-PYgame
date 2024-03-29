from states.state import State

from util.helpers import MenuGUI
from util.game import MusicPlayer
import pygame


class Option(State):
    def __init__(self, game):
        State.__init__(self, game)
        self.Music = 'On'
        self.options_str = ['Volume', 'Music', 'Difficulty']
        self.Volume = ['Higher', 'Lower', 'Mute']
        self.Music_on_options = ['On', 'Off']
        self.Difficulty_options = ['Easy', 'Hard']
        self.volume = 'Higher'
        self.Difficulty = 'Hard'
        self.cur_option = 0
        self.menuGUI = MenuGUI(self.game, self.options_str, self.cur_option, font_size=game.global_text_font_size,
                               x_pos=self.game.DISPLAY_W / 2,
                               justTxt=False)

    def update(self, delta_time, actions):
        options = [self.Volume, self.Music_on_options,
                   self.Difficulty_options]

        self.cur_option = self.menuGUI.update_cur_opt(actions)
        if actions['Esc']:
            self.exit_state()

        if actions['enter']:
            option_state = Option_select(self.game, options[self.cur_option], self.options_str[self.cur_option], self)
            option_state.enter_state()

        x, y = pygame.mouse.get_pos()
        for i in range(len(self.options_str)):
            if self.menuGUI.mouse_collidepoint(x, y, i):
                self.menuGUI.cur_option = i
                if actions['LEFT_MOUSE_KEY_PRESS']:
                    option_state = Option_select(self.game, options[i], self.options_str[i], self)
                    option_state.enter_state()

    def render(self, display):
        display.blit(self.game.menubg, (0, 0))
        self.helper.draw_text(display, 'Options', self.game.global_font_color, 80, self.game.DISPLAY_W / 2, 50,True)
        self.menuGUI.render(display)

    def enter_state(self):
        super().enter_state()

    def exit_state(self):
        super().exit_state()

    def set_music(self, val):
        self.Music = val
        if val == 'Off':
            self.game.global_music_player.pause()
        elif val == "On":
            self.game.global_music_player.unpause()
            

    def set_volume(self, val):
        self.volume = val
        if val == 'Higher':
            self.game.global_music_player.set_volume(0.4)
        elif val=='Lower':
            self.game.global_music_player.set_volume(0.1)
        else:
            self.game.global_music_player.set_volume(0.0)

    def set_PlayerMode(self, val):
        self.PlayerMode = val


    def set_Difficulty(self, val):
        self.Difficulty = val
        if val == 'Easy':
            self.game.ai_difficulty = 1
        else:
            self.game.ai_difficulty = 3


class Option_select(State):
    def __init__(self, game, option, T, op):
        State.__init__(self, game)

        self.options_str = option
        self.option_object = op
        self.type = T  # Correct the assignment here

        self.cur_option = self.get_choose()

        self.menuGUI = MenuGUI(self.game, self.options_str, self.cur_option, font_size=game.global_options_text_size,
                               x_pos=self.game.DISPLAY_W / 2 + 300, justTxt=False)

    def get_choose(self):
        if self.type == 'Volume':  # Correct the usage here
            return self.options_str.index(self.option_object.volume)
        elif self.type == 'Music':
            return self.options_str.index(self.option_object.Music)
        elif self.type == 'Difficulty':
            return self.options_str.index(self.option_object.Difficulty)

    def set_choose(self):
        if self.type == 'Volume':
            self.option_object.set_volume(self.options_str[self.cur_option])
        elif self.type == 'Music':
            self.option_object.set_music(self.options_str[self.cur_option])
        elif self.type == 'Difficulty':
            self.option_object.set_Difficulty(self.options_str[self.cur_option])

    def set_choose_with_value(self, value):
        if self.type == 'Volume':
            self.option_object.set_volume(value)
        elif self.type == 'Music':
            self.option_object.set_music(value)
        elif self.type == 'Difficulty':
            self.option_object.set_Difficulty(value)

    def update(self, delta_time, actions):
        self.cur_option = self.menuGUI.update_cur_opt(actions)
        x, y = pygame.mouse.get_pos()
        for i in range(len(self.options_str)):
            if self.menuGUI.mouse_collidepoint(x, y, i):
                self.menuGUI.cur_option = i
                self.cur_option = i

        if (actions['Esc']):
            self.exit_state()
        if (actions['enter']):
            self.set_choose()
            self.exit_state()
        if (actions['LEFT_MOUSE_KEY_PRESS']):
            x, y = pygame.mouse.get_pos()
            if self.menuGUI.mouse_collidepoint(x, y, 0):
                self.set_choose_with_value(self.options_str[0])
                self.exit_state()
            elif self.menuGUI.mouse_collidepoint(x, y, 1):
                self.set_choose_with_value(self.options_str[1])
                self.exit_state()
            if self.type == 'Volume':
                if self.menuGUI.mouse_collidepoint(x, y, 2):
                    self.set_choose_with_value(self.options_str[2])
                    self.exit_state()

    def render(self, display):
        self.menuGUI.render(display)

    def enter_state(self):
        super().enter_state()

    def exit_state(self):
        super().exit_state()
