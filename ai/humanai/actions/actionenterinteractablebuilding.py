from ai.action import Action
import ai.humanai.prerequisites.prerequisiteatfreeresource
from ai.humanai.prerequisites.prerequisiteatinteractablecell import PrerequisiteAtInteractableCell
from gameworld.cell.cell import CELL_CATEGORY
import global_params
import guiwindow

"""
Harvests a resource that player is currently on

A wrapper for performing an action, including a cost function, prerequisite conditions and worker logic.
"""


class ActionInteractCellHarvestResource(Action):

    """
    DO NOT DELETE THIS. PASTE THIS IN FOR EVERY NEW OBJECT THAT WILL BE STORED IN A SET/DICTIONARY.
    THIS IS ESSENTIAL FOR MAKING SURE THE PROGRAM PERFORMS EXACTLY THE SAME EVERY TIME!

    assert(false) WILL CRASH THE PROGRAM IF YOU ATTEMPT TO PUT THIS OBJECT INTO A SET/DICT WITHOUT FIRST MODIFYING THE FUNCTION.
    THIS IS DONE ON PURPOSE TO PREVENT YOU FROM ACCIDENTALLY LEAKING NON-DETERMINISM INTO THE PROGRAM.
    SPEAK TO ME (TOM) AND I WILL EXPLAIN WHAT TO DO.
    """
    def __hash__(self):
        assert(False)


    def __init__(self, resource, amount):
        self.resource = resource
        self.amount = amount
        self.amount_collected = 0

        self.found_cell = None  # actual cell object node assigned in pre begin

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
        return [PrerequisiteAtInteractableCell(CELL_CATEGORY.RESOURCE, self.resource)]

    """
    The estimated cost of this action.
    This occurs during the decision making process of a action tree.
    For extra accuracy, use data from prerequisites.
    """

    def get_costs(self, human):
        """
        Amount to harvest is the cost of harvesting.
        """
        return self.amount

    """
    Returns true/false if the action should proceed.
    Optional final checks that occur prior to the action starting (i.e. action is currently in a action tree).
    """

    def pre_begin_checks(self, human):
        if not PrerequisiteAtInteractableCell(CELL_CATEGORY.RESOURCE, self.resource).is_satisfied(human):
            return False
        self.found_cell = guiwindow.WORLD_INSTANCE.world[human.location[0]][human.location[1]].cell_type

        return

    """
    This is called once when the action begins.
    """
    def begin(self, human):
        self.found_cell.begin_interact(human.location, human)

    """
    Called every tick while the action has begun and not completed yet.
    Returns True/False to indicate if an error occurs.
    """

    def tick(self, human):
        amount_per_tick = human.skills[
                              self.resource.skill_association] * self.resource.skill_association.default_harvest_rate_tick
        actual_amount_harvested = self.found_cell.harvest(amount_per_tick)
        self.amount_collected += actual_amount_harvested
        human.inventory.weighted_slot.resources[self.resource].quantity += actual_amount_harvested
        return True

    """
    Returns true/false to indicate whether the action is complete or not.
    Called every tick before tick() is executed.    
    """

    def is_complete(self, human):
        return (human.inventory.weighted_slot.resources[self.resource].quantity >= self.amount) or (
                    self.amount_collected >= self.amount)

    """
    Called whenever a action is completed 
    """

    def on_finish(self, human):
        self.found_cell.end_interact(human.location, human)

    def __str__(self):
        return "Harvest %s %s" % (self.amount, self.resource)
