from entities.groupbase import GroupBase
from gameworld.timestamp import TimeStamp
import guiwindow
from entities.groupbase import GroupType
import global_params

max_days_between_join_event = 3

class KnowledgeGroup(GroupBase):

    """
    DO NOT DELETE THIS. PASTE THIS IN FOR EVERY NEW OBJECT THAT WILL BE STORED IN A SET/DICTIONARY.
    THIS IS ESSENTIAL FOR MAKING SURE THE PROGRAM PERFORMS EXACTLY THE SAME EVERY TIME!

    assert(false) WILL CRASH THE PROGRAM IF YOU ATTEMPT TO PUT THIS OBJECT INTO A SET/DICT WITHOUT FIRST MODIFYING THE FUNCTION.
    THIS IS DONE ON PURPOSE TO PREVENT YOU FROM ACCIDENTALLY LEAKING NON-DETERMINISM INTO THE PROGRAM.
    SPEAK TO ME (TOM) AND I WILL EXPLAIN WHAT TO DO.
    """
    def __hash__(self):
        assert(False)


    def __init__(self, group_id):
        super().__init__(group_id, GroupType.RALLY_POINT) # ALWAYS CALL PARENT CONSTRUCTOR

        if group_id in guiwindow.WORLD_INSTANCE.groups.keys():
            self.group_type = guiwindow.WORLD_INSTANCE.groups[group_id].group_type

        self.believed_amount_food = 0
        self.believed_amount_water = 0
        self.believed_fight_score = 0
        self.believed_food_buffer_factor = global_params.DEFAULT_SURVIVAL_BUFFER_FACTOR
        self.believed_water_buffer_factor = global_params.DEFAULT_SURVIVAL_BUFFER_FACTOR

        self.last_attempted_join = TimeStamp()


    """
    Called when person attempts to join
    """
    def attempt_join(self):
        self.last_attempted_join = TimeStamp()

    """
    Flag to indicate if person can join again
    """
    def can_join(self):
        return (guiwindow.WORLD_INSTANCE.time_day - self.last_attempted_join.day) > max_days_between_join_event
