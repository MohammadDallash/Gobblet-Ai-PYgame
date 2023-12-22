import pygame, csv, os
from math import log2


class Tile(pygame.sprite.Sprite):
    def __init__(self, imageIdx, x, y, spritesheet):
        pygame.sprite.Sprite.__init__(self)
        self.imgIds = spritesheet.keys_list # a list of the images names used in the spritesheet.
        self.image = spritesheet.parse_sprite(self.imgIds[imageIdx]) # load an image from the spritesheet.
        self.rect = self.image.get_rect() # get the rect object and change its rectangular coordinates.
        self.rect.x, self.rect.y = x, y
    # draw a surface onto the screen.
    def draw(self, surface):
        surface.blit(self.image, (self.rect.x, self.rect.y))

class TileMap():

    def __init__(self, filename, spritesheet):
        self.tile_size = 120
        self.spritesheet = spritesheet

        self.map_tiles = self.load_initial_tiles(filename)

        self.map_surface = pygame.Surface((self.map_w, self.map_h))
        self.board_surface = pygame.Surface((self.map_w, self.map_h))
        self.inventory_surface = pygame.Surface((self.map_w, self.map_h))

        self.draw_initial_tiles()
        self.map_surface.set_colorkey((0, 0, 0))
        self.board_surface.set_colorkey((0, 0, 0))
        self.inventory_surface.set_colorkey((0, 0, 0))
        self.reconstruct_map()
        self.reconstruct_inventory()

    def draw_initial_tiles(self):
        for tile in self.map_tiles:
            tile.draw(self.map_surface)


    def draw_map_on_canvas(self, surface):
        surface.blit(self.map_surface, (0, 0))
        surface.blit(self.board_surface, (0, 0))
        surface.blit(self.inventory_surface, (0, 0))


    def get_drawing_idx_on_Tilemap(self, number):
        if (number == -1):
            return -1

        largest_bit = 256
        while largest_bit >0:
            if(largest_bit & number != 0):
                break
            largest_bit>>=1 
        
        white = 0
        if(largest_bit > 8):
            largest_bit /=16
            white = 1
        return int(log2(largest_bit))  + (white)*12
        

    def reconstruct_inventory(self, inventory=[[15,15,15],[240,240,240]]):
        ##TODO
        pass

    def reconstruct_map(self, board=None):
        if(board!=None):
            row,col = len(board), len(board[0])
            for y in range (row):
                for x in range (col):

                    idx = self.get_drawing_idx_on_Tilemap(board[y][x])
                    
                   
                    T = (Tile( idx, (x+3) * self.tile_size, (y+1) * self.tile_size, self.spritesheet))
                    T.draw(self.board_surface)
        

    def read_csv(self, filename):
        map = []
        with open(os.path.join(filename)) as data:
            data = csv.reader(data, delimiter=',')
            for row in data:
                map.append(list(row))
        return map

    def load_initial_tiles(self, filename):
        tiles = []
        map = self.read_csv(filename)
        x, y = 0, 0
        for row in map:
            x = 0
            for tile in row:
                tiles.append(Tile(int(tile), x * self.tile_size, y * self.tile_size, self.spritesheet))
                x += 1

            # Move to next row
            y += 1
            # Store the size of the tile map
##

        self.map_w, self.map_h = x * self.tile_size, y * self.tile_size
        return tiles

