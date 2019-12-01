def get_move_function(name):
    def king(grid_pos, color_mask, can_castle_l, can_castle_r):
        moves = bishop_moves(grid_pos, color_mask, 1) + rook_moves(grid_pos, color_mask, 1)
        if can_castle_l:
            moves.append((grid_pos[0] - 2, grid_pos[1]))
        if can_castle_r:
            moves.append((grid_pos[0] + 2, grid_pos[1]))

        return moves

    def queen(grid_pos, color_mask):
        moves = bishop_moves(grid_pos, color_mask, 7) + rook_moves(grid_pos, color_mask, 7)

        return moves

    def bishop(grid_pos, color_mask):
        moves = bishop_moves(grid_pos, color_mask, 7)

        return moves

    def knight(grid_pos, color_mask):
        directions = ((1, 2), (1, -2), (-1, 2), (-1, -2), (2, 1), (2, -1), (-2, 1), (-2, -1))
        board_moves = [(grid_pos[0] + d[0], grid_pos[1] + d[1]) for d in directions
                       if is_on_board((grid_pos[0] + d[0], grid_pos[1] + d[1]))]

        moves = [move for move in board_moves if color_mask[move] <= 0]

        return moves

    def rook(grid_pos, color_mask):
        moves = rook_moves(grid_pos, color_mask, 7)

        return moves

    def pawn(grid_pos, color_mask, color, en_passant):
        moves = []
        step = 1 if color == "w" else -1
        front = (grid_pos[0], grid_pos[1] + step)
        diag_l = (grid_pos[0] - 1, grid_pos[1] + step)
        diag_r = (grid_pos[0] + 1, grid_pos[1] + step)

        if color_mask[front] == 0 and is_on_board(front):
            moves.append(front)
            double_front = (grid_pos[0], grid_pos[1] + 2 * step)
            double_step_rank = 1 if color == "w" else 6
            if grid_pos[1] == double_step_rank and color_mask[double_front] == 0:
                moves.append(double_front)
        if is_on_board(diag_l) and (color_mask[diag_l] < 0 or check_en_passant(diag_l, color, en_passant)):
            moves.append(diag_l)
        if is_on_board(diag_r) and (color_mask[diag_r] < 0 or check_en_passant(diag_r, color, en_passant)):
            moves.append(diag_r)

        return moves

    def bishop_moves(grid_pos, color_mask, max_dist):
        moves = (moves_in_direction(grid_pos, color_mask, max_dist, (-1, -1))
                 + moves_in_direction(grid_pos, color_mask, max_dist, (-1, 1))
                 + moves_in_direction(grid_pos, color_mask, max_dist, (1, -1))
                 + moves_in_direction(grid_pos, color_mask, max_dist, (1, 1)))

        return moves

    def rook_moves(grid_pos, color_mask, max_dist):
        moves = (moves_in_direction(grid_pos, color_mask, max_dist, (0, -1))
                 + moves_in_direction(grid_pos, color_mask, max_dist, (0, 1))
                 + moves_in_direction(grid_pos, color_mask, max_dist, (-1, 0))
                 + moves_in_direction(grid_pos, color_mask, max_dist, (1, 0)))

        return moves

    def moves_in_direction(grid_pos, color_mask, max_dist, step):
        moves = []
        for i in range(1, max_dist + 1):
            grid_pos = (grid_pos[0] + step[0], grid_pos[1] + step[1])
            if is_on_board(grid_pos):
                masked_val = color_mask[grid_pos]
                if masked_val == 0:
                    moves.append(grid_pos)
                elif masked_val < 0:
                    moves.append(grid_pos)
                    break
                else:
                    break
            else:
                break

        return moves

    function_dict = {"king": king, "queen": queen, "bishop": bishop, "knight": knight, "rook": rook, "pawn": pawn}

    return function_dict[name]


def is_on_board(pos):
    return 0 <= pos[0] < 8 and 0 <= pos[1] < 8


def check_en_passant(pos, color, en_passant):
    condition_fulfilled = False
    if en_passant is not None:
        if (pos[1] == 5 and color == "w") or (pos[1] == 2 and color == "b"):
            if pos[0] == en_passant:
                condition_fulfilled = True

    return condition_fulfilled


def detect_en_passant(move, board_state):
    detected = False
    if move.piece.name == "pawn":
        if move.start[0] != move.end[0]:
            if board_state[move.end] == 0:
                detected = True

    return detected


def detect_castle(move):
    has_castled = False
    if move.piece.name == "king":
        if abs(move.start[0] - move.end[0]) > 1:
            has_castled = True

    return has_castled


def detect_promotion(piece):
    detected = False
    if piece.name == "pawn":
        if piece.grid_position[1] == 0 or piece.grid_position[1] == 7:
            detected = True

    return detected
