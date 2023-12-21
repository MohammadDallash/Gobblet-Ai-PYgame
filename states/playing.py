from states.state import State
from util.sprite import Spritesheet
from util.tile import TileMap



class Playing(State):
    def __init__(self, game):
        State.__init__(self, game)
        self.spritesheet = Spritesheet('assets\sprites\sprites.png')
        self.map = TileMap('assets\sprites\map.csv', self.spritesheet)
        self.turn = 1
        self.players_names = ['player 1', 'player 2']
        self.turn_text =  self.players_names[self.turn] + ' Turn'
                                                                       ## 1 3 5
        self.board = [[2,1,4,-1],[-1,3,4,-1], [0,1,4,-1],[1,-1,5,-1]] ## 0 2 4 for sizes and odd even for black, white




        
       

        
    def update(self, delta_time, actions):
        self.map.reconstruct_map(self.board)

        if(actions['Esc']):
           self.exit_state()
    
            

    def render(self,display):
        display.fill(self.game.BROWN)
        self.helper.draw_text(display,self.turn_text,self.game.WHITE ,20, self.game.DISPLAY_W / 2, 30)
        self.map.draw_map_on_canvis(display)




    def enter_state(self):
        super().enter_state()
        
    def exit_state(self):
        super().exit_state()
