
# Python imports
import locale

# Engine imports
from myrmidon.myrmidon import MyrmidonProcess, MyrmidonGame, MyrmidonError
from myrmidon.consts import *
from pygame.locals import *

# OpenGL imports
from OpenGL.GL import *

# game imports
from consts import *
from helpers import *
from gui_elements import GUI_element, GUI_element_window, GUI_element_button, GUI_element_dialog_box


class GUI(MyrmidonProcess):
    gui_state = None
        
    current_visible_gui_elements = {
        GUI_STATE_GALAXY : {},
        GUI_STATE_SOLAR_SYSTEM : {}
        }

    current_game_state_gui_ticks = 0

    parent_window = None

    block_gui_keyboard_input = False

    block_gui_mouse_input = False

    fading = None
    fade_to = 0.0
    fade_speed = 50
    fading_done = False
    fading_callback = None


    def execute(self, game):
        self.game = game
        self.alpha = 1.0
        self.fading = 1.0
        self.fade_to = 0
        self.fading_done = True
        self.z = -5000
        self.priority = PRIORITY_GUI
        locale.setlocale(locale.LC_ALL, '')

        while True:            
            self.current_game_state_gui_ticks += 1

            # Specific state input
            if self.game.game_state == GAME_STATE_GALAXY:
                """
                GALAXY VIEW
                """
                if not self.block_gui_keyboard_input:
                    # Quit on escape
                    if MyrmidonGame.engine['input'].keyboard_key_released(K_ESCAPE):
                        self.game.quit_game()
            elif self.game.game_state == GAME_STATE_SOLAR_SYSTEM:
                """
                SOLAR SYSTEM VIEW
                """
                if not self.block_gui_keyboard_input:
                    # Quit on escape
                    if MyrmidonGame.engine['input'].keyboard_key_released(K_ESCAPE):
                        self.game.quit_game()

            # Handle overall gui input
            if not self.parent_window is None and not self.block_gui_mouse_input:
                mouse_over = self.parent_window.handle_input((MyrmidonGame.engine['input'].mouse.x, MyrmidonGame.engine['input'].mouse.y))
                if not mouse_over is None and not MyrmidonGame.engine['input'].disable_input:
                    
                    if not mouse_over._currently_hovered:
                        mouse_over.mouse_enter()
                        mouse_over._currently_hovered = True
                        
                    mouse_over.mouse_over()
                    
                    if MyrmidonGame.engine['input'].mouse.left:
                        mouse_over.mouse_left_down()
                    elif MyrmidonGame.engine['input'].mouse.left_up:
                        mouse_over.mouse_left_up()

                    if MyrmidonGame.engine['input'].mouse.right:
                        mouse_over.mouse_right_down()
                    elif MyrmidonGame.engine['input'].mouse.right_up:
                        mouse_over.mouse_right_up()

                    if MyrmidonGame.engine['input'].mouse.middle:
                        mouse_over.mouse_middle_down()
                    elif MyrmidonGame.engine['input'].mouse.middle_up:
                        mouse_over.mouse_middle_up()
                        
                    if MyrmidonGame.engine['input'].mouse.wheel_down:
                        mouse_over.mouse_wheel_down()
                    elif MyrmidonGame.engine['input'].mouse.wheel_up:
                        mouse_over.mouse_wheel_up()

            # Handle the fading stuff
            if not self.fading == None and self.fading_done == False:
                for i in range(self.fade_speed):
                    self.alpha = lerp(i, self.fade_speed, self.fading, self.fade_to)
                    yield
                self.fading = None
                self.fading_done = True
                if not self.fading_callback == None:
                    self.fading_callback()

            yield


    def draw(self):
        if self.alpha > 0:
            MyrmidonGame.engine['gfx'].draw_rectangle((0,0), (MyrmidonGame.screen_resolution[0], MyrmidonGame.screen_resolution[1]), colour = (0.0, 0.0, 0.0, self.alpha), filled = True)


    def switch_gui_state_to(self, state):
        self.destroy_current_gui_state()        
        self.gui_state = state
        self.current_game_state_gui_ticks = 0
        self.parent_window = None

        MyrmidonGame.engine['input'].mouse.visible = False
        MyrmidonGame.engine['input'].mouse.z = Z_MOUSE
        MyrmidonGame.engine['input'].mouse.image = self.game.media.graphics['gui']['cursor']
                        
        if self.gui_state == GUI_STATE_GALAXY:
            self.current_visible_gui_elements[GUI_STATE_GALAXY]['galaxy_container'] = GUI_galaxy_container(self.game)
            self.parent_window = self.current_visible_gui_elements[GUI_STATE_GALAXY]['galaxy_container']
            #self.current_visible_gui_elements[GUI_STATE_GALAXY]['fuel_meter'] = GUI_fuel_meter(self.game, self.parent_window)
            #self.current_visible_gui_elements[GUI_STATE_GALAXY]['money_meter'] = GUI_money_meter(self.game, self.parent_window)
            #self.current_visible_gui_elements[GUI_STATE_GALAXY]['crew_meter'] = GUI_crew_meter(self.game, self.parent_window)
        elif self.gui_state == GUI_STATE_SOLAR_SYSTEM:
            self.current_visible_gui_elements[GUI_STATE_SOLAR_SYSTEM]['container'] = GUI_solar_system_container(self.game)
            self.parent_window = self.current_visible_gui_elements[GUI_STATE_SOLAR_SYSTEM]['container']
            self.current_visible_gui_elements[GUI_STATE_SOLAR_SYSTEM]['fuel_meter'] = GUI_fuel_meter(self.game, self.parent_window)
            self.current_visible_gui_elements[GUI_STATE_SOLAR_SYSTEM]['money_meter'] = GUI_money_meter(self.game, self.parent_window)
            self.current_visible_gui_elements[GUI_STATE_SOLAR_SYSTEM]['crew_meter'] = GUI_crew_meter(self.game, self.parent_window)
            

    def destroy_current_gui_state(self):
        if self.gui_state is None:
            return
        for x in self.current_visible_gui_elements[self.gui_state]:
            self.current_visible_gui_elements[self.gui_state][x].signal(S_KILL)
        self.current_visible_gui_elements[self.gui_state] = {}


    def fade_toggle(self, callback = None, speed = 15, colour = (0.0, 0.0, 0.0)):
        if not self.fading_done:
            return

        self.fade_speed = speed
        self.fading_callback = callback
        self.fading = self.alpha
        self.fade_colour = colour
        self.fade_to = 1.0 if self.fading < 1.0 else 0.0
        self.fading_done = False



