from states.state import State
import socket
from util.helpers import MenuGUI
import pygame
from util.MultiplayerHelper import MultiplayerHelper


class MultiplayerChoseMenu(State):
    def __init__(self, game):
        State.__init__(self, game)

        self.options_str = ['host', 'clint']

        self.cur_option = 0
        self.menuGUI = MenuGUI(self.game, self.options_str, self.cur_option, font_size=40,
                               x_pos=self.game.DISPLAY_W / 2)

    def update(self, delta_time, actions):
        self.cur_option = self.menuGUI.update_cur_opt(actions)

        if actions['enter']:
            if(self.cur_option == 1):
                multiplayerMenu_state =  MultiplayeClinetMenu(self.game)
            else :
                multiplayerMenu_state =  MultiplayerHostMenu(self.game)
            multiplayerMenu_state.enter_state()

        x, y = pygame.mouse.get_pos()
        for i in range(len(self.options_str)):
            if self.menuGUI.mouse_collidepoint(x, y, i):
                self.menuGUI.cur_option = i
                if actions['LEFT_MOUSE_KEY_PRESS']:
                    if(self.cur_option == 1):
                        multiplayerMenu_state =  MultiplayeClinetMenu(self.game)
                    else :
                        multiplayerMenu_state =  MultiplayerHostMenu(self.game)
                    multiplayerMenu_state.enter_state()
        if (actions['Esc']):
            self.exit_state()
            self.exit_state()
            self.exit_state()

    def render(self, display):
        display.blit(self.game.menubg, (0, 0))

        self.helper.draw_text(display, 'Chose one', self.game.WHITE, 60, self.game.DISPLAY_W / 2, 50)
        self.menuGUI.render(display)

    def enter_state(self):
        super().enter_state()

    def exit_state(self):
        super().exit_state()




class MultiplayeClinetMenu(State):
    def __init__(self, game):
        State.__init__(self, game)
        self.mulHelper = MultiplayerHelper()

        
        self.room_id  = ''

        self.againBool = False
   

    def update(self, delta_time, actions):
        if actions['enter']:
            self.againBool = True
            self.room_id  = ''
        elif(actions['backspace']) and len(self.room_id)>0:
            self.room_id  = self.room_id[:-1]
        else:                    
            for c in self.game.keys:
                self.room_id+=c
        pass


        if (actions['Esc']):
            self.exit_state()




    def render(self, display):
        display.blit(self.game.menubg, (0, 0))
        self.helper.draw_text(display, 'write the room id and press enter', self.game.WHITE, 35, self.game.DISPLAY_W / 2, 50)
        self.helper.draw_text(display, self.room_id, self.game.WHITE, 60, self.game.DISPLAY_W / 2, self.game.DISPLAY_H / 2)

        if(self.againBool):
            self.helper.draw_text(display, 'Err, try again', self.game.RED, 30, self.game.DISPLAY_W / 2,self.game.DISPLAY_H - 190)



    def enter_state(self):
        super().enter_state()

    def exit_state(self):
        super().exit_state()
        

class MultiplayerHostMenu(State):
    def __init__(self, game):
        State.__init__(self, game)
        self.mulHelper = MultiplayerHelper()

        
        
        self.ip_address, self.port = self.mulHelper.get_ip_address()
        self.room_id = self.mulHelper.ip_to_room_id(self.ip_address, self.port)

        print(self.room_id)
    

    def update(self, delta_time, actions):
        if (actions['Esc']):
            self.exit_state()




    def render(self, display):
        display.blit(self.game.menubg, (0, 0))

        self.helper.draw_text(display, 'Your room Id is:', self.game.WHITE, 60, self.game.DISPLAY_W / 2, 50)
        self.helper.draw_text(display, self.room_id, self.game.WHITE, 60, self.game.DISPLAY_W / 2, self.game.DISPLAY_H / 2)
        self.helper.draw_text(display, 'Wait untill the other player joins', self.game.RED, 30, self.game.DISPLAY_W / 2,self.game.DISPLAY_H - 190)



    def enter_state(self):
        super().enter_state()

    def exit_state(self):
        super().exit_state()
        
        
        
        
        
        
        
        