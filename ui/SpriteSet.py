from ui import ui_utils as utils
import ui.SpriteType


class SpriteSet(object):
    def __init__(self, image, color_key, tile_width, tile_height):
        self.image = utils.load_image(image, color_key)
        self.tile_width = tile_width
        self.tile_height = tile_height
        self.tile_types = dict()
    
    def add_sprite(self, name, start_x, start_y):
        self.tile_types[name] = ui.SpriteType.SpriteType(
                name, start_x, start_y, self.tile_width, self.tile_height)
    
    def get_sprite(self, name):
        try:
            return self.tile_types[name]
        except KeyError:
            return None
