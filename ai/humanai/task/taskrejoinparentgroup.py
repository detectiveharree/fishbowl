from ai import task
import ai.humanai.actions.actionsleep
from ai.humanai.actions.actiongotolocation import ActionGoToLocation
from ai.humanai.actions.actionrejoinparentgroup import ActionRejoinParentGroup

"""
Task for joining a caravan
"""
class TaskRejoinParentGroup(task.Task):


    """
    DO NOT DELETE THIS. PASTE THIS IN FOR EVERY NEW OBJECT THAT WILL BE STORED IN A SET/DICTIONARY.
    THIS IS ESSENTIAL FOR MAKING SURE THE PROGRAM PERFORMS EXACTLY THE SAME EVERY TIME!

    assert(false) WILL CRASH THE PROGRAM IF YOU ATTEMPT TO PUT THIS OBJECT INTO A SET/DICT WITHOUT FIRST MODIFYING THE FUNCTION.
    THIS IS DONE ON PURPOSE TO PREVENT YOU FROM ACCIDENTALLY LEAKING NON-DETERMINISM INTO THE PROGRAM.
    SPEAK TO ME (TOM) AND I WILL EXPLAIN WHAT TO DO.
    """
    def __hash__(self):
        assert(False)


    def __init__(self, caravan_group):
        self.caravan_group = caravan_group



    """
    Possible actions that the user can do to satisfy this pre requisite.
    Note the action with the cheapest action tree will be picked.
    """
    def possible_actions(self):
        return [ActionRejoinParentGroup(self.caravan_group)]


    def __repr__(self):
        return str("Join group %s" % self.caravan_group.id_number)
