import pygame
import subprocess
import platform
import os
import sys
import re
from math import log2
import time

EMPTY_TILE = 0
BLUE_SMALL = 1
BLUE_MEDIUM = 2
BLUE_LARGE = 4
BLUE_XLARGE = 8
ALL_BLUE = 15
RED_SMALL = 16
RED_MEDIUM = 32
RED_LARGE = 64
RED_XLARGE = 128
ALL_RED = 240


# get the order of the highest bit in the number.
# Ex. n = 64 + 32 , get_highest_bit(n) = 6
# returns 0 if n=0
def get_highest_multiple_of_2(n):
    if n == 0:
        return 0
    bit = 0
    n >>= 1
    while (n != 0):
        n >>= 1
        bit += 1
    return 1 << bit


def get_largest_piece(n, secLargest = False):
    pieces = [BLUE_XLARGE, RED_XLARGE,
              BLUE_LARGE, RED_LARGE,
              BLUE_MEDIUM, RED_MEDIUM,
              BLUE_SMALL, RED_SMALL]

    first_time = False

    for piece in pieces:
        if piece & n:
            if not first_time and secLargest:
                first_time = True
            else:
                return piece

    return 0

def get_largest_piece_neutural(n):
    pieces = [BLUE_XLARGE, RED_XLARGE,
              BLUE_LARGE, RED_LARGE,
              BLUE_MEDIUM, RED_MEDIUM,
              BLUE_SMALL, RED_SMALL]

    for piece in pieces:
        if piece & n:
            if(piece>=16):
                return int(piece/16)
            else: return piece

    return 0






def compare_2d_lists(list1, list2):

    # Iterate through each element and compare them
    for i in range(len(list1)):
        for j in range(len(list1[i])):
            if list1[i][j] != list2[i][j]:
                return False  # Elements are not equal

    return True  # All elements are equal


def convert_move_to_str(move):
    move_str = f"{move[0][0]} {move[0][1]} {move[0][2]} {move[1][0]} {move[1][1]} {move[1][2]}"
    return move_str

def convert_stream_to_list(move_str):
    list=int(re.search(r'\d+', move_str).group())
    return [list[0:3],list[3,6]]

def is_move_valid(val_src, val_dst):
    if (val_src == 0):
        return False

    largest_piece_src = get_largest_piece(val_src)
    largest_piece_dst = get_largest_piece(val_dst)

    # check if any of the tiles are red, convert to a unified base for comparison.
    if (largest_piece_src > ALL_BLUE):
        largest_piece_src = largest_piece_src >> 4

    if (largest_piece_dst > ALL_BLUE):
        largest_piece_dst = largest_piece_dst >> 4

    # check the largest piece in both sides after being unified, if the move is valid, go ahead with it.
    if largest_piece_dst < largest_piece_src:
        return True
    else:
        return False


# get the tile order in the spritesheet using the tile id.
def get_drawing_idx_on_Tilemap(number):
    if (number == 0):
        return -1
    if (number == 0):
        largest_bit = 0
    else:
        largest_bit = int(log2(get_highest_multiple_of_2(number)))

    has_red = 0
    if (largest_bit > 3):
        largest_bit = largest_bit - 4
        has_red = 1

    return largest_bit + has_red * 12



def compare_2d_lists(list1, list2):

    # Iterate through each element and compare them
    for i in range(len(list1)):
        for j in range(len(list1[i])):
            if list1[i][j] != list2[i][j]:
                return False  # Elements are not equal

    return True  # All elements are equal


def is_blue(piece):

    return piece < ALL_BLUE


def is_red(piece):
        
    return piece > ALL_BLUE



def is_draw(last_blue,last_red):
    condition1 = len(last_red) == 6 and compare_2d_lists(last_red[0],last_red[2])  and compare_2d_lists(last_red[1],last_red[3])  and compare_2d_lists(last_red[2],last_red[4])  and compare_2d_lists(last_red[3],last_red[5])

    condition2 = len(last_blue) == 6 and compare_2d_lists(last_blue[0],last_blue[2]) and compare_2d_lists(last_blue[1],last_blue[3]) and compare_2d_lists(last_blue[2],last_blue[4]) and compare_2d_lists(last_blue[3],last_blue[5])

    if(condition1 or condition2):
        return True
    else:
        return False















class Helper:
    def __init__(self, game):
        self.game = game

    def load_assets(self):
        pass

    def draw_text(self, display, text, color, size, x, y,title = False):
        if(title):
            font = pygame.font.Font(self.game.text_font_name, size)
        else:
            font = pygame.font.Font(self.game.title_font_name, size)
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect()
        text_rect.center = (x, y)
        display.blit(text_surface, text_rect)

        return text_rect

    def cpp_code(self, args):
        file_name = 'Algorithms.cpp'

        executable_name = file_name.split('.')[0]
        executable_path = os.path.join(sys._MEIPASS, executable_name) if hasattr(sys, '_MEIPASS') else executable_name

        if platform.system() == "Windows": 
            executing_command = f"{executable_path} {args}"

        else:
            executing_command = f"./{executable_path} {args}"
        


       

        if self.game.ai_difficulty == 1:
            time.sleep(1)
       
        try:
            result = subprocess.run(executing_command, shell=True, check=True, capture_output=True, text=True)
            return result.stdout
        except subprocess.CalledProcessError as e:
            print(f"Execution failed with error: {e}")
            print("Error Output:", e.stderr)


    def flush(self, turn=1, board=[[1, 2, 3, 4], [1, 2, 3, 4], [1, 2, 3, 4], [1, 2, 3, 4]],
                      inv=[[1, 2, 3], [1, 2, 3]]):

        s = ''

        s+=(str(turn) + " ")

        for row in board:
            for i in row:
                s+=(str(i) + " ")

            s+=' ' 

        s+=' ' 

        for row in inv:
            for i in row:
                s+=(str(i) + " ")
            s+=' ' 

        s+= str(self.game.ai_difficulty)
        return s


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
            color = self.game.YELLOW if idx == self.cur_option and not self.justTxt else self.game.global_font_color
            text_rect = self.game.helper.draw_text(
                display, options_txt, color, self.font_size, self.x_pos, start_y + idx * 3 * self.font_size
            )
            self.rec.append(text_rect)

    def mouse_collidepoint(self, x, y, index):
        return len(self.rec) == 0 or self.rec[index].collidepoint(x, y)

## load game background music [music1, music2]

## load game sounds 

## other stuff
