from ai.action import Action
from ai.humanai.prerequisites.prerequisitehasresourceininventory import PrerequisiteHasResourceInInventory

"""
Consumes a amount of resource in the player inventory.

A wrapper for performing an action, including a cost function, prerequisite conditions and worker logic.
"""
class ActionConsumeResource(Action):

    """
    DO NOT DELETE THIS. PASTE THIS IN FOR EVERY NEW OBJECT THAT WILL BE STORED IN A SET/DICTIONARY.
    THIS IS ESSENTIAL FOR MAKING SURE THE PROGRAM PERFORMS EXACTLY THE SAME EVERY TIME!

    assert(false) WILL CRASH THE PROGRAM IF YOU ATTEMPT TO PUT THIS OBJECT INTO A SET/DICT WITHOUT FIRST MODIFYING THE FUNCTION.
    THIS IS DONE ON PURPOSE TO PREVENT YOU FROM ACCIDENTALLY LEAKING NON-DETERMINISM INTO THE PROGRAM.
    SPEAK TO ME (TOM) AND I WILL EXPLAIN WHAT TO DO.
    """
    def __hash__(self):
        assert(False)


    def __init__(self, need_type, resource, amount):
        self.need_type = need_type
        self.resource = resource
        self.amount = amount


    """
    Returns a list of prerequisites that must be satisfied in order to complete the action.
    
    Note the order of these prerequisites reflects the order of their potential actions that need
    to be completed for this action to be possible to do. Therefore order it appropriately.
    Note the action may not necessarily be executed if all the prerequisites are true. 
    The prerequisites are used in the decision making process, however the optional
    method pre_begin_checks returns the final check before the action is executed in case new information
    is is revealed.
    """
    def get_prerequisites(self):
        return [PrerequisiteHasResourceInInventory(self.resource, self.amount)]

    """
    The estimated cost of this action.
    This occurs during the decision making process of a action tree.
    For extra accuracy, use data from prerequisites.
    """
    def get_costs(self, human):
        return 0


    """
    This is called once when the action begins.
    """
    def begin(self, human):
        human.inventory.weighted_slot.resources[self.resource].quantity -= self.amount
        human.needs[self.need_type].need_level -= self.amount

    """
    Called every tick while the action has begun and not completed yet.
    Returns True/False to indicate if an error occurs.
    """
    def tick(self, human):
        return True

    """
    Returns true/false to indicate whether the action is complete or not.
    Called every tick before tick() is executed.    
    """
    def is_complete(self, human):
        return True



    def __str__(self):
        return "Consume %s %s" % (self.amount, self.resource)