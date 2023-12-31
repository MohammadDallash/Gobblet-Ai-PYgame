import pygame
import json
import os


class Spritesheet:
    def __init__(self, filename):
        self.filename = filename
        # load the spritesheet and convert the pixel format.
        self.sprite_sheet = pygame.image.load(filename).convert()
        # get the file name for the meta_data file.
        self.meta_data = self.filename.replace('png', 'json')
        # convert json file into a dictionary.
        with open(self.meta_data) as f:
            self.data = json.load(f)
        f.close()
        self.keys_list = list(self.data['frames'].keys())

    # get a sprite from the spritesheet and blit it into a drawable surface.
    def get_sprite(self, x, y, w, h):
        sprite = pygame.Surface((w, h))
        sprite.set_colorkey((0, 0, 0))
        sprite.blit(self.sprite_sheet, (0, 0), (x, y, w, h))
        return sprite

    # get a sprite using its name from the meta_data.
    def parse_sprite(self, name):
        sprite = self.data['frames'][name]['frame']
        x, y, w, h = sprite["x"], sprite["y"], sprite["w"], sprite["h"]
        image = self.get_sprite(x, y, w, h)
        return image
