from collections import deque
from states.pauseMenu import PauseMenu
from states.state import State
from states.winnerMenu import WinnerMenu
from states.drawMenu import DrawMenu
from util.sprite import Spritesheet
from util.tile import TileMap
import pygame
from util.helpers import *
import time




# pieces for each color.
EMPTY_TILE = 0

BLUE_SMALL,BLUE_MEDIUM,BLUE_LARGE,BLUE_XLARGE, ALL_BLUE  = 1,2,4,8,15
RED_SMALL,RED_MEDIUM,RED_LARGE,RED_XLARGE, ALL_RED  = 16,32,64,128,240
BLUE, RED = 0, 1

# SRC OR DEST (CLICK_LOCATION , i , j)


BLUE_INVENTORY,RED_INVENTORY = "blue" ,"red"

BOARD_TILE = "board"

BOARDERS = "empty"
DONT_CARE = "anything invalid"
BLUE_TURN = BLUE_PLAYER =  1
RED_TURN = RED_PLAYER =  2

# different playing modes
PLAYER_VS_PLAYER = 0
PLAYER_VS_AI = 1
AI_VS_AI = 2
MULTIPLAYER_SERVER = 3
MULTIPLAYER_CLIENT = 4

TILE_SIZE = TILE_HEIGHT = TILE_WIDTH = 120
INVENTORY_MOVE = 0
BOARD_MOVE = 1

