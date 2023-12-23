from states.state import State
from util.sprite import Spritesheet
from util.tile import TileMap
import pygame
from util.helpers import *

# pieces for each color.
EMPTY_TILE = -1
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


class Playing(State):
    def __init__(self, game):
        State.__init__(self, game)
        self.spritesheet = Spritesheet('assets\sprites\sprites.png')
        self.map = TileMap('assets\sprites\map.csv', self.spritesheet)
        self.turn = 1 # player 1 starts the game
        self.players_names = ['Player 1', 'Player 2']
        self.turn_text =  self.players_names[self.turn] + ' Turn'
        self.game_started = False 
        self.mouse_is_pressed = False
        self.selected_tile = None  # Stores (inventory_row, tile_value)
        self.selected_tile_original_pos = None  # Stores original position in inventory
        self.result = None
        self.mouse_pos = (0, 0)
        self.selected_shape=False
        self.highlighted_tile_rect = None
        # Initial board (for testing)                                                             
        self.board = [
                    [EMPTY_TILE,BLACK_MEDIUM, BLACK_LARGE,BLACK_XLARGE],
                    [WHITE_SMALL,WHITE_MEDIUM, WHITE_LARGE,WHITE_XLARGE],
                    [BLACK_SMALL,WHITE_SMALL, BLACK_LARGE,EMPTY_TILE],
                    [WHITE_SMALL,EMPTY_TILE,  WHITE_LARGE,EMPTY_TILE]] 
        self.inventory=[
        [ALL_BLACK,ALL_BLACK,ALL_BLACK],   ##inv for black
        [ALL_WHITE,ALL_WHITE,ALL_WHITE] ##inv for white
        ]
        self.map.reconstruct_map(self.board)
    def update(self, delta_time, actions):
        #TODO() add check_wins() here 
        # draw an image only if a new event happens (like mouse movement) or if the game is just launched.
        self.mouse_pos = pygame.mouse.get_pos()
        if len(pygame.event.get()) > 0 or not self.game_started :
            self.map.reconstruct_map(self.board)
            self.result=self.map.reconstruct_inventory(self.inventory)
            self.game_started = True
        if actions['LEFT_MOUSE_KEY_PRESS']:
                self.handle_mouse_click(pygame.mouse.get_pos())
                self.map.reconstruct_map(self.board)
                self.result=self.map.reconstruct_inventory(self.inventory)    
        if not actions['LEFT_MOUSE_KEY_PRESS'] and self.selected_tile:
            self.handle_mouse_release(pygame.mouse.get_pos())
            self.map.reconstruct_map(self.board)
            self.result=self.map.reconstruct_inventory(self.inventory)    
            
        if(actions['Esc']):
           self.exit_state()

    def handle_mouse_click(self, pos):
        if self.is_click_on_inventory(pos) and not self.selected_shape:
            self.selected_shape = True
            self.handle_inventory_click(pos)
        elif self.selected_shape :
            self.near_from_board(pos)
            
            
        
    def is_click_on_inventory(self, pos):
        for tile_list in self.result:  
            for tile in tile_list:
                if tile.rect.collidepoint(pos):
                    return True
        return False
    def near_from_board(self, pos):
        for row in self.map.tiles_board_positions:
            for tile_info in row:
                tile_rect = pygame.Rect(tile_info['x'], tile_info['y'], tile_info['width'], tile_info['height'])
                if tile_rect.collidepoint(pos):
                    # Store the rectangle information instead of drawing
                    self.highlighted_tile_rect = tile_rect
                    return
        self.highlighted_tile_rect = None  # Reset if no tile is highlighted   

    def handle_inventory_click(self, pos):
        # Step 1: Determine which inventory tile and player's inventory is clicked
        clicked_inventory = None
        player = None
        for i, tile_list in enumerate(self.result):  # Assuming result contains inventory tiles
            for j, tile in enumerate(tile_list):
                if tile.rect.collidepoint(pos):
                    clicked_inventory = (j, i)
                    player = i  # 0 for black, 1 for white
                    inventory_num=j
                    break
            if clicked_inventory is not None:
                break

        # Check if a valid inventory tile was clicked
        if clicked_inventory is None:
            return

        # Step 2 and 3: Find and pick the largest piece
        player_inventory = self.inventory[player]
        largest_piece, updated_inventory = self.get_largest_piece(player_inventory[inventory_num])
        # Step 4: Update the inventory and set the selected piece
        self.inventory[player][inventory_num] = updated_inventory
    
        self.selected_tile = (player, largest_piece)
        self.selected_tile_original_pos = clicked_inventory

    def get_largest_piece(self, inventory_value):
        # Masks for black and white pieces
        masks = [8, 4, 2, 1, 128, 64, 32, 16]

        # Find the largest piece
        for mask in masks:
            if inventory_value & mask:
                # Remove the largest piece from the inventory
                return mask, inventory_value - mask

        return None, inventory_value
    def handle_mouse_release(self,pos):
        for row_idx, row in enumerate(self.map.tiles_board_positions):
            for col_idx, tile_info in enumerate(row):
                tile_rect = pygame.Rect(tile_info['x'], tile_info['y'], tile_info['width'], tile_info['height'])
                if tile_rect.collidepoint(pos):
                    
                    # Update the board with the selected tile value
                    if self.selected_tile:  # Ensure a tile is selected
                        self.board[row_idx][col_idx] = self.selected_tile[1]
                        self.selected_shape = False
                        self.selected_tile = None
                        self.highlighted_tile_rect = None
                        return
                        


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
                # if the current piece is black then increment black by 1.
                print() # to stop error (remove it)
            # reset counters.
            black = 0
            white = 0

        for i in range(4):
            # check if the column has 4 pieces of the same color.
            for j in range(4):
                # if the current piece is white then increment white by 1.
                # if the current piece is black then increment black by 1.
                print() # to stop error (remove it)
            # reset counters.
            black = 0
            white = 0
        
        #check if the diagonals has 4 pieces of the same color.
        for i in range(4):
            print() # to stop error (remove it)

    