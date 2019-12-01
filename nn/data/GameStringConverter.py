import numpy as np
from scipy import sparse

from game_logic.LogicController import LogicController
from nn.data.conversion_utils import remove_numbering, get_piece_from_move_string, get_pos_from_move_string, \
    find_coords_by_regex, check_promotion


class GameStringConverter(object):
    def __init__(self, game_string):
        self.game_string  = game_string
        self.move_strings = []
        self.logic_controller = LogicController()
        self.current_move  = 0
        self.result = None

        self.init_game()

    def init_game(self):
        # remove whitespaces, paragraphs, numbering, annotations for check and check mate
        moves = self.game_string.split()
        moves = [remove_numbering(moves[i]) for i in range(len(moves))]
        moves = [moves[i].replace("+", "").replace("#", "") for i in range(len(moves))]
        moves = [move for move in moves if move != ""]
        self.move_strings = moves

    def convert_game(self):
        converted_dict = {}
        for i in range(len(self.move_strings)):
            move = self.move_strings[i]
            if self.check_game_over(move):
                converted_dict["result"] = self.result
            else:
                # get name of next piece to move for more efficiency
                next_piece_name = get_piece_from_move_string(self.move_strings[i + 1])
                self.make_move(move, next_piece_name)
                self.current_move += 1
                converted_dict[self.current_move] = self.get_sparse_game_state()

        return converted_dict

    def check_game_over(self, move):
        game_over = False
        if move == "0-1":
            self.result = "black"
            game_over = True
        elif move == "1/2-1/2":
            self.result = "draw"
            game_over = True
        elif move == "1-0":
            self.result = "white"
            game_over = True

        return game_over

    def make_move(self, move, next_piece_name):
        pos = get_pos_from_move_string(move, self.logic_controller.white_to_play)
        piece_candidates = []
        promote_to = None
        for piece in self.logic_controller.pieces_list:
            if piece.name == get_piece_from_move_string(move):
                if pos in self.logic_controller.possible_moves[piece.piece_id]:
                    piece_candidates.append(piece)

        if len(piece_candidates) == 0:
            raise Exception("No possible piece found for move '{}'".format(move))
        if len(piece_candidates) > 1:
            # reduce list to one member
            piece_candidates = self.reduce_piece_candidates_list(piece_candidates, move)

        if check_promotion(move):
            promote_to = get_piece_from_move_string(move[-1])

        self.logic_controller.make_move(piece_candidates[0], pos, promote_to)
        self.logic_controller.check_state_of_game(next_piece_name)

    @staticmethod
    def reduce_piece_candidates_list(piece_candidates, move):
        first_coord, second_coord = find_coords_by_regex(move)
        if first_coord is not None:
            if second_coord is not None:
                for piece in piece_candidates:
                    if piece.grid_position == (first_coord, second_coord):
                        piece_candidates = [piece]
                        break
            else:
                for piece in piece_candidates:
                    if piece.grid_position[0] == first_coord:
                        piece_candidates = [piece]
                        break
        else:
            for piece in piece_candidates:
                if piece.grid_position[1] == second_coord:
                    piece_candidates = [piece]
                    break

        if len(piece_candidates) != 1:
            raise Exception("Reduction of piece_candidates list failed.")

        return piece_candidates

    def get_sparse_game_state(self):
        sparse_matrices_list = []
        for i in range(6):
            # store black pieces
            sparse_matrices_list.append(sparse.csc_matrix(self.logic_controller.board_state == i - 6))
        for i in range(6):
            # store white pieces
            sparse_matrices_list.append(sparse.csc_matrix(self.logic_controller.board_state == i + 1))

        # store whose turn it is
        sparse_matrices_list.append(sparse.csc_matrix(np.ones((8, 8), dtype=bool) if self.logic_controller.white_to_play
                                                      else np.zeros((8, 8), dtype=bool)))

        return sparse_matrices_list