class Playing(State):
    def __init__(self, game, game_type):
        State.__init__(self, game)
        self.spritesheet = Spritesheet('assets/sprites/sprites.png')
        self.map = TileMap('assets/sprites/map.csv', self.spritesheet)
        self.bg = pygame.image.load("assets/background/background.png")
        self.turn = BLUE_PLAYER  # BLUE starts the game
        self.players_names = ['Player 1', 'Player 2']
        self.turn_text = self.players_names[self.turn - 1] + ' Turn'
        self.inventory_tiles = None
        self.board_tiles = [[], [], [], []]
        self.highlighted_tile_rect = None 
        self.source_selected = False  # stores whether the source piece is selected
        self.source_values =  [-1,-1,-1] # stores source values
        self.destination_values =  [-1,-1,-1] # stores dest values


        self.last_red_moves = []
        self.last_red_moves = deque(self.last_red_moves)


        self.last_blue_moves = []
        self.last_blue_moves = deque(self.last_blue_moves)

        self.is_draw = False

        ################################
        self.mode = game_type
        ################################
        self.game_started = False


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

        self.map.reconstruct_map(self.board)

        self.game_started = False


    def parse_input_string(self,input_string):
        # Convert the input string to a numeric array
        if input_string :
            numeric_array = [int(num) for num in input_string.split()]
            src = numeric_array[0:3]
            dst = numeric_array[3:6]

            if(src[0]==INVENTORY_MOVE):
                largest_piece_src = get_largest_piece(self.inventory[src[1]][src[2]])
                self.inventory[src[1]][src[2]] &= ~largest_piece_src
                #create animation
                self.board[dst[1]][dst[2]] |= largest_piece_src
                

            elif(src[0]==BOARD_MOVE):
                largest_piece_src = get_largest_piece(self.board[src[1]][src[2]])
                self.board[src[1]][src[2]] &= ~largest_piece_src
                self.board[dst[1]][dst[2]] |=  largest_piece_src
        
    
    def update(self, delta_time, actions):
        # if self.turn == BLUE_PLAYER :
        #     self.mode = PLAYER_VS_PLAYER
        # elif self.turn == RED_PLAYER:
        #     self.mode = AI_VS_AI
        
        if(self.game_started == False):
            self.game_started = True
            self.board_tiles = self.map.reconstruct_map(self.board)
            self.inventory_tiles = self.map.reconstruct_inventory(self.inventory)
            return  

        
        self.check_for_draw()
        self.check_wins()
        self.handle_mode_operations()

        
        self.highlight_nearest_tile(pygame.mouse.get_pos())

        if(self.mode != AI_VS_AI):
            if actions['LEFT_MOUSE_KEY_PRESS']:
                time.sleep(0.1)
                self.handle_mouse_click()
        

        self.board_tiles = self.map.reconstruct_map(self.board, self.source_selected, self.source_values)
        self.inventory_tiles = self.map.reconstruct_inventory(self.inventory, self.source_selected, self.source_values)


        if actions['Esc']:
            pause_menu = PauseMenu(self.game)
            pause_menu.enter_state()



    def handle_mode_operations(self):
        
        if(self.mode == AI_VS_AI):
            self.helper.flush_to_file(self.turn-1, self.board,self.inventory)
            s = (self.helper.cpp_code("current_state_file.txt"))
            self.parse_input_string(s)
            self.switch_turns()




        elif(self.mode == MULTIPLAYER_CLIENT):
            if(self.destination_values):
                move = [self.source_values,self.destination_values]
                self.client.send(convert_move_to_str(move).encode('utf-8'))
                data = self.client.recv(1024)


        elif(self.mode==MULTIPLAYER_SERVER):
            if(self.destination_values):
                client, addr = self.server.accept()
                data = client.recv(1024)
                data_str = data.decode('utf-8')
                move = convert_stream_to_list(data_str)
                client.send(move)
                # self.server.close()





    def handle_mouse_click(self):
        location, i, j, state = self.get_clicked_tile_id(self.board_tiles, self.inventory_tiles)

        # if the source is in the boarders, ignore it.
        if (location == BOARDERS):
            return

        # if the source is an empty tile
        if (not self.source_selected and location == BOARD_TILE and state == EMPTY_TILE):
            return

        # if the source is the same as the destination.
        elif (self.source_selected and [location, i, j] == self.source_values):
            return

        # if the destination is the inventory.
        elif (self.source_selected and (location == BLUE_INVENTORY or location == RED_INVENTORY)):
            return

        # if selected from inventory is blue and it's red turn
        elif location == BLUE_INVENTORY and self.turn == RED_TURN:
            return

        # if selected from inventory is red and it's blue turn
        elif location == RED_INVENTORY and self.turn == BLUE_TURN:
            return
        
        
        # if source is not selected.
        if (not self.source_selected and ( (self.turn == BLUE_TURN and get_largest_piece(state)<ALL_BLUE) or (self.turn == RED_TURN and get_largest_piece(state)>ALL_BLUE))):
            # save source values.
            self.source_values = [location, i, j]
            self.source_selected = True
            return
        else:
            self.destination_values = [location,i,j]

        if(self.mode == PLAYER_VS_PLAYER):
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
        source_location, source_i, source_j = move[0]
        dst_location,dst_i,dst_j = move[1] # save destenation values.

        self.source_selected = False

        val_dst = self.board[dst_i][dst_j]

        # piece selected is blue in red's turn or red in blue's turn.
        if (source_location == BOARD_TILE):
            if get_largest_piece(self.board[source_i][source_j]) in [BLUE_SMALL, BLUE_MEDIUM, BLUE_LARGE,BLUE_XLARGE] and self.turn == RED_TURN:
                return

            if get_largest_piece(self.board[source_i][source_j]) in [RED_SMALL, RED_MEDIUM, RED_LARGE,RED_XLARGE] and self.turn == BLUE_TURN:
                return

        # if the source is an inventory.
        if source_location == BLUE_INVENTORY:

            # get the value of the source location (BLUE Inventory)
            val_src = self.inventory[BLUE][source_i]

            # get the largest piece in that place
            largest_piece_in_source = get_largest_piece(val_src)

            # if the move is valid, if the move is valid, go ahead with it.
            if is_move_valid(val_src, val_dst):

                self.inventory[BLUE][source_i] &= ~(largest_piece_in_source)
                self.board[dst_i][dst_j] |= largest_piece_in_source
                self.switch_turns()

            else:
                return

        elif (source_location == RED_INVENTORY):

            # get the value of the source location (RED Inventory).
            val_src = self.inventory[RED][source_i]

            # get the largest piece in that place.
            largest_piece_in_source = get_largest_piece(val_src)

            # if the move is valid, if the move is valid, go ahead with it.
            if (is_move_valid(val_src, val_dst)):
                self.inventory[RED][source_i] &= ~(largest_piece_in_source)
                self.board[dst_i][dst_j] |= largest_piece_in_source
                self.switch_turns()
            else:
                return

        # if the source is a board.
        elif (source_location == BOARD_TILE):

            # get the value of the source location (board).
            val_src = self.board[source_i][source_j]
            # get the largest piece in that place.
            largest_piece_in_source = get_largest_piece(val_src)
            # if the move is valid, if the move is valid, go ahead with it.
            if (is_move_valid(val_src, val_dst)):
                self.board[source_i][source_j] &= ~(largest_piece_in_source)
                self.board[dst_i][dst_j] |= largest_piece_in_source
                self.switch_turns()
            else:
                return

    def render(self, display):
        # Step 1: Clear the screen
        # display.fill(self.game.BROWN)
        display.blit(self.bg, (0, 0))

        # Step 2: Draw game elements
        # Display the current turn text at the top of the screen
        self.helper.draw_text(display, self.turn_text, self.game.RED, 20, self.game.DISPLAY_W / 2, 30)
        self.map.draw_map_on_canvas(display)

        # if the mouse is near a certain tile.
        if self.highlighted_tile_rect:
            s = pygame.Surface((TILE_WIDTH-10,TILE_HEIGHT-10))  # create a surface with these dimensions
            s.set_alpha(64)  # alpha level (opacity)
            s.fill((255,255,255)) # set color to red
            display.blit(s,(self.highlighted_tile_rect.x+5,self.highlighted_tile_rect.y+5))  # shift start coordinates of the surface and blit


        # if a piece is choosen
        if self.source_selected:
            # get fetch data from source values.
            source_location = self.source_values[0]
            source_i = self.source_values[1]
            source_j = self.source_values[2]
            mouse_pos = pygame.mouse.get_pos()
            largest_piece_in_source = None

            # if the source is on the board, get the largest piece in that location.
            if(source_location==BOARD_TILE):
                largest_piece_in_source = get_largest_piece(self.board[source_i][source_j])

                # if the its not that player's turn, cancel drawing.
                if not (largest_piece_in_source>ALL_BLUE and self.turn==RED_TURN) and not(largest_piece_in_source<ALL_BLUE and self.turn==BLUE_TURN):
                    return
                    
            # only allow drawing if the source is the blue inventory, and it's the blue turn.       
            elif(source_location==BLUE_INVENTORY and self.turn == BLUE_TURN):
                largest_piece_in_source = get_largest_piece(self.inventory[BLUE][source_i])

             
            # only allow drawing if the source is the red inventory, and it's the red turn.    
            elif(source_location==RED_INVENTORY and self.turn == RED_TURN):
                largest_piece_in_source = get_largest_piece(self.inventory[RED][source_i])

            # draw the selected piece on the mouse.
            if(largest_piece_in_source):
                self.map.selected_tile(largest_piece_in_source,mouse_pos).draw(display)


        # Step 4: Update the display
        pygame.display.flip()  # or pygame.display.update()

    def enter_state(self):
        super().enter_state()

    def exit_state(self):
        super().exit_state()

    # checks for a winner at the beginning of each round.
    # TODO() Fix checking for largest piece
    def check_wins(self):
        # create 3 loops that checks for a winner in each row, column, diagonal.
        blue = 0
        red = 0
        for i in range(4):
            # check if the row has 4 pieces of the same color.
            for j in range(4):
                # if the current piece is red then increment red by 1.
                if get_largest_piece(self.board[i][j]) > ALL_BLUE and not self.board[i][j] == EMPTY_TILE:
                    red += 1
                # if the current piece is blue then increment blue by 1.
                elif get_largest_piece(self.board[i][j]) < RED_SMALL and not self.board[i][j] == EMPTY_TILE:
                    blue += 1

            if red == 4:
                winner_state = WinnerMenu(self.game, RED_PLAYER, self.mode, self.game.music_player.check_music())
                # time.sleep(3)
                winner_state.enter_state()
            elif blue == 4:
                winner_state = WinnerMenu(self.game, BLUE_PLAYER, self.mode, self.game.music_player.check_music())
                # time.sleep(3)
                winner_state.enter_state()
            # reset counters.
            blue = 0
            red = 0

        for i in range(4):
            # check if the column has 4 pieces of the same color.
            for j in range(4):
                # if the current piece is red then increment red by 1.
                if get_largest_piece(self.board[j][i]) > ALL_BLUE and not self.board[j][i] == EMPTY_TILE:
                    red += 1
                # if the current piece is blue then increment blue by 1.
                elif get_largest_piece(self.board[j][i]) < RED_SMALL and not self.board[j][i] == EMPTY_TILE:
                    blue += 1

            if red == 4:
                winner_state = WinnerMenu(self.game, RED_PLAYER, self.mode, self.game.music_player.check_music())
                # time.sleep(3)
                winner_state.enter_state()

            elif blue == 4:
                winner_state = WinnerMenu(self.game, BLUE_PLAYER, self.mode, self.game.music_player.check_music())
                # time.sleep(3)
                winner_state.enter_state()

            # reset counters.
            blue = 0
            red = 0

        # main diagonal
        for i in range(4):
            if get_largest_piece(self.board[i][i]) > ALL_BLUE and not self.board[i][i] == EMPTY_TILE:
                red += 1

            elif get_largest_piece(self.board[i][i]) < RED_SMALL and not self.board[i][i] == EMPTY_TILE:
                blue += 1

        if red == 4:
            winner_state = WinnerMenu(self.game, RED_PLAYER, self.mode, self.game.music_player.check_music())
            # time.sleep(3)
            winner_state.enter_state()
        elif blue == 4:
            winner_state = WinnerMenu(self.game, BLUE_PLAYER, self.mode, self.game.music_player.check_music())
            # time.sleep(3)
            winner_state.enter_state()

        blue = 0
        red = 0

        # other diagonal
        for i in range(4):
            if get_largest_piece(self.board[i][3-i]) > ALL_BLUE and not self.board[i][3 - i] == EMPTY_TILE:
                red += 1

            elif get_largest_piece(self.board[i][3-i]) < RED_SMALL and not self.board[i][3 - i] == EMPTY_TILE:
                blue += 1

        if red == 4:
            winner_state = WinnerMenu(self.game, RED_PLAYER, self.mode, self.game.music_player.check_music())
            # time.sleep(3)
            winner_state.enter_state()

        elif blue == 4:
            winner_state = WinnerMenu(self.game, BLUE_PLAYER, self.mode, self.game.music_player.check_music())
            # time.sleep(3)
            winner_state.enter_state()

    # check if the mouse click is within a certain tile and returns its position.
    def get_clicked_tile_id(self, board_tiles, inventory_tiles):

        mouse_location_x, mouse_location_y = pygame.mouse.get_pos()

        # check board tiles.
        for i in range(4):
            for j in range(4):
                rect = board_tiles[i][j].get_rect()
                if rect.collidepoint(mouse_location_x, mouse_location_y):
                    return BOARD_TILE, i, j, self.board[i][j]

        # check red inventory tiles
        for i in range(3):
            rect = inventory_tiles[RED][i].get_rect()

            if rect.collidepoint(mouse_location_x, mouse_location_y):
                if (self.inventory[RED][i] == 0):
                    return BOARDERS, DONT_CARE, DONT_CARE, DONT_CARE
                return RED_INVENTORY, i, DONT_CARE , self.inventory[RED][i]

        # check blue inventory tiles
        for i in range(3):
            rect = inventory_tiles[BLUE][i].get_rect()

            if rect.collidepoint(mouse_location_x, mouse_location_y):
                if (not self.inventory[BLUE][i]):
                    return BOARDERS, DONT_CARE, DONT_CARE, DONT_CARE
                return BLUE_INVENTORY, i, DONT_CARE , self.inventory[BLUE][i]

        return BOARDERS, DONT_CARE, DONT_CARE, DONT_CARE
    def check_for_draw(self):

        if(len(self.last_red_moves) == 6 and compare_2d_lists(self.last_red_moves[0],self.last_red_moves[2]) and compare_2d_lists(self.last_red_moves[2],self.last_red_moves[4])):
            self.is_draw = True
            draw_state = DrawMenu(self.game, self.mode, self.game.music_player.check_music())
            draw_state.enter_state()

        if(len(self.last_blue_moves) == 6 and compare_2d_lists(self.last_blue_moves[0],self.last_blue_moves[2]) and compare_2d_lists(self.last_blue_moves[2],self.last_blue_moves[4])):
            self.is_draw = True
            draw_state = DrawMenu(self.game, self.mode, self.game.music_player.check_music())
            draw_state.enter_state()

    def switch_turns(self):
        if self.turn == BLUE_TURN:
            self.turn = RED_TURN
            self.last_blue_moves.append([self.source_values,self.destination_values])
            self.turn_text = self.players_names[RED] + ' Turn'
        else:
            self.turn = BLUE_TURN
            self.last_red_moves.append([self.source_values,self.destination_values])
            self.turn_text = self.players_names[BLUE] + ' Turn'
