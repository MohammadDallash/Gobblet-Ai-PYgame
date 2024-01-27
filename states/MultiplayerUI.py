import locale
from threading import Lock
import threading
from states.state import State
import socket
from util.helpers import MenuGUI
import pygame
from util.MultiplayerHelper import MultiplayerHelper
from states.playing import Playing

PLAYER_VS_OTHER = 1
ONLINE_OPPONENT_IN_OTHER= 1

BLUE, RED = 0, 1

class MultiplayerChooseMenu(State):
    def __init__(self, game):
        State.__init__(self, game)

        self.options_str = ['Host a game', 'Connect to a game']
        self.cur_option = 0
        self.menuGUI = MenuGUI(self.game, self.options_str, self.cur_option, font_size=game.global_text_font_size,
                               x_pos=self.game.DISPLAY_W / 2)
        self.x = None

    def update(self, delta_time, actions):
        self.cur_option = self.menuGUI.update_cur_opt(actions)

        if actions['enter']:
            if(self.cur_option == 1):
                multiplayerMenu_state =  MultiplayerClientMenu(self.game)
            else :
                multiplayerMenu_state =  MultiplayerHostMenu(self.game)
            multiplayerMenu_state.enter_state()

        x, y = pygame.mouse.get_pos()
        for i in range(len(self.options_str)):
            if self.menuGUI.mouse_collidepoint(x, y, i):
                self.menuGUI.cur_option = i
                if actions['LEFT_MOUSE_KEY_PRESS']:
                    if(self.cur_option == 1):
                        multiplayerMenu_state =  MultiplayerClientMenu(self.game)
                    else :
                        multiplayerMenu_state =  MultiplayerHostMenu(self.game)
                    multiplayerMenu_state.enter_state()
        if (actions['Esc']):
            self.exit_state()
            self.exit_state()

    def render(self, display):
        display.blit(self.game.menubg, (0, 0))

        self.helper.draw_text(display, 'Multiplayer', self.game.global_font_color, self.game.global_title_font_size, self.game.DISPLAY_W / 2, 50,True)
        self.menuGUI.render(display)

    def enter_state(self):
        super().enter_state()

    def exit_state(self):
        if self.x:
            self.x.exit() 
        super().exit_state()




class MultiplayerClientMenu(State):
    def __init__(self, game):
        State.__init__(self, game)
        self.mulHelper = MultiplayerHelper()
        
        print('you are a clinet and your local ip is', socket.gethostbyname(socket.gethostname()))
        
        pygame.scrap.init()
        pygame.scrap.set_mode(pygame.SCRAP_CLIPBOARD)
        
        self.room_id  = ''

        self.againBool = False
        self.x = None
   

    def update(self, delta_time, actions):
        if actions['enter']:
            self.againBool = True
            try:
                ip, port = self.mulHelper.room_id_to_ip(self.room_id)
                print("you are trying to conect to", ip, port)
                self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                self.client_socket.connect((ip, port))
                self.game.client_socket =   self.client_socket
                playing_state = Playing (self.game, PLAYER_VS_OTHER, opponent_type_in_other_mode=ONLINE_OPPONENT_IN_OTHER, my_color = RED)    
                playing_state.enter_state()


            except Exception as e:
                self.againBool = True
                self.room_id = ''
                                   
        elif(actions['backspace']) and len(self.room_id)>0:
            self.room_id  = self.room_id[:-1]
        else:                    
            for c in self.game.keys:
                self.room_id+=c
        pass


        if (actions['Esc']):
            self.exit_state()
        
        if(actions["k_v"]):
                self.room_id += pygame.scrap.get(pygame.SCRAP_TEXT)[0:-1].decode("utf-8")
           


    def render(self, display):
        display.blit(self.game.menubg, (0, 0))
        self.helper.draw_text(display, 'Enter the host ID', self.game.global_font_color, self.game.global_title_font_size, self.game.DISPLAY_W / 2, 50)
        self.helper.draw_text(display, self.room_id, self.game.global_font_color, 60, self.game.DISPLAY_W / 2, self.game.DISPLAY_H / 2 - 50, is_default=True)

        if(self.againBool):
            self.helper.draw_text(display, 'Error, Please try again.', self.game.RED, self.game.global_text_font_size, self.game.DISPLAY_W / 2,self.game.DISPLAY_H - 250)
        else :
            self.helper.draw_text(display, 'You can press Ctrl+v for pasting', self.game.RED, self.game.global_text_font_size, self.game.DISPLAY_W / 2,self.game.DISPLAY_H - 250)



    def enter_state(self):
        super().enter_state()

    def exit_state(self):
        if(self.x != None):
            self.x.exit()
        super().exit_state()
        

class MultiplayerHostMenu(State):
    def __init__(self, game):
        State.__init__(self, game)
        self.mulHelper = MultiplayerHelper()
        self.done = True
        self.thread = None
        self.lock = Lock()
        self.ip_address, self.port = self.mulHelper.get_ip_address()
        self.room_id = self.mulHelper.ip_to_room_id(self.ip_address, self.port)
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        
        print('you are a server and your local ip and port is', self.ip_address, self.port)

    

    def update(self, delta_time, actions):

        if(self.done):
            self.thread = threading.Thread(target=self.handle_thread).start()

        if (actions['Esc']):
            self.exit_state()
            try:
                self.server_socket.close()
            except Exception as e:
                pass

    # handles calculations on a separate thread
    def handle_thread(self):
        self.done = False
        self.server_socket.bind((self.ip_address, self.port))
        self.server_socket.listen(1)
        pygame.scrap.init()
        pygame.scrap.put(pygame.SCRAP_TEXT,str(self.room_id).encode('utf-8'))
        self.client_socket, self.client_address = self.server_socket.accept()
        self.server_socket.close()            
        self.game.client_socket =   self.client_socket
        playing_state = Playing(self.game, PLAYER_VS_OTHER, opponent_type_in_other_mode= ONLINE_OPPONENT_IN_OTHER, my_color = BLUE)
        
        playing_state.enter_state()
        

    def render(self, display):
        display.blit(self.game.menubg, (0, 0))

        self.helper.draw_text(display, 'Your Room ID is:', self.game.global_font_color, self.game.global_title_font_size, self.game.DISPLAY_W / 2, 50)
        
        self.helper.draw_text(display, self.room_id, self.game.global_font_color, self.game.global_title_font_size, self.game.DISPLAY_W / 2, self.game.DISPLAY_H / 2 - 50,is_default=True)
        
        self.helper.draw_text(display, 'Waiting for a player to join...', self.game.RED, self.game.global_options_text_size+10, self.game.DISPLAY_W / 2,self.game.DISPLAY_H - 240)
        self.helper.draw_text(display, 'Room ID is copied to clipboard!', self.game.RED, self.game.global_options_text_size, self.game.DISPLAY_W / 2,self.game.DISPLAY_H - 160)




    def enter_state(self):
        super().enter_state()

    def exit_state(self):
        if self.thread != None:
            self.thread.exit()
        super().exit_state()
        
        
        
        
        
        
        
        