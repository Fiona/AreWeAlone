
# Python imports
import random
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
from gui_elements import GUI_element_dialog_box


class Galaxy(object):
    solar_systems = {}
    
    def __init__(self, game):
        self.game = game
        locale.setlocale(locale.LC_ALL, '')

        # Create systems
        # They add themselves to the galaxy
        Solar_system(self.game, self, "Sol", 445, 305)

        Solar_system(self.game, self, "Alpha Centauri", 480, 250, chance_of_life = 20)
        Solar_system(self.game, self, "Bernard's Star", 560, 360, chance_of_life = 10)
        Solar_system(self.game, self, "Wolf 359", 550, 420, chance_of_life = 12)
        Solar_system(self.game, self, "Lalande 21185", 725, 275, chance_of_life = 30)
        Solar_system(self.game, self, "Sirius", 610, 510, chance_of_life = 67)

        Solar_system(self.game, self, "Luyten 726-8", 259, 633, chance_of_life = 30)
        Solar_system(self.game, self, "Epsilon Eridani", 710, 100, chance_of_life = 60)
        Solar_system(self.game, self, "SCR 1845-6357", 800, 670, chance_of_life = 24)
        Solar_system(self.game, self, "Tau Ceti", 240, 540, chance_of_life = 75)
        Solar_system(self.game, self, "GJ 1061", 100, 300, chance_of_life = 18)

        Solar_system(self.game, self, "EZ Aquarii", 820, 600, chance_of_life = 25)
        Solar_system(self.game, self, "Procyon", 110, 210, chance_of_life = 16)
        Solar_system(self.game, self, "Kruger 60", 270, 310, chance_of_life = 3)
        Solar_system(self.game, self, "Struve 2399", 940, 450, chance_of_life = 25)

        # Ross 154
        # Ross 248
        # Lacaille 9352

        # Ross 128
        # 61 Cygni
        # Struve 2399

        # Groombridge 34
        # Epsilon Indi
        # DX Cancri

        # YZ Ceti
        # Luyten's Star
        # Teegarden's Star
        # Kapteyn's Star

        # Lacaille 8760
        # Ross 614
        # Wolf 1061
        # Van Maanen's Star

        # Gilese 1
        # Wolf 242
        # TZ Arteris
        # GJ 687
        # LHS 292

        # GJ 674
        # GJ 1245
        # AD Leonis
        # GJ 832
        # LHS 288

        

