import numpy as np

from constants import *
from copy import deepcopy

from game_logic.Piece import Piece
from game_logic.Move import Move
from game_logic.logic_utils import detect_en_passant, detect_castle, detect_promotion
from ui.ui_utils import move_to_string


class LogicController(object):
    def __init__(self, logger=None):
        self.logger = logger
        self.pieces_list = self.setup_pieces()
        self.largest_piece_id = 31
        self.board_state = self.setup_board_state()
        self.in_check = None
        self.possible_moves = {}
        self.en_passant = None
        self.is_checkmate = False
        self.is_stalemate = False
        self.white_to_play = True
        self.last_move = None
        self.number_of_moves = 0

        self.check_state_of_game()

    @staticmethod
    def setup_pieces():
        pieces = []
        piece_id = 0
        for i in range(len(SPRITE_NAMES)):
            for j in range(PIECES_COUNTS[i]):
                grid_position = PIECES_POSITIONS[i][j]
                pieces.append(Piece(SPRITE_NAMES[i], grid_position, piece_id))
                piece_id += 1

        return pieces

    def setup_board_state(self):
        board_state = np.zeros((8, 8), dtype=np.int8)
        for piece in self.pieces_list:
            board_state[piece.grid_position] = piece.board_state_encoding

        return board_state

    def get_color_to_play(self):

        return "w" if self.white_to_play else "b"

    def get_piece_by_pos(self, grid_pos):
        piece = None
        for p in self.pieces_list:
            if p.grid_position == grid_pos:
                piece = p

        return piece

    def get_piece_by_sprite_name(self, name):
        piece = None
        for p in self.pieces_list:
            if p.sprite_name == name:
                piece = p

        return piece

    def get_piece_by_id(self, piece_id):
        piece = None
        for p in self.pieces_list:
            if p.piece_id == piece_id:
                piece = p

        return piece

    def get_king_pos(self):
        if self.white_to_play:
            king = self.get_piece_by_sprite_name("king_w")
            pos = king.grid_position
        else:
            king = self.get_piece_by_sprite_name("king_b")
            pos = king.grid_position

        return pos

    def check_move_for_check(self, move):
        # simulate situation after move
        sim_board_state = deepcopy(self.board_state)
        sim_board_state[move.start] = 0
        sim_board_state[move.end] = move.piece.board_state_encoding
        excluded_pos = move.end
        if detect_en_passant(move, self.board_state):
            sim_board_state[move.end[0], move.start[1]] = 0
            excluded_pos = (move.end[0], move.start[1])
        color = move.piece.color

        if move.piece.name == "king":
            king_pos = move.end
        else:
            king_pos = self.get_king_pos()

        return self.check_for_threat(sim_board_state, color, king_pos, excluded_pos)

    def check_for_threat(self, board_state, color, king_pos, excluded_pos=None):
        threat = False

        for p in self.pieces_list:
            if p.color != color and p.grid_position != excluded_pos:    # exclude taken pieces from evaluation
                moves = p.get_possible_moves(board_state, self.en_passant, False, False)
                if king_pos in moves:
                    threat = True
                    break

        return threat

    def make_move(self, piece, new_pos, promote_to=None):
        move = Move(piece, piece.grid_position, new_pos)
        self.take_piece(move)
        self.castle(move)

        if piece.name == "pawn":
            if abs(move.start[1] - move.end[1]) > 1:
                self.en_passant = move.end[0]
        else:
            self.en_passant = None

        self.board_state[move.start] = 0
        self.board_state[move.end] = piece.board_state_encoding
        piece.grid_position = new_pos
        if piece.name == "king" or piece.name == "rook":
            piece.can_castle = False

        self.promote(move, promote_to)

        self.white_to_play = not self.white_to_play
        self.last_move = move

    def take_piece(self, move):
        if self.board_state[move.end]:
            taken_piece = self.get_piece_by_pos(move.end)
            self.pieces_list.remove(taken_piece)
        elif detect_en_passant(move, self.board_state):
            taken_piece = self.get_piece_by_pos((move.end[0], move.start[1]))
            self.board_state[taken_piece.grid_position] = 0
            self.pieces_list.remove(taken_piece)

    def castle(self, move):
        if detect_castle(move):
            if move.end[0] < move.start[0]:
                # king went for left castle
                rook = self.get_piece_by_pos((0, move.end[1]))
                self.board_state[0, move.end[1]] = 0
                self.board_state[3, move.end[1]] = rook.board_state_encoding
                rook.grid_position = (3, move.end[1])
            if move.end[0] > move.start[0]:
                # king went for right castle
                rook = self.get_piece_by_pos((7, move.end[1]))
                self.board_state[7, move.end[1]] = 0
                self.board_state[5, move.end[1]] = rook.board_state_encoding
                rook.grid_position = (5, move.end[1])

    def promote(self, move, promote_to):
        if detect_promotion(move.piece):
            if promote_to is None:
                user_input = input("Promote pawn to\nQueen (q)\nBishop (b)\nKnight (n)\nRook (r)\n?\n")
                sprite_name = self.handle_promotion_user_input(user_input)
            else:
                sprite_name = promote_to + "_" + self.get_color_to_play()
            self.add_new_piece(sprite_name, move.end)
            self.pieces_list.remove(move.piece)

    def handle_promotion_user_input(self, user_input):
        sprite_name = ""
        if user_input == "q":
            sprite_name = "queen_" + self.get_color_to_play()
        elif user_input == "b":
            sprite_name = "bishop_" + self.get_color_to_play()
        elif user_input == "n":
            sprite_name = "knight_" + self.get_color_to_play()
        elif user_input == "r":
            sprite_name = "rook_" + self.get_color_to_play()
        else:
            print("Error: Promotion not successful because of invalid user input.")

        return sprite_name

    def add_new_piece(self, sprite_name, pos):
        piece_id = self.largest_piece_id + 1
        piece = Piece(sprite_name, pos, piece_id)
        self.pieces_list.append(piece)
        self.board_state[pos] = piece.board_state_encoding
        self.largest_piece_id = piece_id

    def check_state_of_game(self, next_piece_name=None):
        color = self.get_color_to_play()
        if self.check_for_threat(self.board_state, color, self.get_king_pos()):
            self.in_check = color
        else:
            self.in_check = None

        # possible moves
        end_of_game = True
        can_castle_l, can_castle_r = self.check_castle()
        for p in self.pieces_list:
            if p.color == color:
                if next_piece_name is None or next_piece_name == p.name:
                    possible_moves = p.get_possible_moves(self.board_state, self.en_passant, can_castle_l, can_castle_r)
                    self.possible_moves[p.piece_id] = [move for move in possible_moves if not
                                                       self.check_move_for_check(Move(p, p.grid_position, move))]
                    if len(self.possible_moves[p.piece_id]) > 0:
                        end_of_game = False
            else:
                self.possible_moves[p.piece_id] = []

        # check for end of game
        if end_of_game:
            if self.in_check:
                self.is_checkmate = True
            else:
                self.is_stalemate = True

        if self.logger is not None:
            self.log_last_move()

    def check_castle(self):
        can_castle_l = False
        can_castle_r = False

        king_pos = self.get_king_pos()
        king = self.get_piece_by_pos(king_pos)
        if king is not None and king.can_castle and not self.in_check:
            rook_l = self.get_piece_by_pos((0, king_pos[1]))
            rook_r = self.get_piece_by_pos((7, king_pos[1]))
            color = self.get_color_to_play()
            if rook_l and rook_l.can_castle:
                skipped_square = (king_pos[0] - 1, king_pos[1])
                if (self.board_state[skipped_square] == 0 and
                        not self.check_for_threat(self.board_state, color, skipped_square)):
                    can_castle_l = True
            if rook_r and rook_r.can_castle:
                skipped_square = (king_pos[0] + 1, king_pos[1])
                if (self.board_state[skipped_square] == 0 and
                        not self.check_for_threat(self.board_state, color, skipped_square)):
                    can_castle_r = True

        return can_castle_l, can_castle_r

    def log_last_move(self):
        if self.last_move:
            message = ""
            if self.last_move.piece.color == "w":
                self.number_of_moves += 1
                message += str(self.number_of_moves) + ". "
            message += move_to_string(self.last_move)
            if self.in_check:
                if self.is_checkmate:
                    message += "#"
                else:
                    message += "+"
            message += " " if self.last_move.piece.color == "w" else "\n"

            self.logger.log(message)

            if self.is_checkmate:
                message = "0-1" if self.white_to_play else "1-0"
                self.logger.log("\n" + message)
            if self.is_stalemate:
                self.logger.log("\n1/2-1/2")

    def reset(self):
        self.__init__(self.logger)
