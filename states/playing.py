from collections import deque
from states.pauseMenu import PauseMenu
from states.state import State
from states.winnerMenu import WinnerMenu
from util.sprite import Spritesheet
from util.tile import TileMap
import pygame
from util.helpers import *
import time
import socket




# pieces for each color.
EMPTY_TILE = 0

BLACK_SMALL,BLACK_MEDIUM,BLACK_LARGE,BLACK_XLARGE, ALL_BLACK  = 1,2,4,8,15
WHITE_SMALL,WHITE_MEDIUM,WHITE_LARGE,WHITE_XLARGE, ALL_WHITE  = 16,32,64,128,240
BLACK, WHITE = 0, 1

# SRC OR DEST (CLICK_LOCATION , i , j)


BLACK_INVENTORY,WHITE_INVENTORY = "black" ,"white"

BOARD_TILE = "board"

BOARDERS = "empty"
DONT_CARE = "anything invalid"
BLACK_TURN = BLACK_PLAYER =  1
WHITE_TURN = WHITE_PLAYER =  2

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
        self.turn = BLACK_PLAYER  # BLACK starts the game
        self.players_names = ['Player 1', 'Player 2']
        self.turn_text = self.players_names[self.turn - 1] + ' Turn'
        self.inventory_tiles = None
        self.board_tiles = [[], [], [], []]
        self.highlighted_tile_rect = None 
        self.source_selected = False  # stores whether the source piece is selected
        self.server = None
        self.client = None

        self.source_values = [] # stores source values


        
        self.source_values = [] # stores source values
        self.destination_values = [] # stores dest values


        self.last_white_moves = []
        self.last_white_moves = deque(self.last_white_moves)


        self.last_black_moves = []
        self.last_black_moves = deque(self.last_black_moves)

        self.is_draw = False

        ################################
        self.mode = PLAYER_VS_PLAYER
        ################################
        self.game_started = False


        # Initial board                                                          
        self.board = [
            [EMPTY_TILE, EMPTY_TILE, EMPTY_TILE, EMPTY_TILE],
            [EMPTY_TILE, EMPTY_TILE, EMPTY_TILE, EMPTY_TILE],
            [EMPTY_TILE, EMPTY_TILE, EMPTY_TILE, EMPTY_TILE],
            [EMPTY_TILE, EMPTY_TILE, EMPTY_TILE, EMPTY_TILE]]
        
        self.inventory = [
            [ALL_BLACK, ALL_BLACK, ALL_BLACK], # inv for black
            [ALL_WHITE, ALL_WHITE, ALL_WHITE]  # inv for white
        ]

        self.map.reconstruct_map(self.board)

        self.game_started = False

        if(self.mode==MULTIPLAYER_SERVER):
            self.host_game()

        elif(self.mode==MULTIPLAYER_CLIENT):
            self.connect_to_game()


    def parse_input_string(self,input_string):
        # Convert the input string to a numeric array
        if input_string :
            numeric_array = [int(num) for num in input_string.split()]
            src = numeric_array[0:3]
            dst = numeric_array[3:6]

            if(src[0]==INVENTORY_MOVE):
                largest_piece_src = get_largest_piece(self.inventory[src[1]][src[2]])
                self.board[dst[1]][dst[2]] |= largest_piece_src
                self.inventory[src[1]][src[2]] &= ~largest_piece_src

            elif(src[0]==BOARD_MOVE):
                largest_piece_src = get_largest_piece(self.board[src[1]][src[2]])
                self.board[dst[1]][dst[2]] |=  largest_piece_src
                self.board[src[1]][src[2]] &= ~largest_piece_src
                
            self.turn = WHITE_PLAYER if(self.turn==BLACK_PLAYER)  else BLACK_PLAYER
    
    def update(self, delta_time, actions):

        self.board_tiles = self.map.reconstruct_map(self.board)
        self.inventory_tiles = self.map.reconstruct_inventory(self.inventory)

        self.highlight_nearest_tile(pygame.mouse.get_pos())
        
        self.handle_mode_operations()
        self.check_for_draw()
        self.check_wins()


        if(self.mode != AI_VS_AI):
            if actions['LEFT_MOUSE_KEY_PRESS']:
                time.sleep(0.1)
                self.handle_mouse_click()

        if actions['Esc']:
            pause_menu = PauseMenu(self.game)
            pause_menu.enter_state()


    def handle_mode_operations(self):
        
        if(self.mode == AI_VS_AI):
            self.helper.flush_to_file(self.turn-1, self.board,self.inventory)
            s = (self.helper.cpp_code("current_state_file.txt"))
            self.parse_input_string(s)



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
        elif (self.source_selected and (location == BLACK_INVENTORY or location == WHITE_INVENTORY)):
            return

        # if selected from inventory is black and it's white turn
        elif location == BLACK_INVENTORY and self.turn == WHITE_TURN:
            return

        # if selected from inventory is white and it's black turn
        elif location == WHITE_INVENTORY and self.turn == BLACK_TURN:
            return
        
        
        # if source is not selected.
        if (not self.source_selected):
            # save source values.
            self.source_values = [location, i, j]
            self.source_selected = True
            return
        else:
            self.destination_values = [location,i,j]

        if(self.mode == PLAYER_VS_PLAYER):
            move = [self.source_values,self.destination_values]
            self.move_piece(move)
            self.source_values = []
            self.destination_values = []
        elif(self.mode == MULTIPLAYER_CLIENT):
            pass
        elif(self.mode == MULTIPLAYER_SERVER):
            pass


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

        # piece selected is black in white's turn or white in black's turn.
        if (source_location == BOARD_TILE):
            if get_largest_piece(self.board[source_i][source_j]) in [BLACK_SMALL, BLACK_MEDIUM, BLACK_LARGE,BLACK_XLARGE] and self.turn == WHITE_TURN:
                return

            if get_largest_piece(self.board[source_i][source_j]) in [WHITE_SMALL, WHITE_MEDIUM, WHITE_LARGE,WHITE_XLARGE] and self.turn == BLACK_TURN:
                return

        # if the source is an inventory.
        if source_location == BLACK_INVENTORY:

            # get the value of the source location (Black Inventory)
            val_src = self.inventory[BLACK][source_i]

            # get the largest piece in that place
            largest_piece_in_source = get_largest_piece(val_src)

            # if the move is valid, if the move is valid, go ahead with it.
            if is_move_valid(val_src, val_dst):

                self.inventory[BLACK][source_i] &= ~(largest_piece_in_source)
                self.board[dst_i][dst_j] |= largest_piece_in_source
                self.switch_turns()

            else:
                return

        elif (source_location == WHITE_INVENTORY):

            # get the value of the source location (White Inventory).
            val_src = self.inventory[WHITE][source_i]

            # get the largest piece in that place.
            largest_piece_in_source = get_largest_piece(val_src)

            # if the move is valid, if the move is valid, go ahead with it.
            if (is_move_valid(val_src, val_dst)):
                self.inventory[WHITE][source_i] &= ~(largest_piece_in_source)
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
        display.fill(self.game.BROWN)

        # Step 2: Draw game elements
        # Display the current turn text at the top of the screen
        self.helper.draw_text(display, self.turn_text, self.game.WHITE, 20, self.game.DISPLAY_W / 2, 30)
        self.map.draw_map_on_canvas(display)

        # if the mouse is near a certain tile.
        if self.highlighted_tile_rect:
            s = pygame.Surface((TILE_WIDTH-10,TILE_HEIGHT-10))  # create a surface with these dimensions
            s.set_alpha(64)  # alpha level (opacity)
            s.fill((255,255,255)) # set color to white
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
                if not (largest_piece_in_source>ALL_BLACK and self.turn==WHITE_TURN) and not(largest_piece_in_source<ALL_BLACK and self.turn==BLACK_TURN):
                    return
                    
            # only allow drawing if the source is the black inventory, and it's the black turn.       
            elif(source_location==BLACK_INVENTORY and self.turn == BLACK_TURN):
                largest_piece_in_source = get_largest_piece(self.inventory[BLACK][source_i])

             
            # only allow drawing if the source is the white inventory, and it's the white turn.    
            elif(source_location==WHITE_INVENTORY and self.turn == WHITE_TURN):
                largest_piece_in_source = get_largest_piece(self.inventory[WHITE][source_i])

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
    def check_wins(self):
        # create 3 loops that checks for a winner in each row, column, diagonal.
        black = 0
        white = 0
        for i in range(4):
            # check if the row has 4 pieces of the same color.
            for j in range(4):
                # if the current piece is white then increment white by 1.
                if get_largest_piece(self.board[i][j]) > ALL_BLACK and not self.board[i][j] == EMPTY_TILE:
                    white += 1
                # if the current piece is black then increment black by 1.
                elif get_largest_piece(self.board[i][j]) < WHITE_SMALL and not self.board[i][j] == EMPTY_TILE:
                    black += 1

            if white == 4:
                winner_state = WinnerMenu(self.game, WHITE_PLAYER)
                # time.sleep(3)
                winner_state.enter_state()
            elif black == 4:
                winner_state = WinnerMenu(self.game, BLACK_PLAYER)
                # time.sleep(3)
                winner_state.enter_state()
            # reset counters.
            black = 0
            white = 0

        for i in range(4):
            # check if the column has 4 pieces of the same color.
            for j in range(4):
                # if the current piece is white then increment white by 1.
                if get_largest_piece(self.board[j][i]) > ALL_BLACK and not self.board[j][i] == EMPTY_TILE:
                    white += 1
                # if the current piece is black then increment black by 1.
                elif get_largest_piece(self.board[j][i]) < WHITE_SMALL and not self.board[j][i] == EMPTY_TILE:
                    black += 1

            if white == 4:
                winner_state = WinnerMenu(self.game, WHITE_PLAYER)
                # time.sleep(3)
                winner_state.enter_state()

            elif black == 4:
                winner_state = WinnerMenu(self.game, BLACK_PLAYER)
                # time.sleep(3)
                winner_state.enter_state()

            # reset counters.
            black = 0
            white = 0

        # main diagonal
        for i in range(4):
            if get_largest_piece(self.board[i][i]) > ALL_BLACK and not self.board[i][i] == EMPTY_TILE:
                white += 1

            elif get_largest_piece(self.board[i][i]) < WHITE_SMALL and not self.board[i][i] == EMPTY_TILE:
                black += 1

        if white == 4:
            winner_state = WinnerMenu(self.game, WHITE_PLAYER)
            # time.sleep(3)
            winner_state.enter_state()
        elif black == 4:
            winner_state = WinnerMenu(self.game, BLACK_PLAYER)
            # time.sleep(3)
            winner_state.enter_state()

        black = 0
        white = 0

        # other diagonal
        for i in range(4):
            if get_largest_piece(self.board[i][3-i]) > ALL_BLACK and not self.board[i][3 - i] == EMPTY_TILE:
                white += 1

            elif get_largest_piece(self.board[i][3-i]) < WHITE_SMALL and not self.board[i][3 - i] == EMPTY_TILE:
                black += 1

        if white == 4:
            winner_state = WinnerMenu(self.game, WHITE_PLAYER)
            # time.sleep(3)
            winner_state.enter_state()

        elif black == 4:
            winner_state = WinnerMenu(self.game, BLACK_PLAYER)
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

        # check white inventory tiles
        for i in range(3):
            rect = inventory_tiles[WHITE][i].get_rect()

            if rect.collidepoint(mouse_location_x, mouse_location_y):
                if (self.inventory[WHITE][i] == 0):
                    return BOARDERS, DONT_CARE, DONT_CARE, DONT_CARE
                return WHITE_INVENTORY, i, DONT_CARE , self.inventory[WHITE][i]

        # check black inventory tiles
        for i in range(3):
            rect = inventory_tiles[BLACK][i].get_rect()

            if rect.collidepoint(mouse_location_x, mouse_location_y):
                if (not self.inventory[BLACK][i]):
                    return BOARDERS, DONT_CARE, DONT_CARE, DONT_CARE
                return BLACK_INVENTORY, i, DONT_CARE , self.inventory[BLACK][i]

        return BOARDERS, DONT_CARE, DONT_CARE, DONT_CARE
    


    def check_for_draw(self):

        if(len(self.last_white_moves) == 6 and compare_2d_lists(self.last_white_moves[0],self.last_white_moves[2]) and compare_2d_lists(self.last_white_moves[2],self.last_white_moves[4])):
            self.is_draw = True

        if(len(self.last_black_moves) == 6 and compare_2d_lists(self.last_black_moves[0],self.last_black_moves[2]) and compare_2d_lists(self.last_black_moves[2],self.last_black_moves[4])):
            self.is_draw = True

        if(len(self.last_black_moves) > 6):
            self.last_black_moves.popleft()


        if(len(self.last_white_moves) > 6):
            self.last_white_moves.popleft()


    def host_game(self,host='localhost',port=9999):
        self.server = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        self.server.bind((host,port))
        self.server.listen(1)




    def connect_to_game(self,host='localhost',port=9999):
        self.client = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        self.client.connect((host,port))

    def switch_turns(self):
        if self.turn == BLACK_TURN:
            self.turn = WHITE_TURN
            self.last_black_moves.append([self.source_values,self.destination_values])
            self.turn_text = self.players_names[WHITE] + ' Turn'
        else:
            self.turn = BLACK_TURN
            self.last_white_moves.append([self.source_values,self.destination_values])
            self.turn_text = self.players_names[BLACK] + ' Turn'
        
            