import pygame
import math
from ui import ui_utils as utils
import ui.SpriteController as spriteC
import ui.SpriteSet as spriteS

from constants import *


class UIHandler(object):
    def __init__(self, screen, logic_controller):
        self.screen = screen
        self.logic_controller = logic_controller
        self.pieces_list = logic_controller.pieces_list
        
        self.rel_mouse_pos = None
        self.sel_piece = None   # start with no piece selected/being dragged
        
        self.background_img = utils.load_image(BACKGROUND_IMAGE_FILE)
        self.highlighting_img = utils.load_image(HIGHLIGHTING_IMAGE_FILE)
        self.check_img = utils.load_image(CHECK_IMAGE_FILE)
        self.sprite_controller = self.setup_sprites()

    def setup_sprites(self):
        sprite_set = spriteS.SpriteSet(SPRITE_IMAGE_FILE, None, 80, 80)
        
        for i in range(len(SPRITE_NAMES)):
            start_x = (i * SPRITE_WIDTH) % SPRITE_SHEET_WIDTH
            start_y = math.floor(i / (SPRITE_SHEET_WIDTH / SPRITE_WIDTH)) * SPRITE_HEIGHT
            sprite_set.add_sprite(SPRITE_NAMES[i], start_x, start_y)
        
        return spriteC.SpriteController(self.screen, sprite_set, self.pieces_list)
    
    def render_board(self):
        self.screen.blit(self.background_img, (0, 0))
        self.render_highlighting()
        self.sprite_controller.render_all()
        pygame.display.flip()

    def render_highlighting(self):
        last_move = self.logic_controller.last_move
        if last_move:
            self.render_highlighted_tile(last_move.start)
            self.render_highlighted_tile(last_move.end)
        if self.logic_controller.in_check:
            king_pos = self.logic_controller.get_king_pos()
            self.render_checked_tile(king_pos)

    def render_highlighted_tile(self, grid_pos):
        if utils.is_white_square(grid_pos):
            alpha = 70
        else:
            alpha = 50
        self.highlighting_img.set_alpha(alpha)
        self.screen.blit(self.highlighting_img, utils.grid_to_pixels(grid_pos))

    def render_checked_tile(self, grid_pos):
        if utils.is_white_square(grid_pos):
            alpha = 90
        else:
            alpha = 60
        self.check_img.set_alpha(alpha)
        self.screen.blit(self.check_img, utils.grid_to_pixels(grid_pos))

    def render_board_with_moving_piece(self, mouse_pos):
        self.screen.blit(self.background_img, (0, 0))
        self.render_highlighting()
        self.sprite_controller.render_all_but_one(self.sel_piece.piece_id)

        piece_pos = (mouse_pos[0] - SPRITE_WIDTH / 2,
                     mouse_pos[1] - SPRITE_HEIGHT / 2)
        self.sprite_controller.render_piece_at_position(self.sel_piece, piece_pos)
        pygame.display.flip()
    
    def check_events(self):
        cont_execution = True
        for event in pygame.event.get():
            mouse_pos = pygame.mouse.get_pos()

            # quit events
            if event.type == pygame.QUIT:
                cont_execution = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    cont_execution = False

            # keyboard events
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    self.reset()

            # mouse events
            if event.type == pygame.MOUSEBUTTONDOWN:
                self.sel_piece = self.logic_controller.get_piece_by_pos(utils.pixels_to_grid(mouse_pos))
                # if not turn of sel_piece, deselect
                if self.sel_piece and (self.sel_piece.color == "w") != self.logic_controller.white_to_play:
                    self.sel_piece = None
            if event.type == pygame.MOUSEBUTTONUP:
                if self.sel_piece is not None:
                    new_pos = utils.pixels_to_grid(mouse_pos)
                    if new_pos in self.logic_controller.possible_moves[self.sel_piece.piece_id]:
                        self.logic_controller.make_move(self.sel_piece, new_pos)
                        self.logic_controller.check_state_of_game()
                self.sel_piece = None
                self.render_board()
            
            if self.sel_piece is not None:
                self.render_board_with_moving_piece(mouse_pos)
        
        return cont_execution

    def reset(self):
        self.logic_controller.reset()
        self.__init__(self.screen, self.logic_controller)
        self.render_board()
        self.logic_controller.logger.log("\nGame was reset.\n\n")
