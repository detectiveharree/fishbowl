from ai import task
from ai.humanai.actions.actiondepositresourceatstockpile import ActionDepositResourceAtStockpile
import ai.humanai.actions.actiongetresourcefromstockpile

"""
Task for bringing new cell to a group
"""
class TaskBringResourceToGroup(task.Task):

    """
    DO NOT DELETE THIS. PASTE THIS IN FOR EVERY NEW OBJECT THAT WILL BE STORED IN A SET/DICTIONARY.
    THIS IS ESSENTIAL FOR MAKING SURE THE PROGRAM PERFORMS EXACTLY THE SAME EVERY TIME!

    assert(false) WILL CRASH THE PROGRAM IF YOU ATTEMPT TO PUT THIS OBJECT INTO A SET/DICT WITHOUT FIRST MODIFYING THE FUNCTION.
    THIS IS DONE ON PURPOSE TO PREVENT YOU FROM ACCIDENTALLY LEAKING NON-DETERMINISM INTO THE PROGRAM.
    SPEAK TO ME (TOM) AND I WILL EXPLAIN WHAT TO DO.
    """
    def __hash__(self):
        assert(False)


    def __init__(self, resource, amount, group_action):
        self.resource = resource
        self.amount = amount
        self.group_action = group_action

    """
    Possible actions that the user can do to satisfy this pre requisite.
    Note the action with the cheapest action tree will be picked.
    """
    def possible_actions(self):
        return [ActionDepositResourceAtStockpile(self.resource, self.amount, self.group_action)]

    """
    Actions that CANNOT be performed while completing this task.
    NOTE the actions are specified via its type.
    """
    def forbidden_actions(self):
        return [ai.humanai.actions.actiongetresourcefromstockpile.ActionGetResourceFromStockpile]


    def __repr__(self):
        return str("Bring %s %s" % (self.amount, self.resource))
