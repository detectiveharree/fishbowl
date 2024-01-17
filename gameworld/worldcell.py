from enum import Enum
import numpy as np
from numpy import mean
import guiwindow
from gameworld.cell.cellresource.cellresource import RESOURCE_CELL_TYPE
from gameworld.cell.cell import CELL_CATEGORY
from humanbase import HumanState



class PersonRenderType(Enum):
    DEFAULT = 1
    GROUP = 2
    ATTRIBUTE = 3
    STATE = 4


class GroundTypeAttributes():

    def __init__(self, colour, is_buildable, is_explorable, is_farmable, can_farm_adjacent, can_place_stockpile, explorable_cost=-1):
        self.colour = colour
        self.is_buildable = is_buildable
        self.is_explorable = is_explorable
        self.explorable_cost = explorable_cost
        self.is_farmable = is_farmable
        self.can_farm_adjacent = can_farm_adjacent
        self.can_place_stockpile = can_place_stockpile

class GroundType(Enum):
    """
    DO NOT DELETE THIS. PASTE THIS IN FOR EVERY NEW OBJECT THAT WILL BE STORED IN A SET/DICTIONARY.
    THIS IS ESSENTIAL FOR MAKING SURE THE PROGRAM PERFORMS EXACTLY THE SAME EVERY TIME!

    assert(false) WILL CRASH THE PROGRAM IF YOU ATTEMPT TO PUT THIS OBJECT INTO A SET/DICT WITHOUT FIRST MODIFYING THE FUNCTION.
    THIS IS DONE ON PURPOSE TO PREVENT YOU FROM ACCIDENTALLY LEAKING NON-DETERMINISM INTO THE PROGRAM.
    SPEAK TO ME (TOM) AND I WILL EXPLAIN WHAT TO DO.
    """

    def __hash__(self):
        return hash(self.name)

    def __eq__(self, other):
        return self.__class__ == other.__class__ and self.name == other.name

    def __new__(cls, *args, **kwds):
        value = len(cls.__members__) + 1
        obj = object.__new__(cls)
        obj._value_ = value
        return obj

    def __init__(self, attributes):
        self.attributes = attributes

    def __repr__(self):
        return self.name

    GRASS = (GroundTypeAttributes(colour=(0, 255, 0), is_explorable=True, is_buildable=True, is_farmable=True, can_farm_adjacent=True, can_place_stockpile=True, explorable_cost=0),)
    MOUNTAIN = (GroundTypeAttributes(colour=(127, 127, 127), is_explorable=False, is_buildable=False, is_farmable=False, can_farm_adjacent=True, can_place_stockpile=False),)
    SALT_WATER = (GroundTypeAttributes(colour=(  0 ,0, 255), is_explorable=False, is_buildable=False, is_farmable=False, can_farm_adjacent=False, can_place_stockpile=False),)
    SAND = (GroundTypeAttributes(colour=(  255, 255, 0), is_explorable=True, is_buildable=True, is_farmable=False, can_farm_adjacent=False, can_place_stockpile=True),)
    DESERT = (GroundTypeAttributes(colour=(  255, 201, 14), is_explorable=True, is_buildable=True, is_farmable=False, can_farm_adjacent=False, can_place_stockpile=True),)
    RIVER = (GroundTypeAttributes(colour=(100, 100, 255), is_explorable=False, is_buildable=False, is_farmable=False, can_farm_adjacent=True, can_place_stockpile=False),)
    LAKE = (GroundTypeAttributes(colour=(97, 191, 255), is_explorable=False, is_buildable=False, is_farmable=False, can_farm_adjacent=True, can_place_stockpile=False),)
    SNOW = (GroundTypeAttributes(colour=(255, 255, 255), is_explorable=True, is_buildable=True, is_farmable=True, can_farm_adjacent=True, can_place_stockpile=True),)
    SWAMP = (GroundTypeAttributes(colour=(181, 230, 29), is_explorable=True, is_buildable=True, is_farmable=True, can_farm_adjacent=True, can_place_stockpile=True, explorable_cost=3),)
    SWAMP_WATER = (GroundTypeAttributes(colour=(102, 214, 122), is_explorable=True, is_buildable=False, is_farmable=False, can_farm_adjacent=True, can_place_stockpile=False, explorable_cost=10),)

# quick lookups
fast_look_up_colours = dict((ground_type.attributes.colour, ground_type) for ground_type in list(GroundType))



def colour_to_ground_type(rgb):
    if tuple(rgb) in fast_look_up_colours:
        return fast_look_up_colours[tuple(rgb)]
    return GroundType.GRASS

"""
Cells will contain data.
"""

