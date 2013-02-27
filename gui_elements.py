# Engine imports
from myrmidon.myrmidon import MyrmidonProcess, MyrmidonGame, MyrmidonError
from myrmidon.consts import *
from pygame.locals import *

# OpenGL imports
from OpenGL.GL import *

# game imports
from consts import *
from helpers import *


class GUI_element(MyrmidonProcess):
    """
    All GUI elements extend from this template.
    It must have a position and a width/height. This enables it to take mouse input.
    The handle_input() method must only be directly called by the overall parent element, all
    children will be polled and the correct response will be sent back up the chain.
    The Z order matters for how elements will be polled.
    """
    parent = None
    children = []
    width = 0
    height = 0
    disable = False
    _currently_hovered = False
    
    def execute(self, game, parent = None):
        """
        Template, base all elements off this execute method.
        """
        self.game = game
        self.parent = parent
        self.init()
        while True:
            self.update()
            yield


    def init(self):
        """
        Must be called at the start of the execute method. Requres self.parent to be set though.
        """
        if not self.parent is None:
            self.parent.children.append(self)
        self.children = []
        self.priority = PRIORITY_GUI_ELEMENTS
        

    def update(self):
        """
        Stub designed to be called every frame.
        """
        pass


    def mouse_over(self):
        """
        Override this method to respond to the mouse hovering.
        Called AFTER mouse_enter if that method gets called.
        """
        pass


    def mouse_not_over(self):
        """
        Override this method to respond to the mouse not being over the element.
        Called AFTER mouse_out if that method gets called.
        """
        pass


    def mouse_enter(self):
        """
        Override this method to respond to the mouse entering the element.
        """
        pass


    def mouse_out(self):
        """
        Override this method if to respond to the mouse leaving the element.
        """
        pass


    def mouse_left_down(self):
        """
        Override this method to respond to the left mouse button being held down over the element.
        """
        pass


    def mouse_left_up(self):
        """
        Override this method to respond to the left mouse button being released on the element.
        """
        pass


    def mouse_right_down(self):
        """
        Override this method to respond to the right mouse button being held down over the element.
        """
        pass


    def mouse_right_up(self):
        """
        Override this method to respond to the right mouse button being released on the element.
        """
        pass

    
    def mouse_middle_down(self):
        """
        Override this method to respond to the middle mouse button being held down over the element.
        """
        pass


    def mouse_middle_up(self):
        """
        Override this method to respond to the middle mouse button being released on the element.
        """
        pass


    def mouse_wheel_down(self):
        """
        Override this method to respond to the mouse wheel spinning when the mouse is being held down over the element.
        """
        pass


    def mouse_wheel_up(self):
        """
        Override this method to respond to the mouse wheel spinning when the mouse is being held down over the element.
        """
        pass

        
    def handle_input(self, coordinates, current_best = None):
        """
        Returns the pointer to the GUI object that is under the screen coordinates passed in to the coordinates parameter.
        current_best should be None unless called from this method.
        """
        if self.disable:
            return current_best
        
        if self.is_coords_in_bounds(coordinates):
            if current_best is None or self.z <= current_best.z:
                current_best = self
        else:
            if self._currently_hovered:
                self.mouse_out()
                self._currently_hovered = False
            self.mouse_not_over()
            
        for child in self.children:
            current_best = child.handle_input(coordinates, current_best)

        return current_best


    def is_coords_in_bounds(self, coordinates):
        return (coordinates[0] > self.x and coordinates[0] < self.x + self.width and coordinates[1] > self.y and coordinates[1] < self.y + self.height)
    

    def on_exit(self):
        kids = list(self.children)
        for child in kids:
            child.signal(S_KILL)

        if not self.parent is None and self in self.parent.children:
            self.parent.children.remove(self)



