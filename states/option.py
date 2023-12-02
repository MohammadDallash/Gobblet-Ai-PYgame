
from states.state import State

from util.helpers import MenuGUI
import pygame


class Option(State):
    def __init__(self, game):
        State.__init__(self, game)
        self.options_str = ['Volume', 'Player_Mode', 'Music_On', 'Difficulty', 'Resolution']
        self.Volume_options = ['Higher', 'Lower', 'Mute']
        self.Player_mode_options = ['Player to Player', 'Player to Computer', 'Computer to Computer']
        self.Music_on_options = ['On', 'Off']
        self.Difficulty_options = ['Easy', 'Hard']
        self.Resolution_options = ['900x700', '1200x400', '1200x800']
        self.volume='Higher'
        self.PlayerMode='Player to Player'
        self.Music='On'
        self.Difficulty='Easy'
        self.Resolution='900x700'

        self.cur_option = 0
        self.menuGUI = MenuGUI(self.game, self.options_str, self.cur_option, font_size=30, x_pos=self.game.DISPLAY_W / 2,
                                justTxt=False)

    def update(self, delta_time, actions):
        self.cur_option = self.menuGUI.update_cur_opt(actions)
        if actions['Esc']:
            self.exit_state()

        if actions['enter'] :
            if self.cur_option == 0:
                option_state=Option_select(self.game,self.Volume_options,'Volume_options',self)
                option_state.enter_state()               
            elif self.cur_option == 1:
                option_state=Option_select(self.game,self.Player_mode_options,"Player_mode_options",self)
                option_state.enter_state()          
            elif self.cur_option == 2:
                option_state=Option_select(self.game,self.Music_on_options,"Music_on_options",self)
                option_state.enter_state()          

            elif self.cur_option == 3:
                option_state=Option_select(self.game,self.Difficulty_options,"Difficulty_options",self)
                option_state.enter_state()          
            elif self.cur_option == 4:
                option_state=Option_select(self.game,self.Resolution_options,"Resolution_options",self)
                option_state.enter_state()  
        if(actions['LEFT_MOUSE_KEY_PRESS']):
            x,y=pygame.mouse.get_pos()
            if self.menuGUI.mouse_collidepoint(x,y,0):
                option_state=Option_select(self.game,self.Volume_options,'Volume_options',self)
                option_state.enter_state()     
            if self.menuGUI.mouse_collidepoint(x,y,1):
                option_state=Option_select(self.game,self.Player_mode_options,"Player_mode_options",self)
                option_state.enter_state()          
            if self.menuGUI.mouse_collidepoint(x,y,2):
                option_state=Option_select(self.game,self.Music_on_options,"Music_on_options",self)
                option_state.enter_state()     
            if self.menuGUI.mouse_collidepoint(x,y,3):
                option_state=Option_select(self.game,self.Difficulty_options,"Difficulty_options",self)
                option_state.enter_state() 
            if self.menuGUI.mouse_collidepoint(x,y,4):
                option_state=Option_select(self.game,self.Resolution_options,"Resolution_options",self)
                option_state.enter_state()  



    def render(self, display):
        display.fill(self.game.BLACK)
        self.helper.draw_text(display, 'Option', self.game.WHITE, 80, self.game.DISPLAY_W / 2, 50)
        self.menuGUI.render(display)
    def enter_state(self):
        super().enter_state()

    def exit_state(self):
        super().exit_state()
    def set_music(self,val):
        self.Music=val
    def set_volume(self,val):
        self.volume=val
    def set_PlayerMode(self,val):
        self.PlayerMode=val
    def set_Difficulty(self,val):
        self.Difficulty=val
    def set_Resolutiony(self,val):
        self.Resolution=val
        x_str, y_str = self.Resolution.split('x')
        x = int(x_str)
        y = int(y_str)
        self.game.window_resulotion(x,y)

class Option_select(State):
    def __init__(self, game, option, T, op):
        State.__init__(self, game)

        self.options_str = option
        self.option_object = op
        self.type = T  # Correct the assignment here

        self.cur_option = self.get_choose()

        self.menuGUI = MenuGUI(self.game, self.options_str, self.cur_option, font_size=20,
                               x_pos=self.game.DISPLAY_W / 2 + 500, justTxt=False)

    def get_choose(self):
        if self.type == 'Volume_options':  # Correct the usage here
            return self.options_str.index(self.option_object.volume)
        elif self.type == 'Player_mode_options':
            return self.options_str.index(self.option_object.PlayerMode)
        elif self.type == 'Music_on_options':
            return self.options_str.index(self.option_object.Music)
        elif self.type == 'Difficulty_options':
            return self.options_str.index(self.option_object.Difficulty)
        elif self.type == 'Resolution_options':
            return self.options_str.index(self.option_object.Resolution)
    def set_choose(self):
        if self.type == 'Volume_options':
            self.option_object.set_volume(self.options_str[self.cur_option])
        elif self.type == 'Player_mode_options':
            self.option_object.set_PlayerMode(self.options_str[self.cur_option])
        elif self.type == 'Music_on_options':
            self.option_object.set_music(self.options_str[self.cur_option])
        elif self.type == 'Difficulty_options':
           self.option_object.set_Difficulty(self.options_str[self.cur_option])
        elif self.type == 'Resolution_options':
            self.option_object.set_Resolutiony(self.options_str[self.cur_option])
        
    def update(self, delta_time, actions):
        self.cur_option = self.menuGUI.update_cur_opt(actions)
        if(actions['Esc']):
           self.exit_state()
        if(actions['enter']):
            self.set_choose()
            self.exit_state()
        if(actions['LEFT_MOUSE_KEY_PRESS']):
            x,y=pygame.mouse.get_pos()
            if self.menuGUI.mouse_collidepoint(x,y,0):
                self.option_object.set_volume(self.options_str[0])
                self.exit_state()
            elif self.menuGUI.mouse_collidepoint(x,y,1):
                self.option_object.set_volume(self.options_str[1])
                self.exit_state()

            elif self.menuGUI.mouse_collidepoint(x,y,2) :
                self.option_object.set_volume(self.options_str[2])
                self.exit_state()

   


    def render(self,display):
        self.menuGUI.render(display)



    def enter_state(self):
        super().enter_state()
        
    def exit_state(self):
        super().exit_state()