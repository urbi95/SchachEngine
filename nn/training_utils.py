import numpy as np


def sparse_game_to_numpy(game_dict, start_at_move=0):
    board_state_list = []
    label_list = []
    num_moves = len(game_dict)

    for move_id in range(start_at_move, num_moves):
        matrix = np.zeros((8, 8, 13), dtype=bool)
        for i in range(13):
            matrix[:, :, i] = game_dict[move_id][i].toarray()

        board_state_list.append(matrix)
        if game_dict["result"] == "white":
            label = [1, 0]
        elif game_dict["result"] == "black":
            label = [0, 1]
        else:
            label = [0.5, 0.5]
        label_list.append(label)

    return board_state_list, label_list
