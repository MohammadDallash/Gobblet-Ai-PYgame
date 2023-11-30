import pygame


class Helper:
    def __init__(self, game):
        self.game = game
        pass
    def load_assets():
        pass

    def draw_text(self, display, text, color ,size, x, y):
        font = pygame.font.Font(self.game.font_name, size)
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect()
        text_rect.center = (x, y)
        display.blit(text_surface, text_rect)
   
        return text_rect

class MenuGUI():
    def __init__(self, game,options_str, cur_option, font_size, x_pos, justTxt = False):
        self.options_str = options_str
        self.n_options = len(self.options_str)
        self.cur_option = cur_option
        self.font_size = font_size
        self.x_pos = x_pos
        self.game = game
        self.justTxt = justTxt
       

    def update_cur_opt(self, actions):
        if (actions['up'] == True and (not self.justTxt )):   
            self.cur_option = max(0, self.cur_option -1)

        elif (actions['down']== True and (not self.justTxt )):   
            self.cur_option = min(self.n_options-1, self.cur_option +1)

        return self.cur_option

    def render(self, display):
        width_menu = 3*self.font_size*self.n_options - 3*self.font_size
        start_y =  (self.game.DISPLAY_H - width_menu)//2
        darwing_idx = 0

        for options_txt in self.options_str :
            if (darwing_idx == self.cur_option and not self.justTxt ):
                color = self.game.YELLOW
            else:
                color = self.game.WHITE

            self.game.helper.draw_text(display, options_txt, color, self.font_size , self.x_pos, start_y )
            start_y += 3*self.font_size 
            darwing_idx+=1

           
## mouse

## load game background music [music1, music2]

## load game sounds 

## other stuff