from ai.need import Need, NEED_TYPE
import global_params
from ai.humanai.task.taskgotosleep import TaskGoSleep
from ai.humanai.task.tasksignalgroup import TaskSignalGroup
import guiwindow





class NeedSignalGroup(Need):

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
        super().__init__(NEED_TYPE.SIGNAL_GROUP) # ALWAYS CALL PARENT CONSTRUCTOR
        self.need_level = -20000
        self.threat = None

    """
    Each person will tick
    """
    def tick(self, human):
        pass


    def begin_signal(self, campaign):
        self.need_level = global_params.signal_need_level
        self.threat = campaign

    def finish_signal(self, human):
        self.need_level = -20000
        human.group.need_defence.register_campaign_threat(human.group, self.threat)
        self.threat = None

    def minimum_level_for_switch(self):
        return -19999

    """
    Called when this need is the highest out of all of needs 
    """
    def get_task(self, human):
        return TaskSignalGroup(human)