class Solar_system(object):
    name = "Foo"
    chance_of_life = 50
    objects = []
    
    def __init__(self, game, galaxy, name, x, y, chance_of_life = 50):
        self.game = game
        self.galaxy = galaxy
        self.name = name
        self.x = x
        self.y = y
        self.chance_of_life = chance_of_life
        self.scale = .3
        self.colour = (1.0, 1.0, 1.0)
        self.objects = {}

        self.galaxy.solar_systems[name] = self

        if self.name == "Sol":
            self.scale = .5
            self.colour = (1, 1, .6)
            Planet(
                self.game, self, distance = 100, name="Venus", image = "rocky", scale = .1,
                description = [
                    "Although named after the Roman godess of love,",
                    "there is little to love about a planet covered in",
                    "an atmosphere comprised of sulphuric acid."
                  ],
                actions = {
                    "mine" : Action(self.game, "Mine planet for resources", "Mine", ACTION_MINE, args = (0,)),
                  }                
                )
            Planet(
                self.game, self, distance = 150, name="Earth", image = "earth", scale = .15,
                description = [
                    "Our home planet, as it has been for thousands of years.",
                    "A small green blue marble in the infinite sea of space.",
                    "Could it be that we are alone on our pale blue dot?"
                  ],
                actions = {
                    "buy_fuel" : Action(self.game, "Fuel - 10 units $" + locale.format("%d", self.game.fuel_cost, grouping=True), "Purchase", ACTION_BUY_FUEL, repeat = True),
                    "buy_crew" : Action(self.game, "Hire crew member - $" + locale.format("%d", self.game.crew_cost, grouping=True), "Purchase", ACTION_BUY_CREW, repeat = True),
                  }
                )
            Planet(
                self.game, self, distance = 250, name="Mars", image = "rocky", scale = .2, colour = (1.0, .3, .3),
                description = [
                    "The red planet. Once a world covered in water,",
                    "now it is nothing but a desolate wastleland."
                  ],
                actions = {
                    "mine" : Action(self.game, "Mine planet for resources", "Mine", ACTION_MINE, args = (1,)),
                  }
                )
            Planet(
                self.game, self, distance = 360, name="Jupiter", image = "gas_giant", scale = .4,
                description = [
                    "The huge gas giant that dwarfs the  other",
                    "planets in our solar system.",
                    "It has long served as the Earth's protector against",
                    "sellar objects that would threaten us."
                  ],
                actions = {
                    "mine_gas" : Action(self.game, "Attempt to mine gas for fuel (DANGEROUS)", "Mine", ACTION_MINE_GAS, repeat = True),
                  }                
                )
        elif self.name == "Alpha Centauri":
            self.scale = .2
            self.colour = (.6, .6, 1)
            Planet(
                self.game, self, distance = 75, name="Alpha Centauri I", image = "rocky2", scale = .1, colour = (.2, .2, .2),
                description = [
                    "This charred husk of a planet is almost certainly", "worthless."
                  ],
                actions = {
                    "survey" : Action(self.game, "Survey planet", "Survey", ACTION_SURVEY_ALPHA_CENTAURI_I),
                    "mine" : Action(self.game, "Mine planet for resources", "Mine", ACTION_MINE, args = (0,)),
                  }
                )
            Planet(
                self.game, self, distance = 200, name="Alpha Centauri II", image = "rocky", scale = .4, colour = (1.0, 1.0, .6),
                description = [
                    "An large and completely empty desert planet.", "This planet appears to hold nothing of value."
                  ],
                actions = {
                    "survey" : Action(self.game, "Survey planet", "Survey", ACTION_SURVEY_ALPHA_CENTAURI_II),
                    "mine" : Action(self.game, "Mine planet for resources", "Mine", ACTION_MINE, args = (0,)),
                  }
                )
            Planet(
                self.game, self, distance = 400, name="Alpha Centauri III", image = "rocky2", scale = .2,
                description = [
                    "This little rock looks barren.", "It has no atmosphere to speak of."
                  ],
                actions = {
                    "survey" : Action(self.game, "Survey planet", "Survey", ACTION_SURVEY_ALPHA_CENTAURI_III),
                    "mine" : Action(self.game, "Mine planet for resources", "Mine", ACTION_MINE, args = (3,)),
                  }
                )
            
        elif self.name == "Bernard's Star":
            self.scale = .4
            self.colour = (.9, 1.0, 1.0)
            Planet(
                self.game, self, distance = 300, name="Bernard's Planet", image = "rocky2", scale = .8, colour = (.6, .6, 1.0),
                description = [
                    "Incredible! This planet is completely covered in a", "deep ocean. Could it hold signs of life?"
                  ],
                actions = {
                    "survey" : Action(self.game, "Survey planet", "Survey", ACTION_SURVEY_BERNARD_I),
                    "mine" : Action(self.game, "Mine planet for resources", "Mine", ACTION_MINE, args = (0,)),
                  }
                )

        elif self.name == "Wolf 359":
            self.scale = .5
            self.colour = (.9, .8, 1.0)
            Planet(
                self.game, self, distance = 250, name="Wolf 359 I", image = "gas_giant", scale = .4, colour = (.5, 1.0, .5),
                description = [
                    "One of the two gas giants in this system.",
                    "It glows a bright green."
                  ],
                actions = {
                    "mine_gas" : Action(self.game, "Attempt to mine gas for fuel (DANGEROUS)", "Mine", ACTION_MINE_GAS, repeat = True),
                  }                
                )
            Planet(
                self.game, self, distance = 400, name="Wolf 359 II", image = "gas_giant", scale = .8, colour = (.2, .2, .6),
                description = [
                    "A massive gas giant, it almost seems impossible for", "it to mantain it's orbit around Wolf 359."
                  ],
                actions = {
                    "mine_gas" : Action(self.game, "Attempt to mine gas for fuel (DANGEROUS)", "Mine", ACTION_MINE_GAS, repeat = True),
                  }                
                )

        elif self.name == "Lalande 21185":
            self.scale = .2
            self.colour = (.7, 1.0, 1.0)
            Planet(
                self.game, self, distance = 100, name="Lalande 21185 I", image = "rocky", scale = .1, colour = (1.0, 1.0, 1.0),
                description = [
                    "An unremarkable barren planet. It may be rich in", "resources, however."
                  ],
                actions = {
                    "mine" : Action(self.game, "Mine planet for resources", "Mine", ACTION_MINE, args = (4,)),
                  }                
                )
            Planet(
                self.game, self, distance = 225, name="Lalande 21185 II", image = "rocky", scale = .2, colour = (1.0, .8, 1.0),
                description = [
                    "A dull looking rock. It has an interesting", " atmosphere that demands further attention."
                  ],
                actions = {
                    "survey" : Action(self.game, "Survey planet", "Survey", ACTION_SURVEY_LALANDE_21185_II),
                    "mine" : Action(self.game, "Mine planet for resources", "Mine", ACTION_MINE, args = (0,))
                  }
                )
            Planet(
                self.game, self, distance = 300, name="Lalande 21185 III", image = "rocky", scale = .1, colour = (1.0, .8, .8),
                description = [
                    "Another empty planet."
                  ],
                actions = {
                    "mine" : Action(self.game, "Mine planet for resources", "Mine", ACTION_MINE, args = (0,))
                  }                
                )

        elif self.name == "Sirius":
            self.scale = .2
            self.colour = (1.0, 1.0, 1.0)
            Planet(
                self.game, self, distance = 200, name="Sirius I", image = "rocky", scale = .1, colour = (1.0, .6, .9),
                description = [
                    "An decidedly alien looking, bubble-gum pink planet"
                  ],
                actions = {
                    "survey" : Action(self.game, "Survey planet", "Survey", ACTION_SURVEY_SIRIUS_I),
                    "mine" : Action(self.game, "Mine planet for resources", "Mine", ACTION_MINE, args = (0,))
                  }                
                )
            Planet(
                self.game, self, distance = 350, name="Sirius II", image = "gas_giant", scale = .7, colour = (1.0, 1.0, 1.0),
                description = [
                    "Yet another unremarkable gas giant."
                  ],
                actions = {
                    "mine_gas" : Action(self.game, "Attempt to mine gas for fuel (DANGEROUS)", "Mine", ACTION_MINE_GAS, repeat = True),
                  }
                )

        elif self.name == "Luyten 726-8":
            self.scale = .3
            self.colour = (1.0, 1.0, 1.0)
            Planet(
                self.game, self, distance = 220, name="Luyten 726-8 I", image = "rocky", scale = .2, colour = (.8, 1.0, .8),
                description = [
                    "At first we think the scanners are malfunctioning", "but we soon confirm that this planet", "is covered in a massive jungle!"
                  ],
                actions = {
                    "survey" : Action(self.game, "Survey planet", "Survey", ACTION_SURVEY_LUYTEN_726_8_I),
                    "mine" : Action(self.game, "Mine planet for resources", "Mine", ACTION_MINE, args = (0,))
                  }                
                )
            Planet(
                self.game, self, distance = 350, name="Luyten 726-8 II", image = "gas_giant", scale = .7, colour = (1.0, 1.0, 1.0),
                description = [
                    "Yet another unremarkable gas giant."
                  ],
                actions = {
                    "mine_gas" : Action(self.game, "Attempt to mine gas for fuel (DANGEROUS)", "Mine", ACTION_MINE_GAS, repeat = True),
                  }
                )

        elif self.name == "Epsilon Eridani":
            self.scale = .3
            self.colour = (1.0, 1.0, .7)
            Planet(
                self.game, self, distance = 220, name="Epsilon Eridani I", image = "rocky", scale = .3, colour = (.6, .2, .2),
                description = [
                   "A very hot planet, it almost seems to be bubbling", "even from looking at the satellite images."
                  ],
                actions = {
                    "survey" : Action(self.game, "Survey planet", "Survey", ACTION_SURVEY_EPSILON_ERIDANI_I),
                    "mine" : Action(self.game, "Mine planet for resources", "Mine", ACTION_MINE, args = (2,))
                  }                
                )

        elif self.name == "EZ Aquarii":
            self.scale = .3
            self.colour = (1.0, .7, .7)
            Planet(
                self.game, self, distance = 200, name="EZ Aquarii I", image = "rocky", scale = .3, colour = (1.0, 1.0, 1.0),
                description = [
                    "An unremarkable barren planet. It may be rich in", "resources, however."
                  ],
                actions = {
                    "mine" : Action(self.game, "Mine planet for resources", "Mine", ACTION_MINE, args = (2,)),
                  }                
                )
            Planet(
                self.game, self, distance = 280, name="EZ Aquarii II", image = "rocky", scale = .2, colour = (.2, .2, .2),
                description = [
                    "A dark planet. Our readings suggest a hollow crust.", "We should investigate further."
                  ],
                actions = {
                    "survey" : Action(self.game, "Survey planet", "Survey", ACTION_SURVEY_EZ_AQUARII_II),
                    "mine" : Action(self.game, "Mine planet for resources", "Mine", ACTION_MINE, args = (0,)),
                  }                
                )

        elif self.name == "Procyon":
            self.scale = .3
            self.colour = (1.0, .7, .7)
            Planet(
                self.game, self, distance = 350, name="Procyon III", image = "gas_giant", scale = .7, colour = (1.0, 1.0, 1.0),
                description = [
                    "Yet another unremarkable gas giant."
                  ],
                actions = {
                    "mine_gas" : Action(self.game, "Attempt to mine gas for fuel (DANGEROUS)", "Mine", ACTION_MINE_GAS, repeat = True),
                  }
                )
            Planet(
                self.game, self, distance = 100, name="Procyon I", image = "rocky", scale = .3, colour = (1.0, 1.0, 1.0),
                description = [
                    "An unremarkable barren planet. It may be rich in", "resources, however."
                  ],
                actions = {
                    "mine" : Action(self.game, "Mine planet for resources", "Mine", ACTION_MINE, args = (2,)),
                  }                
                )
            Planet(
                self.game, self, distance = 100, name="Procyon II", image = "rocky2", scale = .3, colour = (1.0, 1.0, .2),
                description = [
                    "This planet has a strange atmosphere."
                  ],
                actions = {
                    "survey" : Action(self.game, "Survey planet", "Survey", ACTION_SURVEY_PROCYON_II),
                    "mine" : Action(self.game, "Mine planet for resources", "Mine", ACTION_MINE, args = (1,)),
                  }                
                )

        elif self.name == "Kruger 60":
            self.scale = .4
            self.colour = (.6, .7, 1.0)
            Planet(
                self.game, self, distance = 200, name="Kruger 60 I", image = "rocky", scale = .4, colour = (1.0, 1.0, .2),
                description = [
                    "An unremarkable barren planet. It may be rich in", "resources, however."
                  ],
                actions = {
                    "survey" : Action(self.game, "Survey planet", "Survey", ACTION_SURVEY_KRUGER_60_I),
                    "mine" : Action(self.game, "Mine planet for resources", "Mine", ACTION_MINE, args = (1,)),
                  }                
                )
            Planet(
                self.game, self, distance = 250, name="Kruger 60 II", image = "rocky", scale = .2, colour = (1.0, 1.0, .5),
                description = [
                    "An unremarkable barren planet. It may be rich in", "resources, however."
                  ],
                actions = {
                    "mine" : Action(self.game, "Mine planet for resources", "Mine", ACTION_MINE, args = (0,)),
                  }                
                )
            
        elif self.name == "Struve 2399":
            self.scale = .4
            self.colour = (.6, .7, 1.0)
            Planet(
                self.game, self, distance = 200, name="Struve 2399 I", image = "rocky2", scale = .3, colour = (.5, .5, .8),
                description = [
                    "An unremarkable barren planet. It may be rich in", "resources, however."
                  ],
                actions = {
                    "survey" : Action(self.game, "Survey planet", "Survey", ACTION_SURVEY_STRUVE_2399_I),
                    "mine" : Action(self.game, "Mine planet for resources", "Mine", ACTION_MINE, args = (2,)),
                  }                
                )
            Planet(
                self.game, self, distance = 400, name="Struve 2399 II", image = "gas_giant", scale = .4,
                description = [
                    "A large gas giant, appearing to", "protect the other planet in the system.", "Much like Jupiter."
                  ],
                actions = {
                    "mine_gas" : Action(self.game, "Attempt to mine gas for fuel (DANGEROUS)", "Mine", ACTION_MINE_GAS, repeat = True),
                  }                
                )

        

