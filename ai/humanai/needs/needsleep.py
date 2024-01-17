from ai.need import Need, NEED_TYPE
import global_params
from ai.humanai.task.taskgotosleep import TaskGoSleep
import guiwindow





class NeedSleep(Need):

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
        super().__init__(NEED_TYPE.SLEEP) # ALWAYS CALL PARENT CONSTRUCTOR

    """
    Each person will tick
    """
    def tick(self, human):
        self.need_level += global_params.tired_tick


    def minimum_level_for_switch(self):
        return global_params.go_to_sleep_threshold

    """
    Called when this need is the highest out of all of needs 
    """
    def get_task(self, human):
        return TaskGoSleep(human)
        # if self.need_level >= global_params.go_to_sleep_threshold * 3:
        #     # pass out
        #     print("%s passed out" % human.id_number)
        #     human.sleep_hour = guiwindow.WORLD_INSTANCE.time_hour


