import pygame

class Menu():
    def __init__(self, game):
        self.game = game
        self.mid_w, self.mid_h = self.game.DISPLAY_W / 2, self.game.DISPLAY_H / 2
        self.run_display = True
        self.cursor_rect = pygame.Rect(0, 0, 20, 20)
        self.offset = - 100
        

    def draw_cursor(self):
        self.game.helper.draw_text(self.game, '*', 15, self.cursor_rect.x, self.cursor_rect.y)

    def blit_screen(self):
        self.game.window.blit(self.game.display, (0, 0))
        pygame.display.update()
        self.game.reset_keys()

class MainMenu(Menu):
    def __init__(self, game):
        Menu.__init__(self, game)
        self.state = "Start"
        self.startx, self.starty = self.mid_w, self.mid_h + 30
        self.optionsx, self.optionsy = self.mid_w, self.mid_h + 50
        self.creditsx, self.creditsy = self.mid_w, self.mid_h + 70
        self.cursor_rect.midtop = (self.startx + self.offset, self.starty)
        self.Rec_Main_Menu = self.game.helper.draw_text(self.game,'Main Menu', 20, self.game.DISPLAY_W / 2, self.game.DISPLAY_H / 2 - 20)
        self.Rec_Start = self.game.helper.draw_text(self.game,"Start Game", 20, self.startx, self.starty)
        self.Rec_Options = self.game.helper.draw_text(self.game,"Options", 20, self.optionsx, self.optionsy)
        self.Rec_Credits = self.game.helper.draw_text(self.game,"Credits", 20, self.creditsx, self.creditsy)

    def display_menu(self):
        self.run_display = True
        while self.run_display:
            self.game.check_events()
            self.check_input()
            self.game.display.fill(self.game.BLACK)
            self.game.helper.draw_text(self.game,'Main Menu', 20, self.game.DISPLAY_W / 2, self.game.DISPLAY_H / 2 - 20)
            self.game.helper.draw_text(self.game,"Start Game", 20, self.startx, self.starty)
            self.game.helper.draw_text(self.game,"Options", 20, self.optionsx, self.optionsy)
            self.game.helper.draw_text(self.game,"Credits", 20, self.creditsx, self.creditsy)
            self.draw_cursor()
            self.blit_screen()

    def move_cursor(self):
        if self.game.DOWN_KEY:
            if self.state == 'Start':
                self.cursor_rect.midtop = (self.optionsx + self.offset, self.optionsy)
                self.state = 'Options'
            elif self.state == 'Options':
                self.cursor_rect.midtop = (self.creditsx + self.offset, self.creditsy)
                self.state = 'Credits'
            elif self.state == 'Credits':
                self.cursor_rect.midtop = (self.startx + self.offset, self.starty)
                self.state = 'Start'
        elif self.game.UP_KEY:
            if self.state == 'Start':
                self.cursor_rect.midtop = (self.creditsx + self.offset, self.creditsy)
                self.state = 'Credits'
            elif self.state == 'Options':
                self.cursor_rect.midtop = (self.startx + self.offset, self.starty)
                self.state = 'Start'
            elif self.state == 'Credits':
                self.cursor_rect.midtop = (self.optionsx + self.offset, self.optionsy)
                self.state = 'Options'

    def check_input(self):
        self.move_cursor()
        if self.game.START_KEY:
            if self.state == 'Start':
                self.game.playing = True
            elif self.state == 'Options':
                self.game.curr_menu = self.game.options
            elif self.state == 'Credits':
                self.game.curr_menu = self.game.credits
        if self.game.KEY_PRESS:
            x, y = pygame.mouse.get_pos()
            if self.Rec_Start.collidepoint(x, y):
                self.game.playing = True
            elif self.Rec_Options.collidepoint(x, y):
                self.game.curr_menu = self.game.options
            elif self.Rec_Credits.collidepoint(x, y):
                self.game.curr_menu = self.game.credits
        self.run_display = False  



class OptionsMenu(Menu): #Todo: make options menu : game_mode : computer-to-computer or player-to-player or player-to-computer , difficulty : easy or hard , volume : 0-100
    def __init__(self, game):
        Menu.__init__(self, game)
        self.volx, self.voly = self.mid_w, self.mid_h + 20
        self.controlsx, self.controlsy = self.mid_w, self.mid_h + 40
        self.cursor_rect.midtop = (self.volx + self.offset, self.voly)


    def display_menu(self):
        while self.run_display:
            self.game.check_events()
            self.check_input()
            self.game.display.fill(self.game.BLACK)
            self.game.helper.draw_text(self.game,'Options', 20, self.game.DISPLAY_W / 2, self.game.DISPLAY_H / 2 - 30)
            self.draw_cursor()
            self.blit_screen()

    def check_input(self):
        if self.game.BACK_KEY:
            self.game.curr_menu=self.game.main_menu
            self.run_display=False
            pass



class CreditsMenu(Menu):
    def __init__(self, game):
        Menu.__init__(self, game)

    def display_menu(self):
            self.run_display = True
            while self.run_display:
                self.game.check_events()
                if self.game.START_KEY or self.game.BACK_KEY:
                    self.game.curr_menu = self.game.main_menu
                    self.run_display = False
                self.game.display.fill(self.game.BLACK)
                self.game.helper.draw_text(self.game,'Credits', 20, self.game.DISPLAY_W / 2, 50)

                # List of contributors
                contributors = [
                    ("Developer", "Rana Hossny"),
                    ("Developer", "Sara Hossny"),
                    ("Artist", "Dallash"),            
                ]

                y_position = 100
                for role, name in contributors:
                    self.game.helper.draw_text(self.game,f'{role} : {name}', 15, self.game.DISPLAY_W / 2, y_position)
                    y_position += 20

                self.blit_screen()







