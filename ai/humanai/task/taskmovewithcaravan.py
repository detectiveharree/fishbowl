import ai
from ai.humanai.actions.actionmovewithcaravan import ActionMoveWithCaravan

"""
Task for moving with a caravan
"""
class TaskMoveWithCaravan(ai.task.Task):

    """
    DO NOT DELETE THIS. PASTE THIS IN FOR EVERY NEW OBJECT THAT WILL BE STORED IN A SET/DICTIONARY.
    THIS IS ESSENTIAL FOR MAKING SURE THE PROGRAM PERFORMS EXACTLY THE SAME EVERY TIME!

    assert(false) WILL CRASH THE PROGRAM IF YOU ATTEMPT TO PUT THIS OBJECT INTO A SET/DICT WITHOUT FIRST MODIFYING THE FUNCTION.
    THIS IS DONE ON PURPOSE TO PREVENT YOU FROM ACCIDENTALLY LEAKING NON-DETERMINISM INTO THE PROGRAM.
    SPEAK TO ME (TOM) AND I WILL EXPLAIN WHAT TO DO.
    """
    def __hash__(self):
        assert(False)


    def __init__(self, human, group_action):
        self.group_action = group_action
        self.human = human


    """
    Possible actions that the user can do to satisfy this pre requisite.
    Note the action with the cheapest action tree will be picked.
    """
    def possible_actions(self):
        return [ActionMoveWithCaravan(self.human, self.group_action)]


    def __repr__(self):
        return str("Move with caravan")
