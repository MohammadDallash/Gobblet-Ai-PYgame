from states.state import State
from util.sprite import Spritesheet



class Playing(State):
    def __init__(self, game):
        State.__init__(self, game)
        self.spritesheet = Spritesheet('assets\sprites\sprites.png')




        
       

        
    def update(self, delta_time, actions):
        if(actions['Esc']):
           self.exit_state()
    
            

    def render(self,display):
        display.fill(self.game.BROWN)
        self.helper.draw_text(display,'playing',self.game.WHITE ,20, self.game.DISPLAY_W / 2, 30)




    def enter_state(self):
        super().enter_state()
        
    def exit_state(self):
        super().exit_state()
        


"""
input :[] list of functions
input :[] list of strings 

"""