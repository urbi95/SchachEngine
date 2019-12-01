import pygame
import Logger
import game_logic.LogicController
import ui.UIHandler
import nn.NNModelHandler


class Core(object):
    def __init__(self):
        if not pygame.font:
            print('Thou shalt thus be warned: pygame.font module could not be loaded.')
        if not pygame.mixer:
            print('Thou shalt thus be warned: pygame.mixer module could not be loaded.')
        
        pygame.init()
        self.screen = pygame.display.set_mode((640, 640))
    
        pygame.display.set_caption("Chess")
        pygame.mouse.set_visible(1)
    
        self.clock = pygame.time.Clock()
        self.running = True
        
        self.logger = Logger.Logger()
        self.use_nn_for_white, self.use_nn_for_black = self.logger.enquire_use_nn()
        self.logic_controller = game_logic.LogicController.LogicController(self.logger)
        self.ui_handler = ui.UIHandler.UIHandler(self.screen, self.logic_controller)
        if self.use_nn_for_white or self.use_nn_for_black:
            self.nn_model_handler = nn.NNModelHandler.NNModelHandler(self.logic_controller)
    
    def loop(self):
        self.ui_handler.render_board()
        while self.running:
            use_nn_this_move = (self.logic_controller.white_to_play and self.use_nn_for_white) or \
                    (not self.logic_controller.white_to_play and self.use_nn_for_black)
            if use_nn_this_move and not self.logic_controller.is_checkmate and not self.logic_controller.is_stalemate:
                self.clock.tick(1)
                self.nn_model_handler.choose_and_make_move()
                self.ui_handler.render_board()
            else:
                self.clock.tick(30)
                self.running = self.ui_handler.check_events()

    @staticmethod
    def cleanup():
        pygame.quit()
