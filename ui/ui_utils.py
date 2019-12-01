import pygame
import math
import string

from constants import *
from game_logic.logic_utils import detect_castle


def load_image(filename, color_key=None):
    image = pygame.image.load(filename)

    if image.get_alpha() is None:
        image = image.convert()
    else:
        image = image.convert_alpha()
 
    if color_key is not None:
        if color_key is -1:
            color_key = image.get_at((0, 0))
        image.set_colorkey(color_key, pygame.RLEACCEL)

    return image


def pixels_to_grid(pixel_pos):
    # calculates grid coordinates from pixel coordinates
    x_grid = math.floor(pixel_pos[0] / SPRITE_WIDTH)
    y_grid = 7 - math.floor(pixel_pos[1] / SPRITE_HEIGHT)
    
    return x_grid, y_grid


def grid_to_pixels(grid_pos):
    # calculates pixel coordinates from grid coordinates
    x_pixel = SPRITE_WIDTH * grid_pos[0]
    y_pixel = BACKGROUND_HEIGHT - SPRITE_HEIGHT * (grid_pos[1] + 1)
    
    return x_pixel, y_pixel


def is_white_square(grid_pos):

    return (grid_pos[0] + grid_pos[1]) % 2 == 1


def move_to_string(move):
    if detect_castle(move):
        piece_abbr = ""
        start = "O"
        if move.end[0] < 4:
            # castled left
            end = "O-O"
        else:
            # castled right
            end = "O"
    else:
        piece_abbr = move.piece.get_piece_abbr()
        start = coord_to_string(move.start)
        end = coord_to_string(move.end)

    return piece_abbr + start + "-" + end


def coord_to_string(grid_pos):

    return list(string.ascii_lowercase)[grid_pos[0]] + str(grid_pos[1])
