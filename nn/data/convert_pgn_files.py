import sys
import pickle

from os import listdir
from os.path import isfile, join, splitext, basename

from nn.data.GameStringConverter import GameStringConverter


def convert_pgn_files(folder_path, destination, file_name=None, max_num_of_games=None):
    if file_name is None:
        files = [f for f in listdir(folder_path) if isfile(join(folder_path, f)) and f.endswith(".pgn")]
        for f in files:
            convert_single_pgn_file(join(folder_path, f), destination)
    else:
        if max_num_of_games is None:
            convert_single_pgn_file(join(folder_path, file_name), destination)
        else:
            convert_single_pgn_file(join(folder_path, file_name), destination, max_num_of_games)


def convert_single_pgn_file(file_path, destination, max_num_of_games=None):
    print("#" * 70)
    print("Converting file: " + file_path)

    storing_list = []
    with open(file_path) as f:
        current_game_string = ""
        game_counter = 0
        for line in f:
            if line.startswith("[") or line.startswith(" ") or line.startswith("\n"):
                current_game_string = ""
            else:
                current_game_string += line
                if line.endswith("1/2-1/2\n") or line.endswith("0-1\n") or line.endswith("1-0\n"):
                    # end of game found
                    game_counter += 1
                    sys.stdout.write("\rConverting game nr. %i" % game_counter)
                    sys.stdout.flush()
                    game_dict = convert_game_string(current_game_string)
                    storing_list.append(game_dict)

            if max_num_of_games == game_counter:
                break

    # save resulting dict
    filename = splitext(basename(file_path))[0]
    with open(join(destination, filename + ".pkl"), 'wb') as f:
        pickle.dump(storing_list, f, pickle.HIGHEST_PROTOCOL)


def convert_game_string(game_string):
    converter = GameStringConverter(game_string)
    converted_dict = converter.convert_game()

    return converted_dict


if __name__ == '__main__':
    PGN_RAW_FOLDER = "raw/KingBaseLite2019"
    DESTINATION_FOLDER = "custom_format"
    PGN_FILE = "KingBaseLite2019-A40-A79.pgn"
    MAX_NUMBER_OF_GAMES = 50
    convert_pgn_files(PGN_RAW_FOLDER, DESTINATION_FOLDER, PGN_FILE, MAX_NUMBER_OF_GAMES)
