from ui import ui_utils as utils


class SpriteController(object):
    def __init__(self, screen, sprite_set, pieces_list):
        self.screen = screen
        self.sprite_set = sprite_set
        self.pieces_list = pieces_list
    
    def render_all(self):
        for piece in self.pieces_list:
            self.render_piece(piece)
    
    def render_all_but_one(self, ignored_piece_id):
        for piece in self.pieces_list:
            if piece.piece_id != ignored_piece_id:
                self.render_piece(piece)
    
    def render_piece(self, piece):
        pixel_pos = utils.grid_to_pixels(piece.grid_position)
        self.render_piece_at_position(piece, pixel_pos)
    
    def render_piece_at_position(self, piece, pixel_pos):
        sprite_type = self.sprite_set.get_sprite(piece.sprite_name)
        if sprite_type is not None:
            self.screen.blit(self.sprite_set.image, pixel_pos, sprite_type.rect)
