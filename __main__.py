##########
# LD 22
# The theme is alone
# it's a dumb theme
# fiona wrote this
##########

# System and Python lib imports
import sys
sys.path += ['.']

# Game engine imports
from myrmidon.myrmidon import MyrmidonGame, MyrmidonProcess
from myrmidon.consts import *
from pygame.locals import *

# Game imports
from consts import *
from media import Media
from gui import GUI
from galaxy import Galaxy
from game_galaxy import Galaxy_background, Solar_system_star, Player_ship, Galaxy_player_ship


class Game(MyrmidonProcess):

    # Current state
    game_state = 0

    # Player state
    money = 2000000000
    fuel = 0
    crew = 0
    current_system = "Sol"
    current_object = "Earth"

    fuel_cost = 1000000000
    crew_cost = 500000000
    actions_done = {}
    home_planet_result = []

    first_time = True
    
    # Self explanitory object pointers and lists
    fps_text = None
    gui = None
    media = None
    solar_system_objects = []

    player_ship = None
    background = None
    galaxy = None
    
    
    def execute(self):
        # Pre launch set-up
        MyrmidonGame.current_fps = 60
        self.priority = PRIORITY_MAIN_GAME

        # Load all media
        self.media = Media()
        self.media.load_fonts()
        self.media.load_graphics()
        self.media.load_audio()

        # Debug display
        if DEBUG_SHOW_FPS:
            self.fps_text = MyrmidonGame.write_text(0.0, 0.0, font = self.media.fonts['basic'], text = 0)
            self.fps_text.colour = (1, 1, 1, 1)
            self.fps_text.z = -2000

        # Set up starting game objects
        self.galaxy = Galaxy(self)
        self.gui = GUI(self)
        self.switch_game_state_to(GAME_STATE_SOLAR_SYSTEM)

        self.media.audio['ambient'].play(loops = -1)
        
        while True:

            # update debug display
            if DEBUG_SHOW_FPS:
                self.fps_text.text = "fps: " + str(MyrmidonGame.fps)
                
            yield


    def quit_game(self):
        sys.exit()


    def switch_game_state_to(self, state, gui_state = None):
        """
        Pass in a state and this will switch to it.
        It will also clean up everying necessary to go out of the
        previous game state.
        """
        # Undo and destroy everything in the current state
        self.gui.destroy_current_gui_state()
        col = (1.0, 1.0, 1.0)

        if self.game_state == GAME_STATE_SOLAR_SYSTEM:
            for x in self.solar_system_objects:
                x.signal(S_KILL)
            self.solar_system_objects = []
            self.player_ship.signal(S_KILL)
            self.background.signal(S_KILL)
        elif self.game_state == GAME_STATE_GALAXY:
            self.player_ship.signal(S_KILL)
            self.background.signal(S_KILL)

        # Switch to new state
        self.game_state = state

        # Create everything we require
        if state == GAME_STATE_GALAXY:
            self.background = Galaxy_background(self)
            self.gui.fade_toggle()            
            self.gui.switch_gui_state_to(GUI_STATE_GALAXY if gui_state is None else gui_state)
            self.player_ship = Galaxy_player_ship(self)
        elif state == GAME_STATE_SOLAR_SYSTEM:
            self.background = Galaxy_background(self)
            self.solar_system_objects = []
            self.solar_system_objects.append(Solar_system_star(self, self.galaxy.solar_systems[self.current_system]))
            self.gui.fade_toggle()            
            self.gui.switch_gui_state_to(GUI_STATE_SOLAR_SYSTEM if gui_state is None else gui_state)
            self.player_ship = Player_ship(self)


    def do_home_planet_results(self):
        if len(self.home_planet_result) > 0:
            result = self.home_planet_result.pop()
            result[0](self, *result[1])
        


if __name__ == '__main__':
    MyrmidonGame.screen_resolution = (1024, 768)
    MyrmidonGame.lowest_resolution = (1024, 768)
    MyrmidonGame.full_screen = False
    Game()

        
