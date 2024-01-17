from ai.need import Need, NEED_TYPE
from ai.humanai.task.taskconsumeresource import TaskConsumeResource
import global_params
from items.itemresources.itemresource import ResourceType
from humanbase import HEALTH_CHANGE_TYPE


class NeedWater(Need):

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
        super().__init__(NEED_TYPE.THIRST) # ALWAYS CALL PARENT CONSTRUCTOR

    """
    Each person will tick 
    """
    def tick(self, human):
        self.need_level += global_params.thirst_tick

        # if self.need_level >= global_params.dehydration_death_threshold:
        #     human.die(HEALTH_CHANGE_TYPE.THIRST)

    def minimum_level_for_switch(self):
        return 30

    """
    Called when this need is the highest out of all of needs 
    """
    def get_task(self, human):
        return TaskConsumeResource(NEED_TYPE.THIRST, ResourceType.WATER, self.need_level)

    # def __str__(self):
    #     return "Water : %s" % self.need_level