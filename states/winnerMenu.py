from states.state import State
import time
from util.helpers import MenuGUI
import pygame

BLUE, RED = 0, 1

class WinnerMenu(State):
    def __init__(self, game, winner, play_mode, my_color , opponent_type_in_other_mode  ):
        State.__init__(self, game)
        self.options_str = ['New Game', 'Main Menu', 'Quit']
        self.winner = winner
        self.play_mode = play_mode
        self.cur_option = 0
        self.menuGUI = MenuGUI(self.game, self.options_str, self.cur_option, font_size=game.global_text_font_size,
                               x_pos=self.game.DISPLAY_W / 2)
        self.my_color  =my_color
        self.opponent_type_in_other_mode = opponent_type_in_other_mode
    def update(self, delta_time, actions):
        self.cur_option = self.menuGUI.update_cur_opt(actions)
        x, y = pygame.mouse.get_pos()
        for i in range(len(self.options_str)):
            if self.menuGUI.mouse_collidepoint(x, y, i):
                self.menuGUI.cur_option = i
                self.cur_option = i

        if actions['enter']:
            if self.cur_option == 0:
                self.exit_state()
                self.exit_state()
                from states.playing import Playing
                playing_state = Playing(self.game,self.play_mode, self.my_color, self.opponent_type_in_other_mode)
                playing_state.enter_state()
                pass
            elif self.cur_option == 1:
                for i in range (len (self.game.state_stack) -1 ): ##exit all the state except the menu one
                    self.exit_state()
                self.game.close_connection()
                pass
            else:
                self.game.running = False

        if actions['Esc']:
            self.exit_state()
            self.exit_state()
            self.exit_state()
            pass

        if actions['LEFT_MOUSE_KEY_PRESS']:
            x, y = pygame.mouse.get_pos()
            if self.menuGUI.mouse_collidepoint(x, y, 0):
                self.exit_state()
                self.exit_state()
                from states.playing import Playing
                playing_state = Playing(self.game,self.play_mode, self.my_color, self.opponent_type_in_other_mode)
            
                playing_state.enter_state()
                pass
            if self.menuGUI.mouse_collidepoint(x, y, 1):
                for i in range (len (self.game.state_stack) -1 ): ##exit all the state except the menu one
                    self.exit_state()
                self.game.close_connection()
                pass
            if self.menuGUI.mouse_collidepoint(x, y, 2):
                self.game.running = False

    def render(self, display):
        display.blit(self.game.menubg, (0, 0))
        self.helper.draw_text(display, f"PLAYER {self.winner} WINS", self.game.global_font_color, 80, self.game.DISPLAY_W / 2, 50,True)
        self.menuGUI.render(display)

    def enter_state(self):
        super().enter_state()

    def exit_state(self):
        super().exit_state()
