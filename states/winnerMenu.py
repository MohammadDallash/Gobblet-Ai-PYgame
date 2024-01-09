from states.state import State

from util.helpers import MenuGUI
import pygame


class WinnerMenu(State):
    def __init__(self, game, winner):
        State.__init__(self, game)
        self.options_str = ['New Game', 'Main Menu', 'Quit']
        self.winner = winner

        self.cur_option = 0

        self.menuGUI = MenuGUI(self.game, self.options_str, self.cur_option, font_size=30,
                               x_pos=self.game.DISPLAY_W / 2)

    def update(self, delta_time, actions):
        self.cur_option = self.menuGUI.update_cur_opt(actions)
        x, y = pygame.mouse.get_pos()
        for i in range(len(self.options_str)):
            if self.menuGUI.mouse_collidepoint(x, y, i):
                self.menuGUI.cur_option = i
                self.cur_option = i

        if actions['enter']:
            if self.cur_option == 0:
                from states.playing import Playing
                playing_state = Playing(self.game,0)
                playing_state.enter_state()
                pass
            elif self.cur_option == 1:
                self.exit_state()
                self.exit_state()
                pass
            else:
                self.game.running = False

        if actions['Esc']:
            self.exit_state()
            self.exit_state()
            pass

        if actions['LEFT_MOUSE_KEY_PRESS']:
            x, y = pygame.mouse.get_pos()
            if self.menuGUI.mouse_collidepoint(x, y, 0):
                from states.playing import Playing
                playing_state = Playing(self.game,0)
                playing_state.enter_state()
                pass
            if self.menuGUI.mouse_collidepoint(x, y, 1):
                self.exit_state()
                self.exit_state()
                pass
            if self.menuGUI.mouse_collidepoint(x, y, 2):
                self.game.running = False

    def render(self, display):
        display.fill(self.game.BLACK)
        self.helper.draw_text(display, f"PLAYER {self.winner} WINS", self.game.WHITE, 80, self.game.DISPLAY_W / 2, 50)
        self.menuGUI.render(display)

    def enter_state(self):
        super().enter_state()

    def exit_state(self):
        super().exit_state()
