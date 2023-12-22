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
WHITE_SMALL = 16
WHITE_MEDIUM = 32
WHITE_LARGE = 64
WHITE_XLARGE = 128


class Playing(State):
    def __init__(self, game):
        State.__init__(self, game)
        self.spritesheet = Spritesheet('assets\sprites\sprites.png')
        self.map = TileMap('assets\sprites\map.csv', self.spritesheet)
        self.turn = 1 # player 1 starts the game
        self.players_names = ['Player 1', 'Player 2']
        self.turn_text =  self.players_names[self.turn] + ' Turn'
        self.game_started = False 
        # Initial board (for testing)                                                             
        self.board = [
                    [BLACK_SMALL,BLACK_MEDIUM, BLACK_LARGE,BLACK_XLARGE],
                    [WHITE_SMALL,WHITE_MEDIUM, WHITE_LARGE,WHITE_XLARGE],
                    [BLACK_SMALL,WHITE_SMALL, BLACK_LARGE,EMPTY_TILE],
                    [WHITE_SMALL,EMPTY_TILE,  WHITE_LARGE,EMPTY_TILE]] 

        self.inventory=[
        [15,15,15],   ##inv for black
        [240,240,240] ##inv for white
        ]
    def update(self, delta_time, actions):
        #TODO() add check_wins() here 

        # draw an image only if a new event happens (like mouse movement) or if the game is just launched.
        if len(pygame.event.get()) > 0 or not self.game_started :
            self.map.reconstruct_map(self.board)
            self.map.reconstruct_inventory(self.inventory)
            self.game_started = True
        
        if(actions['Esc']):
           self.exit_state()
    
    def render(self,display):
        display.fill(self.game.BROWN)
        # display a the current turn text on the top of the screen.
        self.helper.draw_text(display,self.turn_text,self.game.WHITE ,20, self.game.DISPLAY_W / 2, 30)

        self.map.draw_map_on_canvas(display)

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

    