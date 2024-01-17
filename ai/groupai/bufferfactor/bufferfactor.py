from abc import ABC, abstractmethod
import global_params
from items.itemresources.itemresource import GROUP_BUFFER_FACTOR


"""
A wrapper for performing an action, including a cost function, prerequisite conditions and worker logic.

ABC is a abstract base class.
Means we can never instantiate a BufferFactor object.
Instead we have to extend it, and complete the functions to do it. 
"""
class BufferFactor(ABC):

    """
    DO NOT DELETE THIS. PASTE THIS IN FOR EVERY NEW OBJECT THAT WILL BE STORED IN A SET/DICTIONARY.
    THIS IS ESSENTIAL FOR MAKING SURE THE PROGRAM PERFORMS EXACTLY THE SAME EVERY TIME!

    assert(false) WILL CRASH THE PROGRAM IF YOU ATTEMPT TO PUT THIS OBJECT INTO A SET/DICT WITHOUT FIRST MODIFYING THE FUNCTION.
    THIS IS DONE ON PURPOSE TO PREVENT YOU FROM ACCIDENTALLY LEAKING NON-DETERMINISM INTO THE PROGRAM.
    SPEAK TO ME (TOM) AND I WILL EXPLAIN WHAT TO DO.
    """
    def __hash__(self):
        assert(False)

    def __init__(self, skill):
        self.default_value = global_params.DEFAULT_BUFFER_FACTOR
        if skill == GROUP_BUFFER_FACTOR.FOOD_HARVESTING or skill == GROUP_BUFFER_FACTOR.WATER_HARVESTING:
            self.default_value = global_params.DEFAULT_SURVIVAL_BUFFER_FACTOR

        self.value = self.default_value
        self.skill = skill

    """
    Update the buffer factor
    """
    @abstractmethod
    def daily_update(self, amount_needed, amount_collected, total_hours_float_allocation):
        ...

    def __repr__(self):
        return str(self)



