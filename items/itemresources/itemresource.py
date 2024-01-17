from items.itemcraftable import ItemCraftable
from items.item import Item
from ai.humanai.skill import SKILL_TYPE
from enum import Enum
import global_params

class GROUP_BUFFER_FACTOR(Enum):

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

    def __init__(self, default_harvest_rate_tick, associated_human_skill):
        self.default_harvest_rate_tick = default_harvest_rate_tick
        self.associated_human_skill = associated_human_skill

    def get_estimated_hourly_rate(self):
        return self.default_harvest_rate_tick * global_params.hourly_ticks

    def get_estimated_hours(self, amount):
        return amount / (self.get_estimated_hourly_rate())

    FOOD_HARVESTING = (20, SKILL_TYPE.FOOD_HARVESTING)
    WATER_HARVESTING = (20, SKILL_TYPE.WATER_HARVESTING)
    WOOD_HARVESTING = (20, SKILL_TYPE.WOOD_HARVESTING)
    BLACK_STEEL_HARVESTING = (20, SKILL_TYPE.MINING)
    BRASS_HARVESTING = (20, SKILL_TYPE.MINING)
    BRONZE_HARVESTING = (20, SKILL_TYPE.MINING)
    DARK_IRON_HARVESTING = (20, SKILL_TYPE.MINING)
    IRON_HARVESTING = (20, SKILL_TYPE.MINING)
    WHITE_STEEL_HARVESTING = (20, SKILL_TYPE.MINING)
    STONE_HARVESTING = (20, SKILL_TYPE.MINING)
    CRAFTING = (20, SKILL_TYPE.CRAFTING)
    BUILDING = (20, SKILL_TYPE.BUILDING)


    def __repr__(self):
        return self.name

class ResourceType(Enum):

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

    def __init__(self, skill_association, group_buffer_factor_association, optimal_weight, tier):
        self.skill_association = skill_association
        self.group_buffer_factor_association = group_buffer_factor_association
        self.optimal_weight = optimal_weight
        self.tier = tier # higher the worst

    def __str__(self):
        return self.name

    def __repr__(self):
        return str(self)

    # damage | speed | protection | tier
    FOOD = (SKILL_TYPE.FOOD_HARVESTING, GROUP_BUFFER_FACTOR.FOOD_HARVESTING, -1, -1)
    WATER = (SKILL_TYPE.WATER_HARVESTING, GROUP_BUFFER_FACTOR.WATER_HARVESTING, -1, -1)
    WOOD = (SKILL_TYPE.WOOD_HARVESTING, GROUP_BUFFER_FACTOR.WOOD_HARVESTING,-1, -1)
    STONE = (SKILL_TYPE.MINING, GROUP_BUFFER_FACTOR.STONE_HARVESTING, -1, -1)

    WHITE_STEEL = (SKILL_TYPE.MINING, GROUP_BUFFER_FACTOR.WHITE_STEEL_HARVESTING, 0.5, 1)
    IRON = (SKILL_TYPE.MINING, GROUP_BUFFER_FACTOR.IRON_HARVESTING, 0.5, 2)
    BLACK_STEEL = (SKILL_TYPE.MINING, GROUP_BUFFER_FACTOR.BLACK_STEEL_HARVESTING, 0.83, 1)
    DARK_IRON = (SKILL_TYPE.MINING, GROUP_BUFFER_FACTOR.DARK_IRON_HARVESTING, 0.83, 2)
    BRASS = (SKILL_TYPE.MINING, GROUP_BUFFER_FACTOR.BRASS_HARVESTING, 0.17, 1)
    BRONZE = (SKILL_TYPE.MINING, GROUP_BUFFER_FACTOR.BRONZE_HARVESTING, 0.17, 2)

    LEATHER = (SKILL_TYPE.MINING, GROUP_BUFFER_FACTOR.BRONZE_HARVESTING, -1, -1)

"""
A item that has a quantity
"""
class ItemResource(Item):

    """
    DO NOT DELETE THIS. PASTE THIS IN FOR EVERY NEW OBJECT THAT WILL BE STORED IN A SET/DICTIONARY.
    THIS IS ESSENTIAL FOR MAKING SURE THE PROGRAM PERFORMS EXACTLY THE SAME EVERY TIME!

    assert(false) WILL CRASH THE PROGRAM IF YOU ATTEMPT TO PUT THIS OBJECT INTO A SET/DICT WITHOUT FIRST MODIFYING THE FUNCTION.
    THIS IS DONE ON PURPOSE TO PREVENT YOU FROM ACCIDENTALLY LEAKING NON-DETERMINISM INTO THE PROGRAM.
    SPEAK TO ME (TOM) AND I WILL EXPLAIN WHAT TO DO.
    """
    def __hash__(self):
        assert(False)

    def __init__(self, resource_type, quantity):
        self.quantity = quantity
        self.resource_type = resource_type
        # self.default_consumption_tick_rate =


    """
    Get weight of item
    """
    def weight(self):
         pass

