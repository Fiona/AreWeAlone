# Python imports
import os

# Engine imports
from myrmidon.myrmidon import MyrmidonGame, MyrmidonProcess
from myrmidon.consts import *


class Media(object):
    fonts = {}
    graphics = {}
    audio = {}
    

    def load_fonts(self):
        self.fonts = {}
        self.fonts['basic'] = MyrmidonGame.engine['window'].load_font(os.path.join("fnt", "aurulent.ttf"), size = 13)
        self.fonts['solar_system_nameplate'] = MyrmidonGame.engine['window'].load_font(os.path.join("fnt", "bitmap.ttf"), size = 9)
        self.fonts['money_meter'] = MyrmidonGame.engine['window'].load_font(os.path.join("fnt", "hanzel.ttf"), size = 28)
        self.fonts['crew_meter'] = MyrmidonGame.engine['window'].load_font(os.path.join("fnt", "hanzel.ttf"), size = 18)
        self.fonts['frame_titles'] = MyrmidonGame.engine['window'].load_font(os.path.join("fnt", "bitmap.ttf"), size = 9)
        self.fonts['landed_menu_title'] = MyrmidonGame.engine['window'].load_font(os.path.join("fnt", "hanzel.ttf"), size = 20)
        self.fonts['landed_menu_description'] = MyrmidonGame.engine['window'].load_font(os.path.join("fnt", "aurulent.ttf"), size = 15)
        self.fonts['generic_buttons'] = self.fonts['landed_menu_description']
        self.fonts['actions_description'] = MyrmidonGame.engine['window'].load_font(os.path.join("fnt", "aurulent.ttf"), size = 17)
        self.fonts['dialog_box_text'] = self.fonts['actions_description']


    def load_graphics(self):
        self.graphics = {}
        self.graphics['gui'] = {}
        self.graphics['gui']['cursor'] = MyrmidonGame.engine['gfx'].Image(os.path.join("gfx", "gui", "cursor.png"))
        self.graphics['gui']['solar_system_nameplate'] = MyrmidonGame.engine['gfx'].Image(os.path.join("gfx", "gui", "solar_system_nameplate.png"))
        self.graphics['gui']['fuel_meter'] = MyrmidonGame.engine['gfx'].Image(os.path.join("gfx", "gui", "fuel_meter.png"))
        self.graphics['gui']['money_meter'] = MyrmidonGame.engine['gfx'].Image(os.path.join("gfx", "gui", "money_meter.png"))
        self.graphics['gui']['crew_count'] = MyrmidonGame.engine['gfx'].Image(os.path.join("gfx", "gui", "crew_count.png"))
        self.graphics['gui']['button_generic_background'] = MyrmidonGame.engine['gfx'].Image(os.path.join("gfx", "gui", "button_generic_background.png"), sequence = True, width = 1, height = 16)

        self.graphics['space'] = {}
        self.graphics['space']['player_ship'] = MyrmidonGame.engine['gfx'].Image(os.path.join("gfx", "space", "player_ship.png"))
        self.graphics['space']['starfield'] = MyrmidonGame.engine['gfx'].Image(os.path.join("gfx", "space", "starfield.png"), for_repeat = True)
        self.graphics['space']['solar_system'] = MyrmidonGame.engine['gfx'].Image(os.path.join("gfx", "space", "solar_system.png"))
        self.graphics['space']['planet_rocky'] = MyrmidonGame.engine['gfx'].Image(os.path.join("gfx", "space", "planet_rocky.png"))
        self.graphics['space']['planet_rocky2'] = MyrmidonGame.engine['gfx'].Image(os.path.join("gfx", "space", "planet_rocky2.png"))
        self.graphics['space']['planet_earth'] = MyrmidonGame.engine['gfx'].Image(os.path.join("gfx", "space", "planet_earth.png"))
        self.graphics['space']['planet_gas_giant'] = MyrmidonGame.engine['gfx'].Image(os.path.join("gfx", "space", "planet_gas_giant.png"))


    def load_audio(self):
        self.audio = {}
        self.audio['ambient'] = MyrmidonGame.engine['audio'].load_audio_from_file(os.path.join("audio", "ambient.ogg"))
        self.audio['galaxy_travel'] = MyrmidonGame.engine['audio'].load_audio_from_file(os.path.join("audio", "galaxy_travel.wav"))
        self.audio['system_travel'] = MyrmidonGame.engine['audio'].load_audio_from_file(os.path.join("audio", "system_travel.wav"))
        self.audio['mine'] = MyrmidonGame.engine['audio'].load_audio_from_file(os.path.join("audio", "mine.wav"))
        self.audio['survey'] = MyrmidonGame.engine['audio'].load_audio_from_file(os.path.join("audio", "survey.wav"))