###################################################################################################
###################################################################################################
###################################### COMMON GUI #################################################
###################################################################################################
###################################################################################################



class GUI_fuel_meter(GUI_element):
    def execute(self, game, parent = None):
        self.game = game
        self.parent = parent
        self.image = self.game.media.graphics['gui']['fuel_meter']
        self.y = 5
        self.z = Z_GUI_OBJECT_LEVEL_8
        self.bar_width = 185.0
        self.init()
        while True:
            self.update()
            yield


    def draw(self):
        width = (self.bar_width / 100) * self.game.fuel
        if width > 1:
            MyrmidonGame.engine['gfx'].draw_rectangle(
                (self.x + 152, self.y + 20),
                (self.x + 152 + width, self.y + 20 + 11),
                colour = (.6, 1.0, 0.0, .5),
                filled = True
                )



class GUI_money_meter(GUI_element):
    def execute(self, game, parent = None):
        self.game = game
        self.parent = parent
        self.image = self.game.media.graphics['gui']['money_meter']
        self.y = MyrmidonGame.screen_resolution[1] - 55
        self.width = 400
        self.height = 50
        self.z = Z_GUI_OBJECT_LEVEL_8
        self.text = MyrmidonGame.write_text(self.x + 200, self.y + 8, font = self.game.media.fonts['money_meter'], text = "")
        self.text.z = self.z
        self.text.colour = (.8, .5, 0)
        self.init()        
        while True:
            self.update()            
            self.text.text = "$" + locale.format("%d", self.game.money, grouping=True)
            yield


    def on_exit(self):
        GUI_element.on_exit(self)
        self.text.signal(S_KILL)