class GUI_element_window_frame(GUI_element):
    draw_list = None

    def execute(self, game, parent, x, y, width, height):
        self.game = game
        self.parent = parent
        self.init()
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.z = self.parent.z + 1
        while True:
            self.update()
            yield


    def draw(self):        
        if self.draw_list == None:
            self.draw_list = glGenLists(1)
            glNewList(self.draw_list, GL_COMPILE_AND_EXECUTE)

            MyrmidonGame.engine['gfx'].draw_rectangle(
                (self.x + 12, self.y + 12),
                (self.width + self.x - 4, self.height + self.y - 4),
                colour = MyrmidonGame.engine['gfx'].rgb_to_colour((150, 100, 0, 200)),
                )

            MyrmidonGame.engine['gfx'].draw_rectangle(
                (self.x + 8, self.y + 8),
                (self.width + self.x - 8, self.height + self.y - 8),
                colour = (
                  MyrmidonGame.engine['gfx'].rgb_to_colour((230, 230, 230, 255)),
                  MyrmidonGame.engine['gfx'].rgb_to_colour((230, 230, 255, 255)),
                  MyrmidonGame.engine['gfx'].rgb_to_colour((200, 200, 200, 255)),
                  MyrmidonGame.engine['gfx'].rgb_to_colour((200, 200, 200, 255))
                  )
                )

            MyrmidonGame.engine['gfx'].draw_rectangle(
                (self.x + 10, self.y + 10),
                (self.width + self.x - 10, self.height + self.y - 10),
                colour = MyrmidonGame.engine['gfx'].rgb_to_colour((200, 128, 0, 255)),
                filled = False
                )

            MyrmidonGame.engine['gfx'].draw_rectangle(
                (self.x + 16, self.y + 6),
                (self.x + 250, self.y + 20),
                colour = MyrmidonGame.engine['gfx'].rgb_to_colour((200, 200, 200, 200)),
                )

            MyrmidonGame.engine['gfx'].draw_rectangle(
                (self.x + 10, self.y),
                (self.x + 244, self.y + 16),
                colour = MyrmidonGame.engine['gfx'].rgb_to_colour((255, 255, 255, 255)),
                )
        
            glColor4f(1.0, 1.0, 1.0, 1.0)       
            glEnable(GL_TEXTURE_2D)

            glEndList()
        else:
            glCallList(self.draw_list)



class GUI_element_window(GUI_element):
    title = ""
    height = 0
    width = 0
    frame = None
    text = None
    
    def init(self):
        GUI_element.init(self)
        self.frame = GUI_element_window_frame(self.game, self, self.x, self.y, self.width, self.height)
        self.text = MyrmidonGame.write_text(self.x+15, self.y+5, font = self.game.media.fonts['frame_titles'], text = self.title)
        self.text.colour = (0,0,0)
        self.text.z = self.z - 1

    
    def on_exit(self):
        GUI_element.on_exit(self)
        self.text.signal(S_KILL)



class GUI_element_button(GUI_element):
    generic_button = True
    generic_button_text = ""
    disabled = False
    
    generic_button_text_object = None
    sequence_count = 0
    draw_list = None
    
    def execute(self, game, parent = None):
        self.game = game
        self.parent = parent
        self.init()
        while True:
            self.update()
            yield


    def init(self):
        GUI_element.init(self)

        if not self.image is None:
            self.generic_button = False
            self.width = self.image.width if self.width == 0 else self.width
            self.height = self.image.height if self.height == 0 else self.height
        else:
            # Set up a generic button
            self.generic_button = True
            self.image = self.game.media.graphics['gui']['button_generic_background']
            
            # Create the text
            self.generic_button_text_object = MyrmidonGame.write_text(self.x + 5, self.y + 2, font = self.game.media.fonts['generic_buttons'], text = self.generic_button_text)
            self.generic_button_text_object.z = self.z - 1
            self.generic_button_text_object.colour = (0,0,0)
            
            # Set up the width, if we have a larger than normal width then we want to centre the text.
            if self.width > self.generic_button_text_object.text_image_size[0] + 10:
                self.generic_button_text_object.x += (self.width / 2) - (self.generic_button_text_object.text_image_size[0]/2) - 9
            else:
                self.width = self.generic_button_text_object.text_image_size[0] + 10

            # Fixed height, a little bit taller than the text
            self.height = self.generic_button_text_object.text_image_size[1] + 6

            # We dont want to do the default Myrmidon drawing, but we do want to do our own drawing
            self.normal_draw = False
            
        self.sequence_count = len(self.image.surfaces)


    def update(self):
        GUI_element.update(self)
        if self.disabled:
            self.image_seq = 3
            return
        self.image_seq = 0


    def mouse_left_up_toggle(self):
        if self.disabled:
            return


    def mouse_over(self):
        if self.disabled:
            return
        if self.sequence_count > 1:
            self.image_seq = 1


    def mouse_left_down(self):
        if self.disabled:
            return
        if self.sequence_count > 2:
            self.image_seq = 2


    def draw(self):
        if self.generic_button:
            x, y = self.get_screen_draw_position()
            
            self.generic_button_text_object.alpha = self.alpha
            if self.alpha > 0.0:

                if not self.clip is None:
                    glEnable(GL_SCISSOR_TEST)
                    glScissor(int(self.clip[0][0]), MyrmidonGame.screen_resolution[1] - int(self.clip[0][1]) - int(self.clip[1][1]), int(self.clip[1][0]), int(self.clip[1][1]))
                
                glEnable(GL_TEXTURE_2D)
                MyrmidonGame.engine['gfx'].last_image = self.image.surfaces[self.image_seq]
                glBindTexture(GL_TEXTURE_2D, self.image.surfaces[self.image_seq])
                glPushMatrix()
                glTranslatef(x, y, 0)
                glColor4f(1.0, 1.0, 1.0, self.alpha)

                if self.draw_list == None:
                    self.draw_list = glGenLists(1)
                    glNewList(self.draw_list, GL_COMPILE_AND_EXECUTE)
                    MyrmidonGame.engine['gfx'].draw_textured_quad(self.width, self.height, repeat = self.image)
                    glEndList()
                else:
                    glCallList(self.draw_list)

                MyrmidonGame.engine['gfx'].draw_rectangle(
                    (0, 0),
                    (self.width, self.height),
                    colour = MyrmidonGame.engine['gfx'].rgb_to_colour((27, 27, 27, 255 * self.alpha) if self.disabled else (255, 108, 0, 255 * self.alpha)),
                    filled = False,
                    noloadidentity = True,
                    width = 1
                    )

                glPopMatrix()

                if not self.clip == None:
                    glDisable(GL_SCISSOR_TEST)
                    

    def on_exit(self):
        GUI_element.on_exit(self)
        if self.generic_button:
            self.generic_button_text_object.signal(S_KILL)



