from collections import deque
import threading
from states.pauseMenu import PauseMenu
from states.state import State
from states.winnerMenu import WinnerMenu
from states.drawMenu import DrawMenu
from util.sprite import Spritesheet
from util.tile import TileMap
from util.music import *
import pygame
from util.helpers import *
import time
from threading import Lock, Thread




# pieces for each color.
EMPTY_TILE = 0

BLUE_SMALL,BLUE_MEDIUM,BLUE_LARGE,BLUE_XLARGE, ALL_BLUE  = 1,2,4,8,15
RED_SMALL,RED_MEDIUM,RED_LARGE,RED_XLARGE, ALL_RED  = 16,32,64,128,240
BLUE, RED = 0, 1

# SRC OR DEST (CLICK_LOCATION , i , j)



BOARDERS = -1
BLUE_TURN = BLUE_PLAYER =  0
RED_TURN = RED_PLAYER =  1
EASY , HARD = 1, 2

# different playing modes
PLAYER_VS_PLAYER = 0
PLAYER_VS_OTHER = 1
AI_VS_AI = 2

TILE_SIZE = TILE_HEIGHT = TILE_WIDTH = 120
INVENTORY_MOVE = 0
BOARD_MOVE = 1


AI_OPPONENT_IN_OTHER= 0
ONLINE_OPPONENT_IN_OTHER= 1


