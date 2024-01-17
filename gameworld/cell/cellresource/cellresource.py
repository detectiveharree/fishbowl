from gameworld.cell.cell import Cell, CELL_CATEGORY
from abc import ABC, abstractmethod
from items.itemresources.itemresource import ResourceType


from enum import Enum

class RESOURCE_CELL_TYPE(Enum):

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

    def __init__(self, harvestable_type):
        self.harvestable_type = harvestable_type


    BERRY_BUSH = (ResourceType.FOOD,)
    FARM = (ResourceType.FOOD,)
    FRESH_WATER = (ResourceType.WATER,)
    TREE = (ResourceType.WOOD,)

    WHITE_STEEL_ORE = (ResourceType.WHITE_STEEL,)
    IRON_ORE = (ResourceType.IRON,)
    DARK_IRON_ORE = (ResourceType.DARK_IRON,)
    BLACK_STEEL_ORE = (ResourceType.BLACK_STEEL,)
    BRASS_ORE = (ResourceType.BRASS,)
    BRONZE_ORE = (ResourceType.BRONZE,)
    ROCK = (ResourceType.STONE,)

    def __repr__(self):
        return self.name


class CellResource(Cell, ABC):

    """
    DO NOT DELETE THIS. PASTE THIS IN FOR EVERY NEW OBJECT THAT WILL BE STORED IN A SET/DICTIONARY.
    THIS IS ESSENTIAL FOR MAKING SURE THE PROGRAM PERFORMS EXACTLY THE SAME EVERY TIME!

    assert(false) WILL CRASH THE PROGRAM IF YOU ATTEMPT TO PUT THIS OBJECT INTO A SET/DICT WITHOUT FIRST MODIFYING THE FUNCTION.
    THIS IS DONE ON PURPOSE TO PREVENT YOU FROM ACCIDENTALLY LEAKING NON-DETERMINISM INTO THE PROGRAM.
    SPEAK TO ME (TOM) AND I WILL EXPLAIN WHAT TO DO.
    """
    def __hash__(self):
        return hash(self.locations)

    def __eq__(self, other):
        return self.__class__ == other.__class__ and self.locations == other.locations

    def __init__(self, locations):
        super(). __init__(locations)
        # helper such that we
        self.occupied_locations_helper = {}


    def begin_interact(self, coord, human):
        if self.interactable_locations is set():
            print("THIS SHOULD NOT BE GETTING CALLED")
            return False
        # print("%s | %s" % (self.interactable_locations, coord))
        super().begin_interact(coord, human)
        self.interactable_locations.remove(coord)
        self.occupied_locations_helper[human] = coord
        return True

    def end_interact(self, human):
        if human in self.occupied_locations_helper:
            super().end_interact(human)
            freed_location = self.occupied_locations_helper[human]
            del self.occupied_locations_helper[human]
            self.interactable_locations.add(freed_location)


    """
    Return the category of cell
    """
    @staticmethod
    def get_cell_category():
        return CELL_CATEGORY.RESOURCE

    """
    If loaded in from the the PNG, will place this cell type below it.
    """
    @staticmethod
    def get_loader_ground_cell_type():
        ...

    """
    If detecting this colour while loading will place this resource down.
    """
    @staticmethod
    @abstractmethod
    def get_loader_colour():
        return None


    """
    Called when attempt is made to harvest this item.
    Must return some amount.
    """
    def harvest(self, amount):
        return amount


