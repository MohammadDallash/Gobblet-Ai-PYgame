import pygame
from math import log2

# get the order of the highest bit in the number.
# Ex. n = 64 + 32 , get_highest_bit(n) = 6
# returns 0 if n=0
def get_highest_power_of_2(n):
    if n ==-1:
        return -1
    bit = 0
    n >>=1
    while(n!=0):
        n >>=1
        bit+=1
    return bit


# get the tile order in the spritesheet using the tile id. 
def get_drawing_idx_on_Tilemap(number):
    if (number == -1):
        return -1
    
    largest_bit = get_highest_power_of_2(number)

    has_white = 0
    if(largest_bit > 3):
        largest_bit = largest_bit - 4
        has_white = 1
        
    return largest_bit + has_white*12



# @param src,dst -> the source, destenation tiles.
#        board -> board refrence 
# this function checks if a move is allowed from one tile to another, and makes the move if it's valid.

def make_move(board, src, dst):

    val_src = board[src[0]][src[1]]
    val_dst = board[dst[0]][dst[1]]

    # check if any of the tiles are white, convert to a unified base.
    if(val_src > 8):
        val_src /= 16

    if(val_dst > 8):
        val_dst /= 16

    val_src_pow2 = get_highest_power_of_2(val_src)

    # if the move is valid, go ahead with it.
    if val_dst < val_src:
        board[src[0]][src[1]] = board[src[0]][src[1]] & ~(2 << val_src_pow2)
        board[dst[0]][dst[1]] = board[dst[0]][dst[1]] |  (2 << val_src_pow2)
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
    