class Playing(State):
    def __init__(self, game, game_type, my_color = BLUE, opponent_type_in_other_mode = None):
        State.__init__(self, game)

        if getattr(sys, 'frozen', False):
            # Running as compiled executable
            base_path = sys._MEIPASS
        else:
            # Running as a script
            base_path = os.path.abspath(".")

        assets_path = os.path.join(base_path, "assets")

        self.lock = Lock()
        self.spritesheet = Spritesheet(rf'{assets_path}/sprites/sprites.png')
        self.map = TileMap(rf'{assets_path}/sprites/map.csv', self.spritesheet)
        self.bg = pygame.image.load(rf"{assets_path}/background/game background(space).png")
        
        self.turn = BLUE_PLAYER  # BLUE staconda arts the game
        self.players_names = ['Player 1', 'Player 2']
        self.turn_text = self.players_names[self.turn] + ' Turn'
        self.inventory_tiles = None
        self.board_tiles = [[], [], [], []]
        self.highlighted_tile_rect = None 
        self.source_selected = False  # stores whether the source piece is selected
        self.source_values =  [-1,-1,-1] # stores source values
        self.destination_values =  [-1,-1,-1] # stores dest values
        self.global_music_player = game.global_music_player
        self.last_red = []
        self.last_red = deque(self.last_red)
        self.done = True
        self.last_blue = []
        self.last_blue = deque(self.last_blue)
        self.mode = game_type
        self.my_color = my_color
        self.opponent_type_in_other_mode = opponent_type_in_other_mode

        self.client_socket = self.game.client_socket
        
        

        # Initial board                                                          
        self.board = [
            [EMPTY_TILE, EMPTY_TILE, EMPTY_TILE, EMPTY_TILE],
            [EMPTY_TILE, EMPTY_TILE, EMPTY_TILE, EMPTY_TILE],
            [EMPTY_TILE, EMPTY_TILE, EMPTY_TILE, EMPTY_TILE],
            [EMPTY_TILE, EMPTY_TILE, EMPTY_TILE, EMPTY_TILE]]
        
        self.inventory = [
            [ALL_BLUE, ALL_BLUE, ALL_BLUE], # inv for blue
            [ALL_RED, ALL_RED, ALL_RED]  # inv for red
        ]

        self.refresh_UI()

        self.animation = False
        self.animated_tile_pos = {'x': -1, 'y':-1 }
        self.src_for_anime_pos = {'x': -1, 'y':-1 }
        self.dst_for_anime_pos = {'x': -1, 'y':-1 }
        self.animation_speed = 120
        self.slope = -1

    
    def set_animation_parameter(self, src, dst):
        if(src[0]==INVENTORY_MOVE):
            largest_piece_src = get_largest_piece(self.inventory[src[1]][src[2]])

            self.inventory[src[1]][src[2]] &= ~largest_piece_src
            self.src_for_anime_pos['x'] = self.inventory_tiles[src[1]][src[2]].rect.x + self.map.tile_size/2
            self.src_for_anime_pos['y'] = self.inventory_tiles[src[1]][src[2]].rect.y+ self.map.tile_size/2


        elif(src[0]==BOARD_MOVE):
            largest_piece_src = get_largest_piece(self.board[src[1]][src[2]])
            self.board[src[1]][src[2]] &= ~largest_piece_src
            self.src_for_anime_pos['x'] = self.board_tiles[src[1]][src[2]].rect.x+ self.map.tile_size/2
            self.src_for_anime_pos['y'] = self.board_tiles[src[1]][src[2]].rect.y+ self.map.tile_size/2

        self.animated_tile_pos = self.src_for_anime_pos


        self.dst_for_anime_pos['x'] = self.board_tiles[dst[1]][dst[2]].rect.x+ self.map.tile_size/2
        self.dst_for_anime_pos['y'] = self.board_tiles[dst[1]][dst[2]].rect.y+ self.map.tile_size/2

        self.largest_peice_for_animation = largest_piece_src   
        
        self.slope = (self.dst_for_anime_pos['y'] - self.src_for_anime_pos['y']) / (self.dst_for_anime_pos['x'] - self.src_for_anime_pos['x'] + 0.0001)
        self.destination_values = dst   
        self.animation = True
        self.x = None

        self.refresh_UI()
        

    def handle_thread(self):
        
        self.lock.acquire()
        self.done = False
        self.lock.release()
        
        if not self.animation:
            self.check_for_draw()
            self.check_wins()
        self.handle_mode_operations()
        
        self.lock.acquire()
        self.done = True
        self.lock.release()
        


    def parse_input_string(self,input_string):
        # Convert the input string to a numeric array
        if input_string :
            numeric_array = [int(num) for num in input_string.split()]
            src = numeric_array[0:3]
            dst = numeric_array[3:6]
            # print(src,dst)
            self.set_animation_parameter(src, dst)
            
    
    def update(self, delta_time, actions):
        
        if(self.done):
            self.x = threading.Thread(target=self.handle_thread).start()
            
        if(self.mode!=AI_VS_AI and ( not (self.turn == RED_TURN and self.mode == PLAYER_VS_OTHER) or self.turn == BLUE_TURN)):
            self.highlight_nearest_tile(pygame.mouse.get_pos())
        
        if(self.mode != AI_VS_AI or(self.turn == self.my_color and self.mode==PLAYER_VS_OTHER)):
            if not self.animation and actions['LEFT_MOUSE_KEY_PRESS']:
                self.handle_mouse_click()

        if actions['Esc']:
            pause_menu = PauseMenu(self.game)
            pause_menu.enter_state()



    def handle_mode_operations(self):
        self.lock.acquire()
        if(self.mode == AI_VS_AI or (self.turn ==(1-self.my_color) and self.mode==PLAYER_VS_OTHER) ):
            if self.animation:
                if self.animated_tile_pos['x'] < self.dst_for_anime_pos['x']:
                    self.animated_tile_pos['x'] += self.animation_speed
                    self.animated_tile_pos['y'] += self.animation_speed * self.slope
                elif self.animated_tile_pos['x'] > self.dst_for_anime_pos['x']:
                    self.animated_tile_pos['x'] -= self.animation_speed
                    self.animated_tile_pos['y'] -= self.animation_speed * self.slope
                else:
                    # print(self.largest_peice_for_animation,  self.destination_values,'--------------------------------------')
                    self.board[self.destination_values[1]][self.destination_values[2]] |= self.largest_peice_for_animation
                    self.global_music_player.play_sfx()
                    self.animation = False
                    self.switch_turns()
                    self.refresh_UI()

            else:
                if(self.mode == AI_VS_AI or self.opponent_type_in_other_mode == AI_OPPONENT_IN_OTHER):
                    start = time.time()
                    
                    state_Astext = self.helper.flush(self.turn, self.board,self.inventory)
                    s = (self.helper.cpp_code(state_Astext))
                    
                    self.parse_input_string(s)
                    end = time.time()
                    print(f"operation took {1000*(end-start)}ms")
                    
                elif(self.opponent_type_in_other_mode == ONLINE_OPPONENT_IN_OTHER):
                    s = self.client_socket.recv(1024).decode()
                    self.parse_input_string(s)
        self.lock.release()

 




    def refresh_UI(self):
        self.board_tiles = self.map.reconstruct_map(self.board, self.source_selected, self.source_values)
        self.inventory_tiles = self.map.reconstruct_inventory(self.inventory, self.source_selected, self.source_values)



    def apply_move(self,src,src_i,src_j,dst,dst_i,dst_j):
        largest_piece_in_source = get_largest_piece(src[src_i][src_j])
        src[src_i][src_j] &= ~(largest_piece_in_source)
        dst[dst_i][dst_j] |= largest_piece_in_source

        if(self.opponent_type_in_other_mode == ONLINE_OPPONENT_IN_OTHER):
            move = [self.source_values,self.destination_values]
            self.client_socket.send(convert_move_to_str(move).encode())
            self.check_wins()
        self.refresh_UI()





    def handle_mouse_click(self):
        move_type, i, j, state = self.get_clicked_tile_id()
        source_type, source_i, source_j = self.source_values
        
        if(source_type == BOARD_MOVE):
            if(self.source_selected and (get_largest_piece_neutural(self.board[source_i][source_j]) <= get_largest_piece_neutural(self.board[i][j]))):
                return
        
        if(source_type == INVENTORY_MOVE):
            if(self.source_selected and (get_largest_piece_neutural(self.inventory[source_i][source_j]) <= get_largest_piece_neutural(self.board[i][j]))):
                return

  
        # if the source is in the boarders, ignore it.
        if (move_type == BOARDERS):
            return

        # if the source is an empty tile
        if (not self.source_selected and move_type == BOARD_MOVE and state == EMPTY_TILE):
            return

        # if the source is the same as the destination.
        elif (self.source_selected and [move_type, i, j] == self.source_values):
            return

        # if the destination is the inventory.
        elif (self.source_selected and (move_type == INVENTORY_MOVE)):
            return

        # if selected from inventory is blue and it's red turn
        elif move_type == INVENTORY_MOVE and self.turn == RED_TURN and i == BLUE:
            return

        # if selected from inventory is red and it's blue turn
        elif move_type == INVENTORY_MOVE and self.turn == BLUE_TURN and  i == RED:
            return
        
        
        # if source is not selected.
        if (not self.source_selected and ((self.turn == BLUE_TURN and is_blue(get_largest_piece(state))) or (self.turn == RED_TURN and is_red(get_largest_piece(state)))) and not (self.mode == PLAYER_VS_OTHER and self.turn != self.my_color)):
            # save source values.
            self.source_values = [move_type, i, j]
            self.source_selected = True
            self.refresh_UI()

            return
        else :
            self.destination_values = [move_type,i,j]


        # piece selected is blue in red's turn or red in blue's turn.
        if (source_type == BOARD_MOVE):
            if is_blue(get_largest_piece(self.board[source_i][source_j])) and self.turn == RED_TURN:
                return

            if is_red(get_largest_piece(self.board[source_i][source_j]))  and self.turn == BLUE_TURN:
                return
        # if destination piece is a larger piece dont allow it
        
            
        if(self.mode == PLAYER_VS_PLAYER or (self.turn ==self.my_color and self.mode==PLAYER_VS_OTHER)):
            move = [self.source_values,self.destination_values]
            self.move_piece(move)


    # # checks if the held piece is near a board tile and highlight that tile.
        
    def highlight_nearest_tile(self,pos):
        for row in self.board_tiles:
            for tile in row:
                tile_rect = tile.get_rect()
                if tile_rect.collidepoint(pos):
                    # Store the rectangle information instead of drawing
                    self.highlighted_tile_rect = tile_rect
                    tile_rect
                    return
        self.highlighted_tile_rect = None  # Reset if no tile is highlighted   



    # move piece from source to destination.
    def move_piece(self,move):

        # load source and destenation values into a variable for better readability.
        source_type, src_i, src_j = move[0]
        dst_location,dst_i,dst_j = move[1] # save destenation values.
        self.source_selected = False
        val_dst = self.board[dst_i][dst_j]


        # if the source is an inventory.
        if source_type == INVENTORY_MOVE:

            # get the value of the source location (BLUE Inventory)
            val_src = self.inventory[src_i][src_j]

            # if the move is valid, if the move is valid, go ahead with it.
            if not is_move_valid(val_src, val_dst):
                return
            
            self.apply_move(self.inventory,src_i,src_j,self.board,dst_i,dst_j)

        # if the source is a board.
        elif (source_type == BOARD_MOVE):

            # get the value of the source location (board).
            val_src = self.board[src_i][src_j]
            
            # if the move is valid, if the move is valid, go ahead with it.
            if (not is_move_valid(val_src, val_dst)):
                return

            self.apply_move(self.board,src_i,src_j,self.board,dst_i,dst_j)
            
        self.switch_turns()
        self.global_music_player.play_sfx()
        

    def render(self, display):

        display.blit(self.bg, (0, 0))

        # Display the current turn text at the top of the screen
        self.helper.draw_text(display, self.turn_text, self.game.global_font_color, 20, self.game.DISPLAY_W / 2, 30,True)
        self.map.draw_map_on_canvas(display)

        # if the mouse is near a certain tile.
        if self.highlighted_tile_rect:
            self.render_highlighted_tile(display)

        # if a piece is choosen
        if self.source_selected:
            self.render_selected_tile(display)

        if self.animation:
            self.map.selected_tile(self.largest_peice_for_animation,[self.animated_tile_pos['x'], self.animated_tile_pos['y']]).draw(display)    

        # Step 4: Update the display
        pygame.display.flip()  # or pygame.display.update()

    def enter_state(self):
        super().enter_state()

    def exit_state(self):
        self.game.close_connection()
        super().exit_state()

    # checks for a winner at the beginning of each round.
    def check_wins(self):
        # create 3 loops that checks for a winner in each row, column, diagonal.
        blue = 0
        red = 0
        for i in range(4):
            # check if the row has 4 pieces of the same color.
            for j in range(4):
                # if the current piece is red then increment red by 1.
                if is_red(get_largest_piece(self.board[i][j])) and not self.board[i][j] == EMPTY_TILE:
                    red += 1
                # if the current piece is blue then increment blue by 1.
                elif is_blue(get_largest_piece(self.board[i][j])) and not self.board[i][j] == EMPTY_TILE:
                    blue += 1

            if red == 4:
                self.announce_winner(RED_PLAYER)

            elif blue == 4:
                self.announce_winner(BLUE_PLAYER)

            # reset counters.
            blue = 0
            red = 0

        for i in range(4):
            # check if the column has 4 pieces of the same color.
            for j in range(4):
                # if the current piece is red then increment red by 1.
                if is_red(get_largest_piece(self.board[j][i])) and not self.board[j][i] == EMPTY_TILE:
                    red += 1
                # if the current piece is blue then increment blue by 1.
                elif is_blue(get_largest_piece(self.board[j][i])) and not self.board[j][i] == EMPTY_TILE:
                    blue += 1

            if red == 4:
                self.announce_winner(RED_PLAYER)
                

            elif blue == 4:
                self.announce_winner(BLUE_PLAYER)
                

            # reset counters.
            blue = 0
            red = 0

        # main diagonal
        for i in range(4):
            if is_red(get_largest_piece(self.board[i][i])) and not self.board[i][i] == EMPTY_TILE:
                red += 1

            elif is_blue(get_largest_piece(self.board[i][i])) and not self.board[i][i] == EMPTY_TILE:
                blue += 1

        if red == 4:
            self.announce_winner(RED_PLAYER)

        elif blue == 4:
            self.announce_winner(BLUE_PLAYER)
            

        blue = 0
        red = 0

        # other diagonal
        for i in range(4):
            if  is_red(get_largest_piece(self.board[i][3-i])) and not self.board[i][3 - i] == EMPTY_TILE:
                red += 1

            elif is_blue(get_largest_piece(self.board[i][3-i])) and not self.board[i][3 - i] == EMPTY_TILE:
                blue += 1

        if red == 4:
            self.announce_winner(RED_PLAYER)

        elif blue == 4:
            self.announce_winner(BLUE_PLAYER)

    # check if the mouse click is within a certain tile and returns its position.
    def get_clicked_tile_id(self):

        mouse_location_x, mouse_location_y = pygame.mouse.get_pos()

        # check board tiles.
        for i in range(4):
            for j in range(4):
                rect = self.board_tiles[i][j].get_rect()
                if rect.collidepoint(mouse_location_x, mouse_location_y):
                    return BOARD_MOVE, i, j, self.board[i][j]

        # check red inventory tiles
        for i in range(3):
            rect = self.inventory_tiles[RED][i].get_rect()

            if rect.collidepoint(mouse_location_x, mouse_location_y):
                if (self.inventory[RED][i] == 0):
                    return BOARDERS, BOARDERS, BOARDERS, BOARDERS
                return INVENTORY_MOVE, RED, i , self.inventory[RED][i]

        # check blue inventory tiles
        for i in range(3):
            rect = self.inventory_tiles[BLUE][i].get_rect()

            if rect.collidepoint(mouse_location_x, mouse_location_y):
                if (not self.inventory[BLUE][i]):
                    return BOARDERS, BOARDERS, BOARDERS, BOARDERS
                return INVENTORY_MOVE, BLUE, i , self.inventory[BLUE][i]

        return BOARDERS, BOARDERS, BOARDERS, BOARDERS
        
    # checks for a draw in the beginning of a round.
    def check_for_draw(self):
        
        if(is_draw(self.last_blue,self.last_red)):
            draw_state = DrawMenu(self.game, self.mode)
            draw_state.enter_state()

        if(len(self.last_blue) > 6):
            self.last_blue.popleft()

        if(len(self.last_red) > 6):
            self.last_red.popleft()

    # handles events that happen when a player wins.
    def announce_winner(self,player):
        self.global_music_player.play_win_sound()
        time.sleep(3)
        self.global_music_player.play_background_sound()
        winner_state = WinnerMenu(self.game, player+1, self.mode, self.my_color, self.opponent_type_in_other_mode )
        winner_state.enter_state() 

    # switches turns after a move is made.
    def switch_turns(self):
        if self.turn == BLUE_TURN:
            self.turn = RED_TURN
            self.last_blue.append([self.source_values,self.destination_values])
            self.turn_text = self.players_names[RED] + ' Turn'
        else:
            self.turn = BLUE_TURN
            self.last_red.append([self.source_values,self.destination_values])
            self.turn_text = self.players_names[BLUE] + ' Turn'

    def render_selected_tile(self,display):
            # get fetch data from source values.
            source_location = self.source_values[0]
            source_i = self.source_values[1]
            source_j = self.source_values[2]
            mouse_pos = pygame.mouse.get_pos()
            largest_piece_in_source = None

            # if the source is on the board, get the largest piece in that location.
            if(source_location==BOARD_MOVE):
                largest_piece_in_source = get_largest_piece(self.board[source_i][source_j])

                # if the its not that player's turn, cancel drawing.
                if not (is_red(largest_piece_in_source) and self.turn==RED_TURN) and not(is_blue(largest_piece_in_source) and self.turn==BLUE_TURN):
                    return
                    
            # only allow drawing if the source is the blue inventory, and it's the blue turn.       
            elif(source_location==INVENTORY_MOVE):
                largest_piece_in_source = get_largest_piece(self.inventory[source_i][source_j])

            # draw the selected piece on the mouse.
            self.map.selected_tile(largest_piece_in_source,mouse_pos).draw(display)


    def render_highlighted_tile(self,display):
            
            s = pygame.Surface((TILE_WIDTH-10,TILE_HEIGHT-10))  # create a surface with these dimensions
            s.set_alpha(64)  # alpha level (opacity)
            s.fill((255,255,255)) # set color to red
            display.blit(s,(self.highlighted_tile_rect.x+5,self.highlighted_tile_rect.y+5))  # shift start coordinates of the surface and blit