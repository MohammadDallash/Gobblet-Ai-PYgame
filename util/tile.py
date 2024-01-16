import pygame, csv, os
from math import log2
from util.helpers import *
from util.tile import *

# pieces for each color.
EMPTY_TILE = 0
BLUE_SMALL = 1
BLUE_MEDIUM = 2
BLUE_LARGE = 4
BLUE_XLARGE = 8
RED_SMALL = 16
RED_MEDIUM = 32
RED_LARGE = 64
RED_XLARGE = 128

BLUE, RED = 0, 1
INVENTORY_MOVE = 0
BOARD_MOVE = 1


class Tile(pygame.sprite.Sprite):
    def __init__(self, imageIdx, x, y, spritesheet):
        pygame.sprite.Sprite.__init__(self)
        self.imgIds = spritesheet.keys_list  # a list of the images names used in the spritesheet.
        self.image = spritesheet.parse_sprite(self.imgIds[imageIdx])  # load an image from the spritesheet.
        self.rect = self.image.get_rect()  # get the rect object and change its rectangular coordinates.
        self.rect.x, self.rect.y = x, y
        self.rows = 0
        self.cols = 0

    # draw a surface onto the screen.
    def draw(self, surface):
        surface.blit(self.image, (self.rect.x, self.rect.y))

    def get_rect(self):
        return self.rect
    
    def get_coor(self):
        return self.rect.x , self.rect.y
    
    def fill(self,r,g,b):
        pass




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
        self.piece_to_idx = {
            EMPTY_TILE: get_drawing_idx_on_Tilemap(EMPTY_TILE),
            BLUE_SMALL: get_drawing_idx_on_Tilemap(BLUE_SMALL),
            BLUE_MEDIUM: get_drawing_idx_on_Tilemap(BLUE_MEDIUM),
            BLUE_LARGE: get_drawing_idx_on_Tilemap(BLUE_LARGE),
            BLUE_XLARGE: get_drawing_idx_on_Tilemap(BLUE_XLARGE),
            RED_SMALL: get_drawing_idx_on_Tilemap(RED_SMALL),
            RED_MEDIUM: get_drawing_idx_on_Tilemap(RED_MEDIUM),
            RED_LARGE: get_drawing_idx_on_Tilemap(RED_LARGE),
            RED_XLARGE: get_drawing_idx_on_Tilemap(RED_XLARGE)}
        self.reconstruct_map()
        self.reconstruct_inventory()

    def draw_initial_tiles(self):
        for tile in self.map_tiles:
            tile.draw(self.map_surface)

    def draw_map_on_canvas(self, surface):
        surface.blit(self.map_surface, (0, 0))

        surface.blit(self.board_surface, (0, 0))
        surface.blit(self.inventory_surface, (0, 0))

    # draw inventory on the screen.
    def reconstruct_inventory(self, inventory=[[1, 1, 1], [16, 16, 16]], src_is_selected = False, srcNotToDraw = [-1,-1,-1]):
        if src_is_selected and srcNotToDraw[0] != INVENTORY_MOVE:
            src_is_selected = False


        self.inventory_surface.fill((0, 0, 0))
        inv_p1, inv_p2 = [], []
        for i in range(3):
            # get the pieces on top.


            itr_p1 = get_largest_piece(inventory[BLUE][i], secLargest=src_is_selected and srcNotToDraw[2] == i and srcNotToDraw[1] == BLUE)
            itr_p2 = get_largest_piece(inventory[RED][i], secLargest=src_is_selected and srcNotToDraw[2] == i and srcNotToDraw[1] == RED)

            # get coordinates for the inventory pieces.
            y = (1 + i) * int(self.tile_size * 1.5) - int(self.tile_size / 2)
            x_p1 = 1 * self.tile_size
            x_p2 = 8 * self.tile_size

            # append tiles in a list for future processing.
            inv_p2.append(Tile(self.piece_to_idx[itr_p2], x_p2, y, self.spritesheet))
            inv_p1.append(Tile(self.piece_to_idx[itr_p1], x_p1, y, self.spritesheet))

        # draw tiles on the screen.
        for i in range(3):
            inv_p1[i].draw(self.board_surface)
            inv_p2[i].draw(self.board_surface)

        # return the resulting tile list.
        return [inv_p1, inv_p2]

    def selected_tile(self, selected_tile_value, position):
        # Get the sprite for the selected tile
        tile = Tile(self.piece_to_idx[selected_tile_value], 0, 0, self.spritesheet)
        # Calculate the offset so the mouse is in the center of the tile
        offset_x = tile.rect.width // 2
        offset_y = tile.rect.height // 2
        # Update the tile's position
        tile.rect.x = position[0] - offset_x
        tile.rect.y = position[1] - offset_y
        return tile

    def reconstruct_map(self, board=None, src_is_selected = False, srcNotToDraw = [-1,-1,-1]):
        if src_is_selected and srcNotToDraw[0] != BOARD_MOVE:
            src_is_selected = False
        
        self.board_surface.fill((0, 0, 0))
        board_tiles = []
        if board is not None:
            row, col = len(board), len(board[0])
            for y in range(row):
                row_tiles = []
                for x in range(col):
                    largest_peace = get_largest_piece(board[y][x], secLargest=src_is_selected and y == srcNotToDraw[1] and x == srcNotToDraw[2])
                 
                    idx = self.piece_to_idx[largest_peace]
                    tile_x = (x + 3) * self.tile_size
                    tile_y = (y + 1) * self.tile_size
                    T = Tile(idx, tile_x, tile_y, self.spritesheet)
                    T.draw(self.board_surface)
                    row_tiles.append(T)
                board_tiles.append(row_tiles)

        return board_tiles

    def read_csv(self, filename):
        map = []
        with open(os.path.join(filename)) as data:
            data = csv.reader(data, delimiter=',')
            for row in data:
                map.append(list(row))
        return map

    def load_initial_tiles(self, filename):
        tiles = []
        map_data = self.read_csv(filename)
        x, y = 0, 0
        for row in map_data:
            x = 0
            for tile in row:
                tiles.append(Tile(int(tile), x * self.tile_size, y * self.tile_size, self.spritesheet))
                x += 1

            y += 1
        # Store the size of the tile map and the number of rows and columns
        self.map_w, self.map_h = x * self.tile_size, y * self.tile_size
        self.cols, self.rows = x, y
        return tiles
