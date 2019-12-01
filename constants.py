WINDOW_WIDTH  = 640
WINDOW_HEIGHT = 640

BACKGROUND_IMAGE_FILE = "ui/img/board_small_tex.png"
BACKGROUND_WIDTH  = 640
BACKGROUND_HEIGHT = 640

HIGHLIGHTING_IMAGE_FILE = "ui/img/selected_small_light.png"
CHECK_IMAGE_FILE = "ui/img/check_small.png"

PIECES_COUNTS = [1, 1, 2, 2, 2, 8, 1, 1, 2, 2, 2, 8]
# Starting positions for chess pieces
PIECES_POSITIONS = [[(4, 0)],
                    [(3, 0)],
                    [(2, 0), (5, 0)],
                    [(1, 0), (6, 0)],
                    [(0, 0), (7, 0)],
                    [(0, 1), (1, 1), (2, 1), (3, 1), (4, 1), (5, 1), (6, 1), (7, 1)],
                    [(4, 7)],
                    [(3, 7)],
                    [(2, 7), (5, 7)],
                    [(1, 7), (6, 7)],
                    [(0, 7), (7, 7)],
                    [(0, 6), (1, 6), (2, 6), (3, 6), (4, 6), (5, 6), (6, 6), (7, 6)]]

BOARD_STATE_ENCODING = {"king": 1, "queen": 2, "bishop": 3, "knight": 4, "rook": 5, "pawn": 6}
PIECE_ABBREVIATIONS = {"king": "K", "queen": "Q", "bishop": "B", "knight": "N", "rook": "R", "pawn": ""}

# Pieces are visualized using sprites
SPRITE_WIDTH  = 80
SPRITE_HEIGHT = 80
SPRITE_SHEET_WIDTH  = 480
SPRITE_SHEET_HEIGHT = 160
SPRITE_IMAGE_FILE = "ui/img/chess_pieces_small.png"
# Sprite names have to be in the format "name_w" or "name_b"
SPRITE_NAMES = ["king_w", "queen_w", "bishop_w", "knight_w", "rook_w", "pawn_w",
                "king_b", "queen_b", "bishop_b", "knight_b", "rook_b", "pawn_b"]
