from states.state import State
from util.sprite import Spritesheet
from util.tile import TileMap



class Playing(State):
    def __init__(self, game):
        State.__init__(self, game)
        self.spritesheet = Spritesheet('assets\sprites\sprites.png')
        self.map = TileMap('assets\sprites\map.csv', self.spritesheet)
        self.turn = 1
        self.players_names = ['player1', 'player2']
        self.turn_text =  self.players_names[self.turn] + ' Turn'




        
       

        
    def update(self, delta_time, actions):
        if(actions['Esc']):
           self.exit_state()
    
            

    def render(self,display):
        display.fill(self.game.BROWN)
        self.helper.draw_text(display,self.turn_text,self.game.WHITE ,20, self.game.DISPLAY_W / 2, 30)
        self.map.draw_map(display)




    def enter_state(self):
        super().enter_state()
        
    def exit_state(self):
        super().exit_state()
