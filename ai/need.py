from abc import ABC, abstractmethod
from enum import Enum


class NEED_TYPE(Enum):
    HUNGER = 1
    THIRST = 2
    SLEEP = 3
    SOCIALISING = 4
    GROUP_TASK = 5
    CURRENT_INTERACTION = 6
    BETTER_SLEEPING_LOCATION = 7
    NONE = 8
    BOREDOM = 9
    FRUSTRATION = 10
    ANGER = 11
    SIGNAL_GROUP = 12
    TRAIN = 13

    def __repr__(self):
        return self.name



class Need(ABC):


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
    I.e. if level is below this then don't set this as current max task
    Default 0
    """
    def minimum_level_for_switch(self):
        return 0

    """
    Each person will tick 
    """

    @abstractmethod
    def tick(self, human):
        ...

    """
    Called when this need is the highest out of all of needs 
    """
    @abstractmethod
    def get_task(self, human):
        ...

    def __repr__(self):
        return str(self.need_type) + " " + str(round(self.need_level,2))