class GUI_crew_meter(GUI_element):
    def execute(self, game, parent = None):
        self.game = game
        self.parent = parent
        self.x = 7
        self.y = 60
        self.z = Z_GUI_OBJECT_LEVEL_8
        self.text = MyrmidonGame.write_text(self.x, self.y, font = self.game.media.fonts['crew_meter'], text = "CREW COUNT")
        self.text.z = self.z
        self.text.colour = (1.0, .45, 0)
        self.init()
        while True:
            self.update()
            yield


    def draw(self):
        if self.game.crew == 0:
            return
        
        glPushMatrix()
        glColor4f(1.0, 1.0, 1.0, 1.0)
        glEnable(GL_TEXTURE_2D)
        glBindTexture(GL_TEXTURE_2D, self.game.media.graphics['gui']['crew_count'].surfaces[0])
        MyrmidonGame.engine['gfx'].last_image = self.game.media.graphics['gui']['crew_count'].surfaces[0]
        glTranslatef(220.0, 62.0, 0)
        for x in range(self.game.crew):
            MyrmidonGame.engine['gfx'].draw_textured_quad(self.game.media.graphics['gui']['crew_count'].width, self.game.media.graphics['gui']['crew_count'].width)
            glTranslatef(12.0, 0, 0)        
        glPopMatrix()


    def on_exit(self):
        GUI_element.on_exit(self)
        self.text.signal(S_KILL)




###################################################################################################
###################################################################################################
###################################### GALAXY VIEW ################################################
###################################################################################################
###################################################################################################



class GUI_galaxy_container(GUI_element):
    """
    All elements in the galaxy view live inside this thing.
    """    
    def execute(self, game, parent = None):
        self.game = game
        self.parent = parent
        self.init()
        self.z = Z_GUI_CONTAINERS
        self.width = MyrmidonGame.screen_resolution[0]
        self.height = MyrmidonGame.screen_resolution[1]
        
        # Create kids
        for star_name in self.game.galaxy.solar_systems:
            GUI_galaxy_solar_system(self.game, self, self.game.galaxy.solar_systems[star_name])

        GUI_fuel_meter(self.game, self)
        GUI_money_meter(self.game, self)
        GUI_crew_meter(self.game, self)
    
        while True:
            self.update()
            yield



class GUI_galaxy_solar_system(GUI_element):
    def execute(self, game, parent, solar_system):
        self.game = game
        self.parent = parent
        self.solar_system = solar_system
        self.z = Z_GUI_OBJECT_LEVEL_1
        self.image = self.game.media.graphics['space']['solar_system']
        self.x = self.solar_system.x
        self.y = self.solar_system.y
        self.scale = self.solar_system.scale
        self.colour = self.solar_system.colour
        self.width = self.image.width
        self.height = self.image.height
        self.init()
        self.nameplate = None
        while True:
            self.update()
            yield


    def mouse_left_up(self):
        self.game.gui.block_gui_mouse_input = True
        MyrmidonGame.engine['input'].mouse.alpha = 0
        self.game.player_ship.travel_to(self.solar_system)
        self.game.media.audio['galaxy_travel'].play()


    def mouse_not_over(self):
        self.scale = self.solar_system.scale
        if not self.nameplate is None:
            self.nameplate.die()
            self.nameplate = None


    def mouse_over(self):
        self.scale = self.solar_system.scale + .1
        if self.nameplate is None:
            self.nameplate = GUI_galaxy_solar_system_nameplate(self.game, self, self.solar_system)


    def is_coords_in_bounds(self, coordinates):        
        x = self.x - ((self.image.width/2) * self.scale)
        y = self.y - ((self.image.height/2) * self.scale)
        
        return (
            coordinates[0] > x and
            coordinates[0] < x + (self.width * self.scale) and
            coordinates[1] > y and
            coordinates[1] < y + (self.height * self.scale)
            )
            

    def get_screen_draw_position(self):
        return self.x - ((self.image.width/2) * self.scale), self.y - ((self.image.height/2) * self.scale)


    def on_exit(self):
        GUI_element.on_exit(self)
        if not self.nameplate is None:
            self.nameplate.signal(S_KILL)
            


