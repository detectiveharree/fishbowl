from ai.need import Need
from enum import Enum

class GROUP_NEED_TYPE(Enum):
    HUNGER = 1
    THIRST = 2
    WOOD = 3
    SURVIVAL = 4
    SHELTER = 5
    DEFENCE = 6
    CRAFTING = 7
    RESOURCE_REQUESTING = 8
    NONE = 9 # placeholder
    SWITCHING_GROUP = 10 # placeholder

    def __repr__(self):
        return self.name

class NeedGroup(Need):

    """
    DO NOT DELETE THIS. PASTE THIS IN FOR EVERY NEW OBJECT THAT WILL BE STORED IN A SET/DICTIONARY.
    THIS IS ESSENTIAL FOR MAKING SURE THE PROGRAM PERFORMS EXACTLY THE SAME EVERY TIME!

    assert(false) WILL CRASH THE PROGRAM IF YOU ATTEMPT TO PUT THIS OBJECT INTO A SET/DICT WITHOUT FIRST MODIFYING THE FUNCTION.
    THIS IS DONE ON PURPOSE TO PREVENT YOU FROM ACCIDENTALLY LEAKING NON-DETERMINISM INTO THE PROGRAM.
    SPEAK TO ME (TOM) AND I WILL EXPLAIN WHAT TO DO.
    """
    def __hash__(self):
        assert(False)

    need_level = 0

    def __init__(self, need_type):
        self.need_type = need_type


    """
    Needs can be derived here 
    """
    def tick(self, group):
        pass

    """
    Called once a day.
    """
    def get_task(self, group, adjusted_need_level):

        return []
        # return TaskGroupGetResource(ResourceType.WATER, global_params.thirst_tick * global_params.daily_ticks * len(group.members), self.need_level)