class GUI_element_dialog_box(GUI_element):
    title = ""
    message = []
    
    frame = None
    title_text = None
    message_text = []
    caption_image_obj = None

    min_box_height = 95
    min_box_width = 300    
       
    def execute(self, game, parent = None, title = "test", message = ["test message"], confirm_callback = None):
        self.game = game
        self.parent = parent
        self.title = title
        self.message = message
        self.confirm_callback = confirm_callback
        self.init()
        while True:
            yield
        

    def init(self):
        GUI_element.init(self)
        self.z = Z_GUI_OBJECT_LEVEL_9

        self.width = MyrmidonGame.screen_resolution[0]
        self.height = MyrmidonGame.screen_resolution[1]

        # Create the title text objects
        self.title_text = MyrmidonGame.write_text(0, 0, font = self.game.media.fonts['frame_titles'], text = self.title)
        self.title_text.colour = (0,0,0)
        self.title_text.z = Z_GUI_OBJECT_LEVEL_10 - 1

        # Create all the message texts
        self.message_text = []

        y = 30
        max_text_width = None

        for msg in self.message:
            txt_obj = MyrmidonGame.write_text(0, y, font = self.game.media.fonts['dialog_box_text'], text = msg)
            txt_obj.colour = (0,0,0)
            txt_obj.z = Z_GUI_OBJECT_LEVEL_10 - 1
            self.message_text.append(txt_obj)
            y += txt_obj.text_image_size[1] + 2

            if max_text_width is None or txt_obj.text_image_size[0] > max_text_width:
                max_text_width = txt_obj.text_image_size[0]
            
        if max_text_width + 60 > self.min_box_width:
            self.min_box_width = max_text_width + 60

        self.min_box_height = self.min_box_height + (len(self.message_text) * self.message_text[0].text_image_size[1])

        self.frame_location_y = (MyrmidonGame.screen_resolution[1] / 2) - (self.min_box_height / 2)
        self.frame_location_x = (MyrmidonGame.screen_resolution[0] / 2) - (self.min_box_width / 2)

        self.frame = GUI_element_window_frame(self.game, self, self.frame_location_x, self.frame_location_y, self.min_box_width, self.min_box_height)
        self.frame.z = self.z - 1
        
        self.title_text.x = self.frame_location_x + 16
        self.title_text.y = self.frame_location_y + 4

        for txt_obj in self.message_text:
            txt_obj.x = self.frame_location_x + 28
            txt_obj.y += self.frame_location_y

        self.game.gui.block_gui_keyboard_input = True
        self.create_button_objects()        


    def create_button_objects(self):
        GUI_button_dialog_box_confirm(self.game, self, self.frame.x + (self.frame.width/2) - 27)

        
    def on_exit(self):
        GUI_element.on_exit(self)
        self.title_text.signal(S_KILL)
        for msg_obj in self.message_text:
            msg_obj.signal(S_KILL)
        self.game.gui.block_gui_keyboard_input = False
        

    def draw(self):
        MyrmidonGame.engine['gfx'].draw_rectangle(
            (self.x, self.y),
            (self.width + self.x, self.height + self.y),
            colour = (0, 0, 0, .4)
            )



class GUI_button_dialog_box_confirm(GUI_element_button):
    generic_button = True
    generic_button_text = "Okay"

    def execute(self, game, parent = None, x = 0):
        self.game = game
        self.parent = parent
        self.z = self.parent.frame.z - 1
        self.x = x
        self.y = self.parent.frame.y + self.parent.frame.height - 50
        self.init()
        while True:
            self.update()
            yield

    
    def mouse_left_up(self):
        if not self.parent.confirm_callback is None:
            self.parent.confirm_callback()
        self.parent.signal(S_KILL)
