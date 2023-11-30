import pygame


class Helper:
    def __init__(self):
        pass
    def load_assets():
        pass
    def draw_text(self, game, text, size, x, y):
        font = pygame.font.Font(game.font_name, size)
        text_surface = font.render(text, True, game.WHITE)
        text_rect = text_surface.get_rect()
        text_rect.center = (x, y)
        game.display.blit(text_surface, text_rect)
   
        return text_rect
## mouse

## load game background music [music1, music2]

## load game sounds 

## other stuff