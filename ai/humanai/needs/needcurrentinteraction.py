from ai.need import Need, NEED_TYPE
import global_params
from ai.humanai.task.taskinteract import TaskInteract

"""
Artifically sets current need to completing the interaction
"""
class NeedCurrentInteraction(Need):

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
        super().__init__(NEED_TYPE.CURRENT_INTERACTION) # ALWAYS CALL PARENT CONSTRUCTOR
        self.interaction_type = None
        self.need_level = -1
        # self.minimum_need_level_switch = 0

    def currently_interacting(self):
        return self.need_level != -1

    def start_interaction(self, interaction_type, need_level):
        # print("%s started interaction" % human.id_number)
        self.interaction_type = interaction_type
        self.need_level = need_level





    def finish_interaction(self, human):
        # print("%s finished interaction" % human.id_number)
        self.interaction_type = None # just in case set it to None
        self.need_level = -1

    """
    Each person will tick
    """
    def tick(self, human):
        pass


    """
    Called when this need is the highest out of all of needs 
    """
    def get_task(self, human):
        return TaskInteract(human, self.interaction_type)
