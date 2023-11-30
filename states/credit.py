from states.state import State

from util.helpers import MenuGUI


class Credit(State):
    def __init__(self, game):
        State.__init__(self, game)

        self.options_str = ['Leader : Dallash', 'Developer : Rana Hossny', 'Developer : Sara Hossny',]

        self.cur_option = 0

        self.menuGUI = MenuGUI(self.game ,self.options_str, self.cur_option, font_size = 30, x_pos=self.game.DISPLAY_W/2, justTxt = True )

        
       

        
    def update(self, delta_time, actions):
        if(actions['Esc']):
           self.exit_state()
    
            

    def render(self,display):
        display.fill(self.game.BLACK)
        self.helper.draw_text(display,'Credits',self.game.WHITE ,80, self.game.DISPLAY_W / 2, 50)
        self.menuGUI.render(display)

        

        #         # List of contributors
        # contributors = [
        #             ("Leader", "Dallash"),  
        #             ("Developer", "Rana Hossny"),
        #             ("Developer", "Sara Hossny"),          
        #         ]

        # y_position = 100
        # for role, name in contributors:
        #     self.game.helper.draw_text(display,f'{role} : {name}',self.game.WHITE, 15, self.game.DISPLAY_W / 2, y_position)
            
        #     y_position += 20



    def enter_state(self):
        super().enter_state()
        
    def exit_state(self):
        super().exit_state()
        


"""
input :[] list of functions
input :[] list of strings 

"""