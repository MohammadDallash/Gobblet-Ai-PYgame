from states.pauseMenu import PauseMenu
from states.state import State
from util.sprite import Spritesheet
from util.tile import TileMap
import pygame
from util.helpers import *
import time

# pieces for each color.
EMPTY_TILE = 0
BLACK_SMALL = 1
BLACK_MEDIUM = 2
BLACK_LARGE = 4
BLACK_XLARGE = 8
ALL_BLACK = 15

WHITE_SMALL = 16
WHITE_MEDIUM = 32
WHITE_LARGE = 64
WHITE_XLARGE = 128
ALL_WHITE = 240

BLACK, WHITE= 0 , 1


BLACK_INVENTORY = "black"
WHITE_INVENTORY = "white"
BOARD_TILE = "board"
BOARDERS = "empty"



class Playing(State):
    def __init__(self, game):
        State.__init__(self, game)
        self.spritesheet = Spritesheet('assets/sprites/sprites.png')
        self.map = TileMap('assets/sprites/map.csv', self.spritesheet)
        self.turn = 1 # player 1 starts the game
        self.players_names = ['Player 1', 'Player 2']
        self.turn_text =  self.players_names[self.turn] + ' Turn'
        self.game_started = False 
        self.mouse_is_pressed = False
        self.selected_tile = None  # Stores (inventory_row, tile_value)
        self.selected_tile_original_pos = None  # Stores original position in inventory
        self.inventory_tiles = None
        self.mouse_pos = (0, 0)
        self.shape_held=False

        self.board_tiles = [[],[],[],[]]



        self.highlighted_tile_rect = None
        self.x = 0

        self.source_selected = False # stores whether the source piece is selected
        self.source_values = []

        # Initial board (for testing)                                                             
        self.board = [
                    [EMPTY_TILE,EMPTY_TILE, EMPTY_TILE,EMPTY_TILE],
                    [EMPTY_TILE,EMPTY_TILE, EMPTY_TILE,EMPTY_TILE],
                    [EMPTY_TILE,EMPTY_TILE, EMPTY_TILE,EMPTY_TILE],
                    [EMPTY_TILE,EMPTY_TILE, EMPTY_TILE,EMPTY_TILE]] 
        self.inventory=[
        [ALL_BLACK,ALL_BLACK,ALL_BLACK],##inv for black
        [ALL_WHITE,ALL_WHITE,ALL_WHITE] ##inv for white
        ]


        self.map.reconstruct_map(self.board)

    def update(self, delta_time, actions):
        #self.check_wins()
        # draw an image only if a new event happens (like mouse movement) or if the game is just launched.
        self.mouse_pos = pygame.mouse.get_pos()


        self.board_tiles = self.map.reconstruct_map(self.board)
        self.inventory_tiles = self.map.reconstruct_inventory(self.inventory)


        self.game_started = True

            # self.helper.flush_to_file(self.turn, self.board,self.inventory)
            # print(self.helper.cpp_code("current_state_file.txt"))
            
        if actions['LEFT_MOUSE_KEY_PRESS']:
                self.handle_mouse_click()
                time.sleep(0.15)
    
        # if not actions['LEFT_MOUSE_KEY_PRESS'] and self.selected_tile:
        #     self.place_piece(pygame.mouse.get_pos())
        #     self.map.reconstruct_map(self.board)
        #     self.inventory_tiles=self.map.reconstruct_inventory(self.inventory)    
            
        if(actions['Esc']):
            pause_menu = PauseMenu(self.game)
            pause_menu.enter_state()

    def handle_mouse_click(self):
        location,i,j, state = self.get_clicked_tile_id(self.board_tiles,self.inventory_tiles)
        self.move_piece(location, i , j, state)


        # if location !='empty':
        #     self.shape_held = True


        # elif self.shape_held :
        #     self.highlight_nearest_tile(pos)
            
            
        
    # # checks if the held piece is near a board tile and highlight that tile.
    # def highlight_nearest_tile(self, pos):
    #     for row in self.board_tiles:
    #         for tile in row:

    #             tile_rect = tile.get_rect()

    #             if tile_rect.collidepoint(pos):
    #                 # Store the rectangle information instead of drawing
    #                 self.highlighted_tile_rect = tile_rect
    #                 return
    #     self.highlighted_tile_rect = None  # Reset if no tile is highlighted   



    def move_piece(self, location , i , j , state):
        
        # if the source is in the boarders, ignore it.
        if(location==BOARDERS):
            return
        
        # if the source is an empty tile
        if(not self.source_selected and location == BOARD_TILE and state == EMPTY_TILE):
            print("cannot move an empty tile ")
            return
        
        # if the source is the same as the destenation.
        elif(self.source_selected and [location,i,j] == self.source_values):
            print("cannot make move from a place to the same place ")
            return
        
        # if the destenation is the inventory.
        elif(self.source_selected and (location==BLACK_INVENTORY or location==WHITE_INVENTORY)):
            print("cannot make move to inventory")
            return
        

        # if source is not selected.
        elif(not self.source_selected):
            # save source values.
            self.source_values = [location, i , j]
            self.source_selected = True


        else:
            # load source values into a variable for better readability (Note: current function parameters are destenation).
            source_location, source_i , source_j = self.source_values
            val_dst = self.board[i][j]
            self.source_selected = False


            # if the source is an inventory.
            if(source_location==BLACK_INVENTORY):

                # get the value of the source location (Black Inventory)
                val_src = self.inventory[BLACK][source_i]

                # get the largest piece in that place
                largest_piece_in_source = get_largest_piece(val_src)

                # check the largest piece in both sides after being unified, if the move is valid, go ahead with it.
                if(is_move_valid(val_src,val_dst)):

                    self.inventory[0][source_i] &= ~(largest_piece_in_source)
                    self.board[i][j] |= largest_piece_in_source

                else:
                    return
                

            elif(source_location == WHITE_INVENTORY): 

                # get the value of the source location (White Inventory)
                val_src = self.inventory[WHITE][source_i]

                # get the largest piece in that place
                largest_piece_in_source = get_largest_piece(val_src)

                # check the largest piece in both sides after being unified, if the move is valid, go ahead with it.
                if(is_move_valid(val_src,val_dst)):
                    self.inventory[1][source_i] &= ~(largest_piece_in_source)
                    self.board[i][j] |= largest_piece_in_source
                else:
                    return
                    

            # if the source is a board.
            elif(source_location == BOARD_TILE):

                # get the value of the source location (board)
                val_src = self.board[source_i][source_j]
                # get the largest piece in that place
                largest_piece_in_source = get_largest_piece(val_src)

                if(is_move_valid(val_src,val_dst)):
                    self.board[source_i][source_j]  &= ~(largest_piece_in_source)
                    self.board[i][j] |= largest_piece_in_source
                else:
                        return

            

    # # place held piece on board.
    # def place_piece(self,pos):

    #     # iterate the board tile by tile.
    #     for i, row in enumerate(self.board_tiles):
    #         for j, tile in enumerate(row):
                
    #             # get rect -haha- object (used to check if the tile is pressesd).
    #             tile_rect = tile.get_rect()

    #             # if the rectangle is pressed
    #             if tile_rect.collidepoint(pos):

    #                 # Update the board with the selected tile value
    #                 if self.selected_tile:  # Ensure a tile is selected

    #                     self.board[i][j] |= self.selected_tile[1] # TODO() TBD: needs to be fixed by checking if the move is valid.

    #                     self.shape_held = False
    #                     self.selected_tile = None
    #                     self.highlighted_tile_rect = None
    #                     return
    


    def render(self, display):
        # Step 1: Clear the screen
        display.fill(self.game.BROWN)

        # Step 2: Draw game elements
        # Display the current turn text at the top of the screen
        self.helper.draw_text(display, self.turn_text, self.game.WHITE, 20, self.game.DISPLAY_W / 2, 30)
        self.map.draw_map_on_canvas(display)
        if self.highlighted_tile_rect:
            pygame.draw.rect(display, (128, 0, 128), self.highlighted_tile_rect)
        
        if self.selected_tile:
            self.map.selected_tile(self.selected_tile, self.mouse_pos).draw(display)
        

        # Step 4: Update the display
        pygame.display.flip()  # or pygame.display.update()


    def enter_state(self):
        super().enter_state()
        
    def exit_state(self):
        super().exit_state()



    # TODO() TBD after fixing piece sizes
    # checks for a winner at the beginning of each round.
    def check_wins(self):
        # create 3 loops that checks for a winner in each row, column, diagonal.
        black = 0
        white = 0
        for i in range(4):
            # check if the row has 4 pieces of the same color.
            for j in range(4):
                # if the current piece is white then increment white by 1.
                if self.board[i][j] > 15 and not self.board[i][j] == EMPTY_TILE:
                    white+=1
                # if the current piece is black then increment black by 1.
                elif self.board[i][j] < 16 and not self.board[i][j] == EMPTY_TILE:
                    black+=1

            if white == 4:
                print("white wins")
            elif black == 4:
                print("black wins")
            # reset counters.
            black = 0
            white = 0

        for i in range(4):
            # check if the column has 4 pieces of the same color.
            for j in range(4):
                # if the current piece is white then increment white by 1.
                if self.board[j][i] > 15 and not self.board[i][j] == EMPTY_TILE:
                    white+=1
                # if the current piece is black then increment black by 1.
                elif self.board[i][j] < 16 and not self.board[i][j] == EMPTY_TILE:
                    black+=1

            if white == 4:
                print("white wins")
            elif black == 4:
                print("black wins")

            # reset counters.
            black = 0
            white = 0
        
        #main diagonal
        for i in range(4):
                if self.board[i][i] > 15 and not self.board[i][i] == EMPTY_TILE:
                    white+=1

                elif self.board[i][i] < 16 and not self.board[i][i] == EMPTY_TILE:
                    black+=1

        if white == 4:
            print("white wins")
        elif black == 4:
            print("black wins")


        black = 0
        white = 0

        #other diagonal
        for i in range(4):
                if self.board[i][3-i] > 15 and not self.board[i][3-i] ==EMPTY_TILE:
                    white+=1

                elif self.board[i][3-i] < 16 and not self.board[i][3-i] == EMPTY_TILE:
                    black+=1

        if white == 4:
            print("white wins")
        elif black == 4:
            print("black wins")



    # check if the mouse click is within a certain tile and returns its position.
    def get_clicked_tile_id(self, board_tiles, inventory_tiles):

        mouse_location_x, mouse_location_y = pygame.mouse.get_pos()

        # check board tiles.
        for i in range(4):
            for j in range(4):
                rect = board_tiles[i][j].get_rect()
                if rect.collidepoint(mouse_location_x, mouse_location_y):
                    return BOARD_TILE, i, j ,self.board[i][j]

        # check white inventory tiles
        for i in range(3):
            rect = inventory_tiles[1][i].get_rect()

            if rect.collidepoint(mouse_location_x, mouse_location_y):
                if(self.inventory[WHITE][i]==0):
                    return BOARDERS, -1, -1 , -1
                return WHITE_INVENTORY, i , "anything invalid" , self.inventory[WHITE][i]

        # check black inventory tiles
        for i in range(3):
            rect = inventory_tiles[0][i].get_rect()

            if rect.collidepoint(mouse_location_x, mouse_location_y):
                if(not self.inventory[BLACK][i]):
                    return BOARDERS, -1, -1 , -1
                return BLACK_INVENTORY, i , "anything invalid" , self.inventory[BLACK][i]
            
        return BOARDERS, -1, -1 , -1
    