class GUI_galaxy_solar_system_nameplate(MyrmidonProcess):
    def execute(self, game, parent, solar_system):
        self.game = game
        self.parent = parent
        self.solar_system = solar_system
        self.z = Z_GUI_OBJECT_LEVEL_5
        self.image = self.game.media.graphics['gui']['solar_system_nameplate']
        self.alpha = 0
        self.dying = False
        
        self.text = MyrmidonGame.write_text(0.0, 0.0, font = self.game.media.fonts['solar_system_nameplate'], text = self.solar_system.name)
        self.text.z = self.z-1
        self.text.colour = (1.0, 0.5, 0.0)

        self.text2 = MyrmidonGame.write_text(0.0, 0.0, font = self.game.media.fonts['solar_system_nameplate'], text = "Home" if solar_system.name == "Sol" else str(self.solar_system.chance_of_life) + "% chance of life.")
        self.text2.z = self.z-1
        self.text2.colour = (1.0, 0.5, 0.0)

        while True:
            if self.dying:
                if self.alpha > 0:
                    self.alpha -= .1
                if self.alpha <= 0:
                    self.signal(S_KILL)
            else:
                if self.alpha < 1:
                    self.alpha += .1
            self.x = MyrmidonGame.engine['input'].mouse.x
            self.y = MyrmidonGame.engine['input'].mouse.y - self.image.height
            
            self.text.x = self.x + 60
            self.text.y = self.y - 11
            self.text.alpha = self.alpha

            self.text2.x = self.x + 65
            self.text2.y = self.y + 7
            self.text2.alpha = self.alpha
            
            yield


    def die(self):
        self.dying = True


    def on_exit(self):
        self.text.signal(S_KILL)
        self.text2.signal(S_KILL)



###################################################################################################
###################################################################################################
################################# SOLAR SYSTEM VIEW ###############################################
###################################################################################################
###################################################################################################



class GUI_solar_system_container(GUI_element):
    """
    All elements in the solar system view live inside this thing.
    """    
    def execute(self, game, parent = None):
        self.game = game
        self.parent = parent
        self.init()
        self.z = Z_GUI_CONTAINERS
        self.width = MyrmidonGame.screen_resolution[0]
        self.height = MyrmidonGame.screen_resolution[1]
        
        # Create kids
        for object_name in self.game.galaxy.solar_systems[self.game.current_system].objects:
            GUI_solar_system_object(self.game, self, self.game.galaxy.solar_systems[self.game.current_system], self.game.galaxy.solar_systems[self.game.current_system].objects[object_name])

        if not self.game.current_object is None:
            GUI_solar_system_landed_menu(self.game, self)

        GUI_solar_system_leave_system_button(self.game, self)
        
        while True:
            self.update()
            yield



