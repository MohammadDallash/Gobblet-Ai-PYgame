class Game():
    def __init__(self):
        pass
    def get_dt(self):
        pass
    def update_keyboard_events(self):
        pass
    def update_mouse_events(self):
        pass
    def update_cur_state(self):
        pass
        
    def game_loop(self):
        while self.playing:
                self.get_dt()
                self.update_keyboard_events()
                self.update_mouse_events()
                self.update_cur_state()
                self.render_cur_state()
                
    def render_cur_state(self):
       pass
   
   
   
if __name__ == "__main__":
    g = Game()
    while g.running:
        g.game_loop()
        
        
#any other fuctions like draw_text or load_assets  or ....etc 
#   put them on the Util/helpers.py