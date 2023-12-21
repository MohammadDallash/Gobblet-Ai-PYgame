import pygame, csv, os

class Tile(pygame.sprite.Sprite):
    def __init__(self, imageIdx, x, y, spritesheet):
        pygame.sprite.Sprite.__init__(self)
        
        self.imgIds = spritesheet.keys_list

        self.image = spritesheet.parse_sprite(self.imgIds[imageIdx])
        # Manual load in: self.image = pygame.image.load(image)
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = x, y

    def draw(self, surface):
        surface.blit(self.image, (self.rect.x, self.rect.y))

class TileMap():

    def __init__(self, filename, spritesheet):

        self.tile_size = 120
        self.spritesheet = spritesheet

        self.map_tiles = self.load_initial_tiles(filename)


        self.map_surface = pygame.Surface((self.map_w, self.map_h))
        self.board_surface = pygame.Surface((self.map_w, self.map_h))

        self.draw_initial_tiles()



        

        self.map_surface.set_colorkey((0, 0, 0))
        self.board_surface.set_colorkey((0, 0, 0))
        self.reconstruct_map()
        self.convert = {0:4,2:1, 4:0,-2:5}

    def draw_initial_tiles(self):
        for tile in self.map_tiles:
            tile.draw(self.map_surface)



    def draw_map_on_canvis(self, surface):
        surface.blit(self.map_surface, (0, 0))
        surface.blit(self.board_surface, (0, 0))

    def reconstruct_map(self, board=None ):
        if(board!=None):
            n,m = len(board), len(board[0])
            for y in range (n):
                for x in range (m):
                    idx = self.convert[board[y][x] - board[y][x]%2]
                    T = (Tile( idx  + (board[y][x]%2)*6, (x+3) * self.tile_size, (y+1) * self.tile_size, self.spritesheet))
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

