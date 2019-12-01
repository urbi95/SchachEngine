from copy import deepcopy

import tensorflow as tf
import numpy as np

from game_logic.Move import Move
from game_logic.logic_utils import detect_en_passant
from nn.train_neural_network import SAVE_PATH


class NNModelHandler:
    def __init__(self, logic_controller):
        self.logic_controller = logic_controller
        self.model = self.load_model(SAVE_PATH)

    @staticmethod
    def load_model(path):
        print("Loading model...")

        # Set memory growth, had an error without that
        gpus = tf.config.experimental.list_physical_devices('GPU')
        if gpus:
            try:
                # Currently, memory growth needs to be the same across GPUs
                for gpu in gpus:
                    tf.config.experimental.set_memory_growth(gpu, True)
                logical_gpus = tf.config.experimental.list_logical_devices('GPU')
                print(len(gpus), "Physical GPUs,", len(logical_gpus), "Logical GPUs")
            except RuntimeError as e:
                # Memory growth must be set before GPUs have been initialized
                print(e)

        model = tf.keras.models.load_model("nn/" + path)

        print("Finished loading model.")

        return model

    def choose_and_make_move(self):
        moves = self.logic_controller.possible_moves
        if self.logic_controller.is_checkmate or self.logic_controller.is_stalemate:
            return
        else:
            best_move_piece = None
            best_move_new_pos = (-1, -1)
            best_move_score = 0
            for piece_id in moves:
                piece = self.logic_controller.get_piece_by_id(piece_id)
                for new_pos in moves[piece_id]:
                    score = self.simulate_and_evaluate_move(piece, new_pos)
                    if score > best_move_score:
                        best_move_piece = piece
                        best_move_new_pos = new_pos

            self.logic_controller.make_move(best_move_piece, best_move_new_pos)
            self.logic_controller.check_state_of_game()

    def simulate_and_evaluate_move(self, piece, new_pos):
        move = Move(piece, piece.grid_position, new_pos)
        sim_board_state = deepcopy(self.logic_controller.board_state)
        sim_board_state[move.start] = 0
        sim_board_state[move.end] = move.piece.board_state_encoding
        if detect_en_passant(move, self.logic_controller.board_state):
            sim_board_state[move.end[0], move.start[1]] = 0

        model_input = self.get_model_input_from_game_state(sim_board_state)
        prediction = self.model.predict(model_input[np.newaxis, :, :, :])
        if self.logic_controller.white_to_play:
            score = prediction[0][0]
        else:
            score = prediction[0][1]

        return score

    def get_model_input_from_game_state(self, board_state):
        model_input = np.zeros((8, 8, 13), dtype=float)
        for i in range(6):
            # store black pieces
            model_input[:, :, i] = (board_state == i - 6)
        for i in range(6):
            # store white pieces
            model_input[:, :, i + 6] = (board_state == i + 1)

        # store whose turn it is
        model_input[:, :, 12] = (True if self.logic_controller.white_to_play else False)

        return model_input
