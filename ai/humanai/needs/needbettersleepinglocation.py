from ai.need import Need, NEED_TYPE
from ai.humanai.task.taskinitiateinteraction import TaskInitiateInteraction
from ai import pathfinding
from random import randint


"""
Check belongs to them.
is_free_us()
"""

class NeedBetterSleepingLocation(Need):

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
        super().__init__(NEED_TYPE.BETTER_SLEEPING_LOCATION) # ALWAYS CALL PARENT CONSTRUCTOR
        self.need_level = 0

    def update_need_level(self, human):
        if len(human.group.members) > 1:
            self.need_level = human.sleeping_location.get_preference_score(human)
            return
        self.need_level = 0



    def set_new_sleeping_location(self, human, location):

        """
        Leave location if not already.
        """
        if human.sleeping_location is not None:
            human.sleeping_location.leave_location(human)

        human.sleeping_location = location

        if location is not None:
            self.update_need_level(human)
            human.sleeping_location.take_location(human)



    """
    Finds new sleeping location
    """
    def find_sleeping_location(self, human):
        """
        Gets all possible sleeping location types, tents, houses etc.
        Finds best from each one of them
        """
        best_sleeping_locations = {}
        for sleeping_location_type in human.group.possible_sleeping_location_types:
            score_and_loc = sleeping_location_type.find_best_sleeping_location(human)
            if score_and_loc is not None:
                best_sleeping_locations[sleeping_location_type] = score_and_loc

        """
        Finds the best one of these sleeping locations
        """
        best = sorted(best_sleeping_locations.items(), key=lambda x: x[1][0])[0]

        best_loc = best[1][1]
        best_type = best[0]

        sleeping_location = best_type.create_sleeping_location(human.group, best_loc)
        self.set_new_sleeping_location(human, sleeping_location)



    """
    Each person will tick 
    """
    def tick(self, human):
        if human.sleeping_location is None:
            self.need_level = human.needs[NEED_TYPE.SLEEP].need_level + 10


    def minimum_level_for_switch(self):
        return 0

    """
    Called when this need is the highest out of all of needs 
    """
    def get_task(self, human):
        if randint(0, 50) == 0:
            # print("Randomly resetting sleeping location for %s" % human.id_number)
            self.set_new_sleeping_location(human, None)

        if human.sleeping_location is None:
            self.find_sleeping_location(human)


    def __str__(self):
        return "Need Better Sleeping Location : %s" % self.need_level