class Planet(object):
    def __init__(self, game, solar_system, distance = 100, name = "Foo", image = "rocky", scale = .5, colour = (1, 1, 1), description = [], actions = {}):
        self.game = game
        self.solar_system = solar_system
        self.distance = distance
        self.name = name
        self.image = image
        self.scale = scale
        self.colour = colour
        self.description = description
        self.x, self.y = MyrmidonGame.move_forward((MyrmidonGame.screen_resolution[0] / 2, MyrmidonGame.screen_resolution[1] / 2), self.distance, random.randrange(0, 360))
        self.actions = actions
        
        self.solar_system.objects[name] = self



class Action(object):
    
    def __init__(self, game, description, button_text, action_type, repeat = False, args = ()):
        self.game = game
        self.description = description
        self.button_text = button_text
        self.action_type = action_type
        self.repeat = repeat
        self.args = args


    def do_action(self):
        if self.game.crew == 0 and self.action_type not in (ACTION_BUY_CREW, ACTION_BUY_FUEL):
            GUI_element_dialog_box(
                self.game,
                self.game.gui.parent_window,
                title = "Cannot do action",
                message = ["You require a crew to do anything."]
                )
            return
        
        self.actions_to_method[self.action_type](self, *self.args)
        if not self.game.current_system in self.game.actions_done:
            self.game.actions_done[self.game.current_system] = {}
        if not self.game.current_object in self.game.actions_done[self.game.current_system]:
            self.game.actions_done[self.game.current_system][self.game.current_object] = []
        self.game.actions_done[self.game.current_system][self.game.current_object].append(self.action_type)
        

    # actions


    def action_buy_fuel(self):
        if self.game.money >= self.game.fuel_cost and self.game.fuel < 100:
            self.game.money -= self.game.fuel_cost
            self.game.fuel += 10
            if self.game.fuel > 100:
                self.game.fuel = 100


    def action_buy_crew(self):
        if self.game.money >= self.game.crew_cost and self.game.crew < MAX_CREW:
            self.game.money -= self.game.crew_cost
            self.game.crew += 1


    def action_mine(self, amount_to_mine = 0):
        if amount_to_mine == 0:
            message = ["Attempting to mine the planet yields no useful resources."]
        else:
            message = ["Mining the planet yields a number of plentiful resources.", "Selling them on Earth will provide money, useful for later expeditions."]
            self.game.home_planet_result.append((self.results_to_method[RESULT_SOLD_RESOURCES], (self.game.current_object, amount_to_mine)))

        if random.random() > .80:
            self.game.crew -= 1
            message.append("During the mining process one of your crew members was tragically killed.")

        GUI_element_dialog_box(
            self.game,
            self.game.gui.parent_window,
            title = "Mining result",
            message = message
            )

        self.game.media.audio['mine'].play()


    def action_mine_gas(self):
        self.game.fuel += 5
        if self.game.fuel > 100:
            self.game.fuel = 100
        message = ["You mine 5 units of fuel from the planet's atmosphere."]
        
        if random.random() > .50:
            self.game.crew -= 1
            message.append("During the mining process one of your crew members was tragically killed.")

        GUI_element_dialog_box(
            self.game,
            self.game.gui.parent_window,
            title = "Mining result",
            message = message
            )


    def action_survey_alpha_centauri_i(self):
        GUI_element_dialog_box(
            self.game,
            self.game.gui.parent_window,
            title = "Survey result",
            message = ["The heat from Alpha Centauri causes the space suit of one of your", "crew to explode in flames and he burns to death.", "The survey mission is permanently called off as a result."]
            )
        self.game.crew -= 1
        self.game.media.audio['survey'].play()        
        

    def action_survey_alpha_centauri_ii(self):
        GUI_element_dialog_box(
            self.game,
            self.game.gui.parent_window,
            title = "Survey result",
            message = ["As expected, the planet is devoid of anything of value.", "Some rocks are gathered to take back to Earth."]
            )
        self.game.home_planet_result.append( (self.results_to_method[RESULT_ALPHA_CENTAURI_II], ()) )
        self.game.media.audio['survey'].play()        


    def action_survey_alpha_centauri_iii(self):
        GUI_element_dialog_box(
            self.game,
            self.game.gui.parent_window,
            title = "Survey result",
            message = ["A survey of the planet's crust yields a heavy metal content, making the planet ripe for mining."]
            )
        self.game.media.audio['survey'].play()        
        

    def action_survey_bernard_i(self):
        GUI_element_dialog_box(
            self.game,
            self.game.gui.parent_window,
            title = "Survey result",
            message = ["The initial excitement of discovering this planet subsided as a complete survey", "of the planet found it held no life at all.", "The temperature of the water is too warm to contain any life. It's nearly boiling!", "We have gathered some of the planet's water to take back with us."]
            )
        self.game.home_planet_result.append( (self.results_to_method[RESULT_BERNARD_I], ()) )
        self.game.media.audio['survey'].play()        


    def action_survey_lalande_21185_ii(self):
        GUI_element_dialog_box(
            self.game,
            self.game.gui.parent_window,
            title = "Survey result",
            message = ["Indeed, the planet's atmosphere was interesting. Appearing to", "be made up of a gaseous lead-like compound.", "Not long after the planet survey started, rain began to fall.", "It was not long before it became apparent that the rain was", "infact solid lead pellets.", "While fleeing the planet, one of the survey team was struck", "by a particularly large chunk and died immediately."]
            )
        self.game.crew -= 1
        self.game.media.audio['survey'].play()        
        

    def action_survey_sirius_i(self):
        GUI_element_dialog_box(
            self.game,
            self.game.gui.parent_window,
            title = "Survey result",
            message = ["Although a very pretty planet, the survey yielded no interesting results.", "Of note is that crewman Matthews has decided to dub the newly", "discovered planet 'Cassidy' in honour of his daughter back home."]
            )
        self.game.home_planet_result.append( (self.results_to_method[RESULT_SIRIUS_I], ()) )
        self.game.media.audio['survey'].play()        


    def action_survey_luyten_726_8_i(self):
        GUI_element_dialog_box(
            self.game,
            self.game.gui.parent_window,
            title = "Survey result",
            message = ["The planet is covered in hundreds of thousands of different species", "of plant-life. Although not intelligent life, this is still an", "important and unprecedented find!", "Unfortunately, during the survey a massive Venus-flytrap-like plant swallowed", "and digested a crewman whole.", "We should get these plant samples back home to ensure his death was not in vain."]
            )
        self.game.home_planet_result.append( (self.results_to_method[RESULT_LUYTEN_726_8_I], ()) )
        self.game.media.audio['survey'].play()        

        
    def action_survey_epsilon_eridani_i(self):
        GUI_element_dialog_box(
            self.game,
            self.game.gui.parent_window,
            title = "Survey result",
            message = ["This is a rocky planet covered in seas and rivers of molten lava.", "Our scans indicate huge shafts, leading down to the", "core of the planet that are open on the surface.", "The survey team witness the spectacular display of one of these shafts erupting,", "but barely escape with their lives and decide to call off the survey mission"]
            )
        self.game.media.audio['survey'].play()        


    def action_survey_ez_aquarii_ii(self):
        GUI_element_dialog_box(
            self.game,
            self.game.gui.parent_window,
            title = "Survey result",
            message = ["The survey finds that the crust of the planet is not so hollow. Infact we quickly discover,", "to our excitement and surprise, that a large portion of the structure is organic.", "It transpires that the entire undecrust of the planet is a massive species of fungii!", "Indeed, there appears to be a single organism encompassing the entire mass.", "This is the largest single organism ever discovered in history!", "We should report our findings back home."]
            )
        self.game.home_planet_result.append( (self.results_to_method[RESULT_EZ_AQUARII_II], ()) )        
        self.game.media.audio['survey'].play()        


    def action_survey_procyon_ii(self):
        GUI_element_dialog_box(
            self.game,
            self.game.gui.parent_window,
            title = "Survey result",
            message = ["Initially the survey seemed fine. Samples of the soil and atmosphere were taken and the team", "returned to the ship. After a couple of hours the members of the survey team started to act oddly.", "They exhibited symptoms of extreme paranoia and distrust.", "It was too late to help a small number of crewmen before it was discovered", "that a toxin in the atmosphere of the planet somehow infected them.", "They were found to have commited suicide."]
            )
        self.game.crew -= 3
        if self.game.crew < 0:
            self.game.crew = 0            
        self.game.media.audio['survey'].play()


    def action_survey_kruger_60_i(self):
        GUI_element_dialog_box(
            self.game,
            self.game.gui.parent_window,
            title = "Survey result",
            message = ["This planet is very interesting indeed, a huge section of the crust appears to have been dug out.", "The long, winding tunnels remind of ants nests.", "Unfortunately, we have discovered that the tunnels are natural, formed by", "flowing water that has long since vanished."]
            )
        self.game.media.audio['survey'].play()        


    def action_survey_struve_2399_i(self):
        GUI_element_dialog_box(
            self.game,
            self.game.gui.parent_window,
            title = "Survey result",
            message = ["At first we were ready to dismiss this planet. Although it had some interesting vegitation,", "once we got to the surface we made the most incredible discovery of our lives.", "We saw beasts, the likes of which we have never seen. And hundreds of incredible insects flying", "past our heads.", "Although we were already over the moon, nothing could have prepared us for what we found next.", "", "We observed a group of intelligent extra terrestrials.", "They appeared to be in a tribal stage of development.", "We did not introduce ourselves and only watched from afar.", "That is far out of our league. Still, we MUST make it back home to report our findings."]
            )
        self.game.home_planet_result.append((self.results_to_method[RESULT_STRUVE_2399_I], ()))
        self.game.media.audio['survey'].play()        

    
    actions_to_method = {
        ACTION_BUY_FUEL : action_buy_fuel,
        ACTION_BUY_CREW : action_buy_crew,
        ACTION_MINE : action_mine,
        ACTION_MINE_GAS : action_mine_gas,
        ACTION_SURVEY_ALPHA_CENTAURI_I : action_survey_alpha_centauri_i,
        ACTION_SURVEY_ALPHA_CENTAURI_II : action_survey_alpha_centauri_ii,
        ACTION_SURVEY_ALPHA_CENTAURI_III : action_survey_alpha_centauri_iii,
        ACTION_SURVEY_BERNARD_I : action_survey_bernard_i,
        ACTION_SURVEY_LALANDE_21185_II : action_survey_lalande_21185_ii,
        ACTION_SURVEY_SIRIUS_I : action_survey_sirius_i,
        ACTION_SURVEY_LUYTEN_726_8_I : action_survey_luyten_726_8_i,
        ACTION_SURVEY_EPSILON_ERIDANI_I : action_survey_epsilon_eridani_i,
        ACTION_SURVEY_EZ_AQUARII_II : action_survey_ez_aquarii_ii,
        ACTION_SURVEY_PROCYON_II : action_survey_procyon_ii,
        ACTION_SURVEY_KRUGER_60_I : action_survey_kruger_60_i,
        ACTION_SURVEY_STRUVE_2399_I : action_survey_struve_2399_i,
        }


    # Home planet results


    def result_sold_resources(game, planet_name, amount_sold):
        money_yield = 1500020407 * amount_sold
        game.money += money_yield

        GUI_element_dialog_box(
            game,
            game.gui.parent_window,
            title = "Result",
            message = ["Selling the resources gathered from " + planet_name, "nets $" + locale.format("%d", money_yield, grouping=True) + "."],
            confirm_callback = game.do_home_planet_results
            )


    def result_alpha_centauri_ii(game):
        money_yield = 500053031
        game.money += money_yield

        GUI_element_dialog_box(
            game,
            game.gui.parent_window,
            title = "Result",
            message = ["The rocks you brought back from Alpha Centauri II go down a", "treat with the boys back home.", "A small amount of money has been donated."],
            confirm_callback = game.do_home_planet_results
            )


    def result_bernard_i(game):
        money_yield = 2040043732
        game.money += money_yield

        GUI_element_dialog_box(
            game,
            game.gui.parent_window,
            title = "Result",
            message = ["After examination, the water you brought back from Bernard's Planet apparently exhibited", "some extraordinary properties.", "Immediately after this news was delivered to your team a group of government agents arrived.", "They sieze the water sample and offer your team a large amount of money in exchange for", "your silence on the matter.", "Naturally, you comply."],
            confirm_callback = game.do_home_planet_results
            )


    def result_sirius_i(game):
        GUI_element_dialog_box(
            game,
            game.gui.parent_window,
            title = "Result",
            message = ["After finding about the planet named after her in the Sirius system, Cassidy Matthews", "has sent the whole team a big thank you card.", "That was nice."],
            confirm_callback = game.do_home_planet_results
            )


    def result_luyten_726_8_i(game):
        money_yield = 4040043732
        game.money += money_yield

        message = ["The discovery of the jungle planet of Luyten 726-8 I has been hailed", "as one of the most important of our time.", "As a result a significant injection of funds has been pumped into the project."]

        if game.crew < MAX_CREW:
            message.append("A very influential scientist has also joined the crew on the back of this.")
            game.crew += 1

        GUI_element_dialog_box(
            game,
            game.gui.parent_window,
            title = "Result",
            message = message,
            confirm_callback = game.do_home_planet_results
            )


    def result_ez_aquarii_ii(game):
        money_yield = 1040043732
        game.money += money_yield

        message = ["Although the team attempted to explain the importance of finding", "the huge fungii organism on EZ Aquarii II, it transpires", "that fungii just doesn't excite people as much as it should.", "No amount of graphs and charts could convince your benefactors to give a", "larger budget, they instead gave you a small amount just", "to get yout out of the boardroom."]

        GUI_element_dialog_box(
            game,
            game.gui.parent_window,
            title = "Result",
            message = message,
            confirm_callback = game.do_home_planet_results
            )


    def result_struve_2399_i(game):
        money_yield = 100040043732
        game.money += money_yield

        message = ["It's been a week since we returned from our discovery at Struve 2399.", "Images and videos of the lifeforms have been shown all over the world.", "Now everyone knows, WE ARE NOT ALONE.", "Untold riches are now ours from countless interviews, book deals and guest lectures.", "But, there's still a galaxy out there to explore.", "Somehow it doesn't seem right to leave it alone.", "", "", "[YOU WIN! THANKS FOR PLAYING!]"]

        GUI_element_dialog_box(
            game,
            game.gui.parent_window,
            title = "Result",
            message = message,
            confirm_callback = game.do_home_planet_results
            )

        
    results_to_method = {
        RESULT_SOLD_RESOURCES : result_sold_resources,
        RESULT_ALPHA_CENTAURI_II : result_alpha_centauri_ii,
        RESULT_BERNARD_I : result_bernard_i,
        RESULT_SIRIUS_I : result_sirius_i,
        RESULT_LUYTEN_726_8_I : result_luyten_726_8_i,
        RESULT_EZ_AQUARII_II : result_ez_aquarii_ii,
        RESULT_STRUVE_2399_I : result_struve_2399_i,        
        }