class GUI_solar_system_object(GUI_element):
    def execute(self, game, parent, solar_system, object):
        self.game = game
        self.parent = parent
        self.solar_system = solar_system
        self.object = object
        self.z = Z_GUI_OBJECT_LEVEL_2
        self.image = self.game.media.graphics['space']['planet_' + object.image]
        self.x = self.object.x
        self.y = self.object.y
        self.scale = self.object.scale
        self.colour = self.object.colour
        self.width = self.image.width
        self.height = self.image.height
        self.init()
        self.nameplate = None
        self.selected = False
        while True:
            self.update()
            yield


    def mouse_left_up(self):
        self.game.gui.block_gui_mouse_input = True
        MyrmidonGame.engine['input'].mouse.alpha = 0
        self.game.player_ship.travel_to(self.solar_system, self.object)
        self.game.media.audio['system_travel'].play()
        

    def mouse_not_over(self):
        self.selected = False
        if not self.nameplate is None:
            self.nameplate.die()
            self.nameplate = None


    def mouse_over(self):
        self.selected = True
        if self.nameplate is None:
            self.nameplate = GUI_solar_system_object_nameplate(self.game, self, self.object)


    def is_coords_in_bounds(self, coordinates):
        x = self.x - ((self.image.width/2) * self.scale)
        y = self.y - ((self.image.height/2) * self.scale)
        
        return (
            coordinates[0] > x and
            coordinates[0] < x + (self.width * self.scale) and
            coordinates[1] > y and
            coordinates[1] < y + (self.height * self.scale)
            )
            

    def get_screen_draw_position(self):
        return self.x - ((self.image.width/2) * self.scale), self.y - ((self.image.height/2) * self.scale)


    def draw(self):
        if self.selected == False or self.game.gui.block_gui_mouse_input:
            if not self.nameplate is None:
                self.nameplate.die()
                self.nameplate = None
            return
        glPushMatrix()
        MyrmidonGame.engine['gfx'].draw_circle((MyrmidonGame.screen_resolution[0]/2, MyrmidonGame.screen_resolution[1]/2), self.object.distance, colour = (1.0,.6,0,1.0), width = 1.0, accuracy = 32)
        MyrmidonGame.engine['gfx'].draw_circle((self.x, self.y), 128 * self.scale, colour = (1.0,.6,0,1.0), width = 2.0)
        glPopMatrix()



class GUI_solar_system_object_nameplate(MyrmidonProcess):
    def execute(self, game, parent, object):
        self.game = game
        self.parent = parent
        self.object = object
        self.z = Z_GUI_OBJECT_LEVEL_5
        self.image = self.game.media.graphics['gui']['solar_system_nameplate']
        self.alpha = 0
        self.dying = False
        
        self.text = MyrmidonGame.write_text(0.0, 0.0, font = self.game.media.fonts['solar_system_nameplate'], text = self.object.name)
        self.text.z = self.z-1
        self.text.colour = (1.0, 0.5, 0.0)

        while True:
            if self.dying:
                if self.alpha > 0:
                    self.alpha -= .1
                if self.alpha <= 0:
                    self.signal(S_KILL)
            else:
                if self.alpha < 1:
                    self.alpha += .1
            self.x = MyrmidonGame.engine['input'].mouse.x
            self.y = MyrmidonGame.engine['input'].mouse.y - self.image.height
            
            self.text.x = self.x + 60
            self.text.y = self.y - 11
            self.text.alpha = self.alpha

            yield


    def die(self):
        self.dying = True



class GUI_solar_system_landed_menu(GUI_element):
    def execute(self, game, parent = None):
        self.game = game
        self.parent = parent
        self.width = MyrmidonGame.screen_resolution[0]
        self.height = MyrmidonGame.screen_resolution[1]
        self.z = Z_GUI_OBJECT_LEVEL_6
        self.init()
        GUI_solar_system_landed_menu_window(self.game, self)
        while True:
            self.update()
            yield


    def draw(self):
        MyrmidonGame.engine['gfx'].draw_rectangle((0,0), (MyrmidonGame.screen_resolution[0], MyrmidonGame.screen_resolution[1]), colour = (0.0, 0.0, 0.0, .6), filled = True)



