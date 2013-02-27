
# Engine imports
from myrmidon.myrmidon import MyrmidonProcess, MyrmidonGame, MyrmidonError
from myrmidon.consts import *
from pygame.locals import *

# OpenGL imports
from OpenGL.GL import *

# game imports
from consts import *
from helpers import *
from gui import GUI_solar_system_landed_menu


class Galaxy_background(MyrmidonProcess):
    def execute(self, game):
        self.game = game
        self.z = Z_BACKGROUND            
        while True:
            yield


    def draw(self):
        glPushMatrix()
        glColor4f(1.0, 1.0, 1.0, 1.0)
        glEnable(GL_TEXTURE_2D)
        glBindTexture(GL_TEXTURE_2D, self.game.media.graphics['space']['starfield'].surfaces[0])
        MyrmidonGame.engine['gfx'].last_image = self.game.media.graphics['space']['starfield'].surfaces[0]
        MyrmidonGame.engine['gfx'].draw_textured_quad(MyrmidonGame.screen_resolution[0], MyrmidonGame.screen_resolution[1], repeat = self.game.media.graphics['space']['starfield'])
        glPopMatrix()
        



class Solar_system_star(MyrmidonProcess):
    def execute(self, game, solar_system):
        self.game = game
        self.z = Z_GUI_OBJECT_LEVEL_1
        self.image = self.game.media.graphics['space']['solar_system']
        self.x = MyrmidonGame.screen_resolution[0]/2
        self.y = MyrmidonGame.screen_resolution[1]/2
        self.colour = solar_system.colour
        while True:
            yield


    def get_screen_draw_position(self):
        return self.x - (self.image.width/2), self.y - (self.image.height/2)



class Player_ship(MyrmidonProcess):
    do_travel_to = None
    
    def execute(self, game):
        self.game = game
        if self.game.current_object is None:
            self.x = MyrmidonGame.screen_resolution[0] / 2
            self.y = MyrmidonGame.screen_resolution[1] - 100
            self.rotation = -90
        else:
            current_object = self.game.galaxy.solar_systems[self.game.current_system].objects[self.game.current_object]
            self.x, self.y = current_object.x, current_object.y
        self.z = Z_PLAYER_SHIP
        self.image = self.game.media.graphics['space']['player_ship']
        while True:
            
            if not self.do_travel_to is None and self.game.fuel >= 0:
                rotation_towards_target = MyrmidonGame.angle_between_points(
                    (self.x, self.y),
                    (self.do_travel_to[1].x, self.do_travel_to[1].y)
                )
                self.rotation = MyrmidonGame.near_angle(
                    self.rotation,
                    rotation_towards_target,
                    2.0
                )
                self.move_forward(1.0)
                if self.get_distance((self.do_travel_to[1].x, self.do_travel_to[1].y)) < 8 :
                    self.game.current_object = self.do_travel_to[1].name
                    self.do_travel_to = None
                    GUI_solar_system_landed_menu(self.game, self.game.gui.current_visible_gui_elements[GUI_STATE_SOLAR_SYSTEM]['container'])
                    self.game.gui.block_gui_mouse_input = False
                    MyrmidonGame.engine['input'].mouse.alpha = 1.0

                self.travel_time += 1
                if self.travel_time == 360:
                    self.travel_time = 0
                    self.game.fuel -= 1
                    
            yield
    

    def get_screen_draw_position(self):
        return self.x - (self.image.width/2), self.y - (self.image.height/2)


    def travel_to(self, solar_system_object, object_object):
        self.travel_time = 0
        self.do_travel_to = (solar_system_object, object_object)



class Galaxy_player_ship(MyrmidonProcess):
    do_travel_to = None
    
    def execute(self, game):
        self.game = game
        current_system = self.game.galaxy.solar_systems[self.game.current_system]
        self.x, self.y = current_system.x, current_system.y
        self.z = Z_PLAYER_SHIP
        self.image = self.game.media.graphics['space']['player_ship']
        while True:

            if not self.do_travel_to is None and self.game.fuel >= 0:
                rotation_towards_target = MyrmidonGame.angle_between_points(
                    (self.x, self.y),
                    (self.do_travel_to.x, self.do_travel_to.y)
                )
                self.rotation = MyrmidonGame.near_angle(
                    self.rotation,
                    rotation_towards_target,
                    1.0
                )
                self.move_forward(.5)
                if self.get_distance((self.do_travel_to.x, self.do_travel_to.y)) < 8 :
                    self.game.current_system = self.do_travel_to.name
                    self.do_travel_to = None
                    self.game.gui.block_gui_mouse_input = False
                    MyrmidonGame.engine['input'].mouse.alpha = 1.0
                    self.game.gui.fade_toggle(callback = lambda: self.game.switch_game_state_to(GAME_STATE_SOLAR_SYSTEM))

                self.travel_time += 1
                if self.travel_time == 60:
                    self.travel_time = 0
                    self.game.fuel -= 1
            
            yield


    def get_screen_draw_position(self):
        return self.x - (self.image.width/2), self.y - (self.image.height/2)


    def travel_to(self, solar_system_object):
        self.travel_time = 0
        self.do_travel_to = solar_system_object