class Cell():
    PERSONRENDERTYPE = PersonRenderType.DEFAULT

    """
    DO NOT DELETE THIS. PASTE THIS IN FOR EVERY NEW OBJECT THAT WILL BE STORED IN A SET/DICTIONARY.
    THIS IS ESSENTIAL FOR MAKING SURE THE PROGRAM PERFORMS EXACTLY THE SAME EVERY TIME!

    assert(false) WILL CRASH THE PROGRAM IF YOU ATTEMPT TO PUT THIS OBJECT INTO A SET/DICT WITHOUT FIRST MODIFYING THE FUNCTION.
    THIS IS DONE ON PURPOSE TO PREVENT YOU FROM ACCIDENTALLY LEAKING NON-DETERMINISM INTO THE PROGRAM.
    SPEAK TO ME (TOM) AND I WILL EXPLAIN WHAT TO DO.
    """
    def __hash__(self):
        assert(False)

    def __init__(self, x, y, rgb):
        self.location = (x, y)
        self.ground_type = colour_to_ground_type(rgb)

        # indicates if something exists on this cell
        self.cell_type = None

        self.people_on_cell = set()

        self.group_center = None

        # territory
        self.territory = None
        self.territory_colour = None


    def set_territory(self, group):
        if group is None:
            self.territory = None
            self.territory_colour = None
        else:
            self.territory = group.id_number
            self.territory_colour = group.colour


    def is_buildable(self):
        return self.ground_type.attributes.is_buildable and self.cell_type is None

    def is_harvestable_cell(self):
        return self.cell_type is not None and self.cell_type.get_cell_category() == CELL_CATEGORY.RESOURCE

    def is_farm(self):
        return self.cell_type is not None and self.cell_type.get_cell_type() == RESOURCE_CELL_TYPE.FARM

    def is_building(self):
        return self.cell_type is not None and self.cell_type.get_cell_category() == CELL_CATEGORY.BUILDING

    def is_farmable(self):
        return self.ground_type.attributes.is_farmable and self.is_buildable()

    def can_farm_adjacent(self):
        return self.ground_type.attributes.can_farm_adjacent or self.is_building()

    """
    Returns true if NPC can walk on it
    """
    def is_explorable(self):
        return self.ground_type.attributes.is_explorable

    """
    Returns colour of what the cell should be
    """
    def get_colour(self, render_territories, render_territories_on_top):
        base_colour = self.ground_type.attributes.colour

        # is farm only done like this because we want people to be rendered on top for debug reasons
        if self.is_farm():
            if not self.cell_type.get_debug_colour() is None:
                base_colour = self.cell_type.get_debug_colour()


        if render_territories:
            if self.territory_colour is not None:
                base_colour = self.territory_colour
                if render_territories_on_top:
                    return base_colour
        if self.people_on_cell:
            # self.get_person_colour()
            if Cell.PERSONRENDERTYPE == PersonRenderType.DEFAULT:
                base_colour = self.get_person_colour_default(base_colour)
            elif Cell.PERSONRENDERTYPE == PersonRenderType.GROUP:
                base_colour=  self.get_person_colour_by_group()
            elif Cell.PERSONRENDERTYPE == PersonRenderType.ATTRIBUTE:
                base_colour=  self.get_person_colour_by_attribute()
            elif Cell.PERSONRENDERTYPE == PersonRenderType.STATE:
                base_colour=  self.get_person_colour_by_state()
        # if self.resource_type == ResourceType.FOOD and self.being_harvested():
        #     base_colour= (155, 100, 100)
        # if self.resource_type == ResourceType.WOOD and self.being_harvested():
        #     base_colour= (16, 82, 36)

        if self.cell_type is not None:
            # is farm only done like this because we want people to be rendered on top for debug reasons
            if not self.is_farm():
                if not self.cell_type.get_debug_colour() is None:
                    base_colour = self.cell_type.get_debug_colour()
        if self.group_center:
            base_colour= (255, 255, 255)
        return base_colour



    """
    Returns the colour of the group if people are on it.
    Averages colorus together (i.e. multiple groups on one cell)
    """
    def get_person_colour_default(self, base_colour):
        for person in self.people_on_cell:
            return (255, 0, 0)
        return base_colour


    """
    Returns the colour of the group if people are on it.
    Averages colorus together (i.e. multiple groups on one cell)
    """
    def get_person_colour_by_group(self):
        colours = []
        for person in self.people_on_cell:
            colour = (255, 0, 0)
            if guiwindow.WORLD_INSTANCE.humanDict[person] is not None:
                colour = guiwindow.WORLD_INSTANCE.humanDict[person].group.colour

            colours.append(colour)
        return (tuple(map(mean, zip(*colours))))


    """
    Returns the colour of the group if people are on it.
    Averages colorus together (i.e. multiple groups on one cell)
    """
    def get_person_colour_by_attribute(self):
        colours = []
        for person in self.people_on_cell:
            colours.append(guiwindow.WORLD_INSTANCE.humanDict[person].personality.get_colour())
        return (tuple(map(mean, zip(*colours))))


    """
    Returns the colour of the group if people are on it.
    Averages colorus together (i.e. multiple groups on one cell)
    """
    def get_person_colour_by_state(self):
        colours = []
        for person in self.people_on_cell:
            if guiwindow.WORLD_INSTANCE.humanDict[person].state == HumanState.AWAKE:
                colours.append((255, 0, 0))
            elif guiwindow.WORLD_INSTANCE.humanDict[person].state == HumanState.SLEEPING:
                colours.append((0, 0, 255))

        return (tuple(map(mean, zip(*colours))))




    """
    Returns true if valid place for stockpile
    """
    def can_place_stockpile(self):
        return self.ground_type.attributes.can_place_stockpile


    def __repr__(self):
        output = ""
        output += "loc: %s\n" % str(self.location)
        output += "people_on_cell: %s\n" % str(self.people_on_cell)
        output += "group_center: %s\n" % str(self.group_center)
        output += "territory: %s\n" % str(self.territory)
        output += "ground_type: %s\n" % str(self.ground_type)
        if self.cell_type is not None:
            output += "cell info %s\n" % self.cell_type.get_cell_type()
            output += "location: %s\n" % self.cell_type.locations
            output += "interactable_locs: %s\n" % self.cell_type.interactable_locations
            output += "debug: %s\n" % self.cell_type.debug_info()
        return output











