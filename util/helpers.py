import pygame
import subprocess
import platform
from math import log2

# get the order of the highest bit in the number.
# Ex. n = 64 + 32 , get_highest_bit(n) = 6
# returns 0 if n=0
def get_highest_multiple_of_2(n):

    if n == 0:
        return 0
    bit = 0
    n >>=1
    while(n!=0):
        n >>=1
        bit+=1
    return 1<<bit


# get the tile order in the spritesheet using the tile id. 
def get_drawing_idx_on_Tilemap(number):
    if (number == 0):
        return -1
    if(number == 0):
        largest_bit = 0
    else :
        largest_bit = int( log2(get_highest_multiple_of_2(number)))

    has_white = 0
    if(largest_bit > 3):
        largest_bit = largest_bit - 4
        has_white = 1
        
    return largest_bit + has_white*12





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
    
    def cpp_code(self,file_namee):
        file_name = 'test.cpp'
        input_file_name = file_namee

        compilation_command = f"g++ -o {file_name.split('.')[0]} {file_name}"

        executable_name = file_name.split('.')[0]

        executing_command = f"./{executable_name} < {input_file_name}" if platform.system() != 'Windows' else f"{executable_name} < {input_file_name}"

        try:
            # subprocess.run(compilation_command, shell=True, check=True)
            print("Compilation success")
        except subprocess.CalledProcessError as e:
            print(f"Compilation failed with error: {e}")

        try:
            result = subprocess.run(executing_command, shell=True, check=True, capture_output=True, text=True)
            return result.stdout

        except subprocess.CalledProcessError as e:
            print(f"Execution failed with error: {e}")
            print("Error Output:", e.stderr)


    def flush_to_file(self,board=[[1,2,3,4],[1,2,3,4],[1,2,3,4],[1,2,3,4]],inv = [[1,2,3],[1,2,3]]):
        
        with open("current_state_file.txt", "w") as f:
            for row in board:
                for i in row:
                    f.write(str(i)+" ")

                f.write("\n")

            f.write("\n")

            for row in inv:
                for i in row:
                    f.write(str(i)+" ")
                f.write("\n")



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
    

