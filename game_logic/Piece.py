import re
import numpy as np

from constants import BOARD_STATE_ENCODING, PIECE_ABBREVIATIONS
from game_logic.logic_utils import get_move_function


class Piece(object):
    def __init__(self, sprite_name, grid_position, piece_id):
        self.sprite_name = sprite_name
        self.name  = next(re.finditer(r"([a-z]*)_([a-z])", sprite_name, re.MULTILINE)).group(1)
        self.color = next(re.finditer(r"([a-z]*)_([a-z])", sprite_name, re.MULTILINE)).group(2)
        self.grid_position = grid_position
        self.can_castle = True if (self.name == "king" or self.name == "rook") else False
        self.piece_id = piece_id    # should match position in pieces list
        self.board_state_encoding = self.get_board_code()
        self.move_function = get_move_function(self.name)

    def get_board_code(self):
        sign = 1 if self.color == "w" else -1

        return sign * BOARD_STATE_ENCODING[self.name]

    def get_piece_abbr(self):

        return PIECE_ABBREVIATIONS[self.name]

    def get_possible_moves(self, board_state, en_passant, can_castle_l, can_castle_r):
        color_mask = board_state if self.color == "w" else np.negative(board_state)

        if self.name == "king":
            moves = self.move_function(self.grid_position, color_mask, can_castle_l, can_castle_r)
        elif self.name == "pawn":
            moves = self.move_function(self.grid_position, color_mask, self.color, en_passant)
        else:
            moves = self.move_function(self.grid_position, color_mask)

        return moves
