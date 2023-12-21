from states.state import State
from util.sprite import Spritesheet
from util.tile import TileMap
import pygame

# pieces for each color.
EMPTY_TILE = -1
BLACK_SMALL = 0
BLACK_MEDIUM = 2
BLACK_LARGE = 4
WHITE_SMALL = 1
WHITE_MEDIUM = 3
WHITE_LARGE = 5


class Playing(State):
    def __init__(self, game):
        State.__init__(self, game)
        self.spritesheet = Spritesheet('assets\sprites\sprites.png')
        self.map = TileMap('assets\sprites\map.csv', self.spritesheet)
        self.turn = 1 # player 1 starts the game
        self.players_names = ['Player 1', 'Player 2']
        self.turn_text =  self.players_names[self.turn] + ' Turn' 
        # Initial board (for testing)                                                             
        self.board = [
                    [BLACK_LARGE,WHITE_SMALL, BLACK_LARGE,EMPTY_TILE],
                    [EMPTY_TILE, WHITE_MEDIUM,BLACK_LARGE,EMPTY_TILE],
                    [BLACK_SMALL,WHITE_SMALL, BLACK_LARGE,EMPTY_TILE],
                    [WHITE_SMALL,EMPTY_TILE,  WHITE_LARGE,EMPTY_TILE]] 

    def update(self, delta_time, actions):
        # draw an image only if a new event happens (like mouse movement).
        if len(pygame.event.get())>0:
            self.map.reconstruct_map(self.board)
        
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