class GUI_solar_system_landed_menu_window(GUI_element_window):
    title = "Landed"
    def execute(self, game, parent = None):
        self.game = game
        self.parent = parent
        self.width = 700
        self.x = (MyrmidonGame.screen_resolution[0]/2) - (self.width/2)
        self.y = 100
        self.z = Z_GUI_OBJECT_LEVEL_7

        self.texts = []

        current_object = self.game.galaxy.solar_systems[self.game.current_system].objects[self.game.current_object]
        
        text = MyrmidonGame.write_text(self.x + 200, self.y + 30, font = self.game.media.fonts['landed_menu_title'], text = current_object.name)
        text.z = self.z -1
        text.colour = (0, 0, 0)
        self.texts.append(text)

        if len(current_object.description) > 0:
            start_y = 60
            for desc_line in current_object.description:
                text = MyrmidonGame.write_text(self.x + 180, self.y + start_y, font = self.game.media.fonts['landed_menu_description'], text = desc_line)
                text.z = self.z -1
                text.colour = (0, 0, 0)
                self.texts.append(text)
                start_y += 15

        self.height = 220

        # Do each action
        start_y = 170
        for action_name in current_object.actions:
            text = MyrmidonGame.write_text(self.x + 20, self.y + start_y, font = self.game.media.fonts['actions_description'], text = current_object.actions[action_name].description)
            text.z = self.z -1
            text.colour = (0, 0, 0)
            self.texts.append(text)            
            start_y += 30
            self.height += 30

        self.height += 20

        self.init()            

        # Do each action
        start_y = 170
        for action_name in current_object.actions:
            GUI_solar_system_landed_menu_window_action_button(self.game, self, current_object.actions[action_name], start_y)
            start_y += 30
        
        GUI_solar_system_landed_menu_window_planet(self.game, self, current_object.image, current_object.colour)
        self.launch_button = GUI_solar_system_landed_menu_window_launch(self.game, self)
        self.launch_error_text = MyrmidonGame.write_text(self.x + 20, self.y + self.height - 43, font = self.game.media.fonts['landed_menu_description'], text = "")
        self.launch_error_text.z = self.z -1
        self.launch_error_text.colour = (.8, 0, 0)
        self.texts.append(self.launch_error_text)

        yield
        
        # If this is our first time launching the game, we need to show the intro message
        if self.game.first_time:
            GUI_element_dialog_box(
                self.game,
                self.game.gui.parent_window,
                title = "The journey begins!",
                message = [
                    "This is it! The culmination of years of work.", "Finally SETI have gathered enough funding to build a space", "faring vessel of their own.",
                    "With it they will explore the nearest stars, but the ultimate ", "goal is of course the answer to the question;", "Are We Alone?"
                  ]
                )
            self.game.first_time = False            
        else:
            if self.game.current_system == "Sol" and self.game.current_object == "Earth":
                # Coming home empty handed is harsh.
                if len(self.game.home_planet_result) == 0 and self.game.money > 500000000:
                    GUI_element_dialog_box(
                        self.game,
                        self.game.gui.parent_window,
                        title = "Funding disaster",
                        message = [
                            "You have returned to Earth empty-handed and your benefactors are not impressed.",
                            "Your funding has been slashed as a result."
                          ]
                        )
                    self.game.money /= 2
                else:
                    # If we're on sol we need to do the results
                    self.game.do_home_planet_results()
        
        while True:
            self.check_can_launch()
            self.update()
            yield


    def check_can_launch(self):
        self.launch_button.disabled = True
        if self.game.fuel < 2:
            self.launch_error_text.text = "Require at least 2 units of fuel to launch!"
            return
        if self.game.crew == 0:
            self.launch_error_text.text = "Require at least 1 crew member to launch!"
            return
        self.launch_error_text.text = ""
        self.launch_button.disabled = False
        
        
    def on_exit(self):
        GUI_element_window.on_exit(self)
        for x in self.texts:
            x.signal(S_KILL)

            
    def draw(self):
        # The planet image box
        box_pos = (self.x + 20, self.y + 25)
        MyrmidonGame.engine['gfx'].draw_rectangle(
            box_pos,
            (box_pos[0] + 128, box_pos [1] + 128),
            colour = (0.0, 0.0, 0.0, 1.0),
            )
        MyrmidonGame.engine['gfx'].draw_rectangle(
            box_pos,
            (box_pos[0] + 128, box_pos [1] + 128),
            colour = (0.8, 0.4, 0.0, 1.0),
            width = 1.0,
            filled = False
            )

        # Line
        MyrmidonGame.engine['gfx'].draw_line(
            (self.x + 30, self.y + 160),
            (self.x + self.width - 30, self.y + 160),
            colour = (0.8, 0.4, 0.0, 1.0),
            width = 1.0
            )

        MyrmidonGame.engine['gfx'].draw_line(
            (self.x + 30, self.y + self.height - 60),
            (self.x + self.width - 30, self.y + self.height - 60),
            colour = (0.8, 0.4, 0.0, 1.0),
            width = 1.0
            )



