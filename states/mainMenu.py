from states.MultiplayerUI import *
from states.state import State
from states.credit import Credit
from states.playing import Playing
from util.helpers import MenuGUI
import pygame
from states.option import Option
from util.music import MusicPlayer


AI_OPPONENT_IN_OTHER= 0
ONLINE_OPPONENT_IN_OTHER= 1


class MainMenu(State):
    def __init__(self, game):
        State.__init__(self, game)

        self.options_str = ['Play', 'options', 'credit', 'quit']
        self.Player_Mode = ['Player vs Player', 'Player vs Computer', 'Computer vs Computer', 'multiplayer']

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

        if (actions['enter']):
            if (self.cur_option == 0):
                mode = Play_Mode(self.game, self.Player_Mode)
                mode.enter_state()
                # playing_state = Playing(self.game,0)
                ##self.exit_state()## if we want to exit the tile state we woul un comment this but we want to keep them as we want to retrun back to them
                # playing_state.enter_state()  ## enter play state
            elif (self.cur_option == 1):
                option_state = Option(self.game)
                option_state.enter_state()
            elif (self.cur_option == 2):
                credit_state = Credit(self.game)
                ##self.exit_state()## if we want to exit the tile state we woul un comment this but we want to keep them as we want to retrun back to them
                credit_state.enter_state()

                ## enter credit state
                pass
            else:
                self.game.running = False

        if (actions['Esc']):
            self.game.running = False
        if (actions['LEFT_MOUSE_KEY_PRESS']):
            x, y = pygame.mouse.get_pos()
            if self.menuGUI.mouse_collidepoint(x, y, 0):
                mode = Play_Mode(self.game, self.Player_Mode)
                mode.enter_state()
                # playing_state = Playing(self.game,0)
                # ##self.exit_state()## if we want to exit the tile state we woul un comment this but we want to keep them as we want to retrun back to them
                # playing_state.enter_state()  ## enter play state
            if self.menuGUI.mouse_collidepoint(x, y, 1):
                option_state = Option(self.game)
                option_state.enter_state()
            if self.menuGUI.mouse_collidepoint(x, y, 2):
                credit_state = Credit(self.game)
                ##self.exit_state()## if we want to exit the tile state we woul un comment this but we want to keep them as we want to retrun back to them
                credit_state.enter_state()
            if self.menuGUI.mouse_collidepoint(x, y, 3):
                self.game.running = False

    def render(self, display):
        # display.fill(self.game.BLUE)
        display.blit(self.game.menubg, (0, 0))
        self.helper.draw_text(display, 'Space Gobblers', self.game.WHITE, 80, self.game.DISPLAY_W / 2, self.game.global_title_font_size)
        self.menuGUI.render(display)

    def enter_state(self):
        super().enter_state()

    def exit_state(self):
        super().exit_state()

        
class Play_Mode(State):
    def __init__(self, game, option):
        State.__init__(self, game)

        self.options_str = option

        self.cur_option = 0

        self.menuGUI = MenuGUI(self.game, self.options_str, self.cur_option, font_size=game.global_text_font_size,
                               x_pos=self.game.DISPLAY_W / 2 + 400, justTxt=False)



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
            if(self.cur_option  == 3):
                multiplayerMenu = MultiplayerChooseMenu(self.game) ##multi
                multiplayerMenu.enter_state()
            elif(self.cur_option  == 1): #player vs computer
                playing_state = Playing(self.game, self.cur_option, opponent_type_in_other_mode=AI_OPPONENT_IN_OTHER)
                playing_state.enter_state()
            else:
                playing_state = Playing(self.game, self.cur_option)
                playing_state.enter_state()  ## enter play state
        if (actions['LEFT_MOUSE_KEY_PRESS']):
            x, y = pygame.mouse.get_pos()
            if self.menuGUI.mouse_collidepoint(x, y, self.cur_option):
                if(self.cur_option  == 3):
                    multiplayerMenu = MultiplayerChooseMenu(self.game)
                    multiplayerMenu.enter_state()
                elif(self.cur_option  == 1): #TODO
                    playing_state = Playing(self.game, self.cur_option, opponent_type_in_other_mode=AI_OPPONENT_IN_OTHER)
                    playing_state.enter_state()
           
                else:
                    playing_state = Playing(self.game, self.cur_option)
                    playing_state.enter_state()
                

    def render(self, display):
        self.menuGUI.render(display)

    def enter_state(self):
        super().enter_state()

    def exit_state(self):
        super().exit_state()



"""
input :[] list of functions
input :[] list of strings 

"""
