import pygame
import sys 

from states.state_manager import StateManager
from states.main_game_state import InGame
from states.title_screen_state import TitleScreen
from states.options_screen_state import OptionsScreen
from states.instructions_screen_state import InstructionsScreen
from states.game_over_state import GameOver
#from states.loading_screen_state import LoadingScreen
from scripts.settings import * 

# the class that constructs the game itself
class Game:
    def __init__(self, screen):
        self.screen = screen  
        self.clock = pygame.time.Clock()
        self.running = True 
        self.state_manager = StateManager(self)
        self.is_fullscreen = False 

        # Initialise and add game states
        self.state_manager.add_state("title_screen", TitleScreen(self))
        #self.state_manager.add_state("loading_screen", LoadingScreen(self))
        self.state_manager.add_state("game", InGame(self))
        self.state_manager.add_state("options_screen", OptionsScreen(self))
        self.state_manager.add_state("information_screen", InstructionsScreen(self))
        self.state_manager.add_state("game_over", GameOver(self))
        self.state_manager.change_state("title_screen")

        # Initialise + Define fonts
        self.font = pygame.font.Font(FONT1, 80)
        self.font1 = pygame.font.Font(FONT2, 80)
        self.font2 = pygame.font.Font(FONT3, 80)
        self.font3 = pygame.font.Font(FONT4, 80)
        self.font4 = pygame.font.Font(FONT4, 40)
    
    def toggle_fullscreen(self):
        if self.is_fullscreen:
            self.screen
            self.is_fullscreen = False
        else:
            (self.screen, pygame.FULLSCREEN)
            self.is_fullscreen = True

    def run(self):
        while self.running:
            events = pygame.event.get()
            print(FONT1)
            for event in events:
                if event.type == pygame.QUIT:
                    self.running = False 
            
            self.state_manager.update(events)
      
            self.state_manager.draw(self.screen)

            pygame.display.flip()
            self.clock.tick(FPS)
        
        pygame.quit() 