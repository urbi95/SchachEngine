import re


def remove_numbering(move):
    clean_string = move
    p = re.compile(r"[0-9]+\.")
    matches = p.findall(move)
    if len(matches) == 1:
        clean_string = move.replace(matches[0], "")
    if len(matches) > 1:
        raise Exception("Numbering was not recognized correctly.")

    return clean_string


def get_pos_from_move_string(move, white_to_play):
    if move[0] == "O":
        # castle
        if move == "O-O":
            # short castle
            if white_to_play:
                pos = (6, 0)
            else:
                pos = (6, 7)
        else:
            # long castle
            if white_to_play:
                pos = (2, 0)
            else:
                pos = (2, 7)
    elif "=" in move:
        # promotion
        pos = get_pos_from_string(move[-4:])
    else:
        # regular move
        pos = get_pos_from_string(move[-2:])

    return pos


def get_piece_from_move_string(move_string):
    if move_string[0] == "O" or move_string[0] == "K":
        piece = "king"
    elif move_string[0] == "Q":
        piece = "queen"
    elif move_string[0] == "B":
        piece = "bishop"
    elif move_string[0] == "N":
        piece = "knight"
    elif move_string[0] == "R":
        piece = "rook"
    else:
        piece = "pawn"

    return piece


def get_pos_from_string(move):
    first_coord = ord(move[0].lower()) - 97
    second_coord = int(move[1]) - 1

    return first_coord, second_coord


def check_promotion(move):
    promotion = False
    if "=" in move:
        promotion = True

    return promotion


def find_coords_by_regex(move):
    first_coord  = None
    second_coord = None
    dummy_coord = "1"

    if check_regex(move, r"^[a-h][1-8]$"):
        first_coord = get_pos_from_string(match_regex(move, r"^[a-h][1-8]$")[0])[0]
    elif check_regex(move, r"[a-h][a-h][1-8]"):
        first_coord = get_pos_from_string(match_regex(move, r"[a-h][a-h][1-8]")[0][0] + dummy_coord)[0]
    elif check_regex(move, r"[a-h]x[a-h][1-8]"):
        first_coord = get_pos_from_string(match_regex(move, r"[a-h]x[a-h][1-8]")[0][0] + dummy_coord)[0]
    elif check_regex(move, r"[1-8][a-h][1-8]"):
        second_coord = int(match_regex(move, r"[1-8][a-h][1-8]")[0][0]) - 1
    elif check_regex(move, r"[1-8]x[a-h][1-8]"):
        second_coord = int(match_regex(move, r"[1-8]x[a-h][1-8]")[0][0]) - 1
    elif check_regex(move, r"[a-h][1-8][a-h][1-8]"):
        first_coord, second_coord = get_pos_from_string(match_regex(move, r"[a-h][1-8][a-h][1-8]")[0][0:1])[0]
    elif check_regex(move, r"[a-h][1-8]x[a-h][1-8]"):
        first_coord, second_coord = get_pos_from_string(match_regex(move, r"[a-h][1-8]x[a-h][1-8]")[0][0:1])[0]
    else:
        raise Exception("Could not match move '{}' with regex.".format(move))

    return first_coord, second_coord


def check_regex(move, regex):
    success = False
    p = re.compile(regex)
    matches = p.findall(move)
    if len(matches) == 1:
        success = True

    return success


def match_regex(move, regex):
    p = re.compile(regex)
    matches = p.findall(move)

    return matches
