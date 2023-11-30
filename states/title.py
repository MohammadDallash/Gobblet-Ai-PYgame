from states.state import State
from states.credit import Credit
from util.helpers import MenuGUI



class Title(State):
    def __init__(self, game):
        State.__init__(self, game)
        
   
        self.options_str = ['Play', 'options', 'credit' ,'quit']

        self.cur_option = 0

        self.menuGUI = MenuGUI(self.game ,self.options_str, self.cur_option, font_size = 30, x_pos=self.game.DISPLAY_W/2)
        

        
    def update(self, delta_time, actions):
        self.cur_option = self.menuGUI.update_cur_opt(actions)

        if(actions['enter']):
            if (self.cur_option == 0):
                ## enter play state
                pass
            elif (self.cur_option == 1):
                ## enter options state
                pass
            elif (self.cur_option == 2):
                credit_state = Credit(self.game)
                ##self.exit_state()## if we want to exit the tile state we woul un comment this but we want to keep them as we want to retrun back to them
                credit_state.enter_state()
                
                ## enter credit state

                pass
            else:
                self.game.running = False
        
        if (actions['Esc']):
            self.game.running = False
    

        
            

    def render(self,display):
        display.fill(self.game.BLACK)
        self.menuGUI.render(display)


    def enter_state(self):
        super().enter_state()
        
    def exit_state(self):
        super().exit_state()
        


"""
input :[] list of functions
input :[] list of strings 

"""