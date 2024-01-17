from ai.need import Need, NEED_TYPE
import global_params
from ai.humanai.task.taskconsumeresource import TaskConsumeResource
from items.itemresources.itemresource import ResourceType

"""
This is a corner case need just because we can never
have human.current_highest_need = None 

This need will only ever be set as the highest, 
IF all other human needs are below their minimum need level
"""

class NeedNone(Need):

    """
    DO NOT DELETE THIS. PASTE THIS IN FOR EVERY NEW OBJECT THAT WILL BE STORED IN A SET/DICTIONARY.
    THIS IS ESSENTIAL FOR MAKING SURE THE PROGRAM PERFORMS EXACTLY THE SAME EVERY TIME!

    assert(false) WILL CRASH THE PROGRAM IF YOU ATTEMPT TO PUT THIS OBJECT INTO A SET/DICT WITHOUT FIRST MODIFYING THE FUNCTION.
    THIS IS DONE ON PURPOSE TO PREVENT YOU FROM ACCIDENTALLY LEAKING NON-DETERMINISM INTO THE PROGRAM.
    SPEAK TO ME (TOM) AND I WILL EXPLAIN WHAT TO DO.
    """
    def __hash__(self):
        assert(False)


    def __init__(self):
        super().__init__(NEED_TYPE.NONE) # ALWAYS CALL PARENT CONSTRUCTOR
        self.need_level = -10000

    """
    Each person will tick 
    """
    def tick(self, human):
        pass


    def minimum_level_for_switch(self):
        return -10001

    """
    Called when this need is the highest out of all of needs 
    """
    def get_task(self, human):
        return None