class GUI_solar_system_landed_menu_window_planet(GUI_element):
    def execute(self, game, parent = None, image = "", colour = ()):
        self.game = game
        self.parent = parent
        self.x = self.parent.x + 20 - 64
        self.y = self.parent.y + 25 - 64
        self.z = Z_GUI_OBJECT_LEVEL_8
        self.init()
        self.image = self.game.media.graphics['space']['planet_' + image]
        self.colour = colour
        self.scale = .3
        self.scale_point = (self.image.width/2, self.image.height/2)
        while True:
            self.update()
            yield



class GUI_solar_system_landed_menu_window_launch(GUI_element_button):
    generic_button_text = "Launch"
    
    def execute(self, game, parent = None):
        self.game = game
        self.parent = parent
        self.x = self.parent.x + self.parent.width - 90
        self.y = self.parent.y + self.parent.height - 50
        self.z = Z_GUI_OBJECT_LEVEL_8
        self.init()
        while True:
            self.update()
            yield

    def mouse_left_up(self):
        if self.disabled:
            return        
        GUI_element_button.mouse_left_up(self)
        self.game.current_object = None        
        self.game.fuel -= FUEL_COST_TO_LAUNCH
        self.parent.parent.signal(S_KILL)
        


class GUI_solar_system_landed_menu_window_action_button(GUI_element_button):
    generic_button_text = ""
    
    def execute(self, game, parent = None, action = None, y = 0):
        self.game = game
        self.parent = parent
        self.action = action
        self.y = self.parent.y + y
        self.z = Z_GUI_OBJECT_LEVEL_9
        self.generic_button_text = self.action.button_text
        self.init()
        self.x = self.parent.x + self.parent.width - self.width - 30
        self.generic_button_text_object.x = self.parent.x + self.parent.width - self.width - 25

        if not self.game.current_system in self.game.actions_done:
            self.game.actions_done[self.game.current_system] = {}
        if not self.game.current_object in self.game.actions_done[self.game.current_system]:
            self.game.actions_done[self.game.current_system][self.game.current_object] = []

        if self.action.action_type in self.game.actions_done[self.game.current_system][self.game.current_object] and self.action.repeat == False:
            self.disabled = True
        
        while True:
            self.update()
            yield


    def mouse_left_up(self):
        GUI_element_button.mouse_left_up(self)
        if self.disabled:
            return        
        self.action.do_action()
        if self.action.repeat == False:
            self.disabled = True
        


class GUI_solar_system_leave_system_button(GUI_element_button):
    generic_button_text = "LEAVE SOLAR SYSTEM"
    
    def execute(self, game, parent = None):
        self.game = game
        self.parent = parent
        self.x = MyrmidonGame.screen_resolution[0] - 200
        self.y = MyrmidonGame.screen_resolution[1] - 40
        self.z = Z_GUI_OBJECT_LEVEL_3
        self.init()
        while True:
            self.update()
            yield


    def mouse_left_up(self):
        GUI_element_button.mouse_left_up(self)
        self.game.gui.fade_toggle(callback = lambda: self.game.switch_game_state_to(GAME_STATE_GALAXY))
