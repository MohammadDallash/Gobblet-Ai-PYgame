import pygame


# get the value of the highest bit in the number.
# Ex. n = 64 + 32 , get_highest_bit(n) = 64
# returns 0 if n=0
def get_highest_bit(n):
    if(n==0):
        return 0
    bit = 0
    n = int(n/2)
    while(n!=0):
        n = n >> 1
        bit+=1
    return 1 << bit


# @param src,dst -> the source, destenation tiles. 
# this function checks if a move is allowed from one tile to another.
def is_valid_move(board, src, dst):
    val_src = board[src[0]][src[1]]
    val_dst = board[dst[0]][dst[1]]
    if(get_highest_bit(val_dst) < get_highest_bit(val_src)):
        return True
    else:
        return False



class Helper:
    def __init__(self, game):
        self.game = game

    def load_assets(self):
        pass

    def draw_text(self, display, text, color, size, x, y):
        font = pygame.font.Font(self.game.font_name, size)
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect()
        text_rect.center = (x, y)
        display.blit(text_surface, text_rect)

        return text_rect
    


class MenuGUI:
    def __init__(self, game, options_str, cur_option, font_size, x_pos, justTxt=False):
        self.options_str = options_str
        self.n_options = len(self.options_str)
        self.cur_option = cur_option
        self.font_size = font_size
        self.x_pos = x_pos
        self.game = game
        self.justTxt = justTxt
        self.rec = []
        self.display = None

    def update_cur_opt(self, actions):
        if actions['up'] and (not self.justTxt):
            self.cur_option = max(0, self.cur_option - 1)
        elif actions['down'] and (not self.justTxt):
            self.cur_option = min(self.n_options - 1, self.cur_option + 1)
        return self.cur_option
    

    def render(self, display):
        self.display = display
        width_menu = 3 * self.font_size * self.n_options - 3 * self.font_size
        start_y = (self.game.DISPLAY_H - width_menu) // 2
        for idx, options_txt in enumerate(self.options_str):
            color = self.game.YELLOW if idx == self.cur_option and not self.justTxt else self.game.WHITE
            text_rect = self.game.helper.draw_text(
                display, options_txt, color, self.font_size, self.x_pos, start_y + idx * 3 * self.font_size
            )
            self.rec.append(text_rect)

    def mouse_collidepoint(self, x, y, index):
        return len(self.rec) == 0 or self.rec[index].collidepoint(x, y)

## load game background music [music1, music2]

## load game sounds 

## other stuff
    

