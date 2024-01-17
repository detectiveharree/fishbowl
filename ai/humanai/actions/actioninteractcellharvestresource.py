from ai.action import Action
from ai.humanai.prerequisites.prerequisiteatinteractablecell import PrerequisiteAtInteractableCell
from ai.humanai.actions.actioninteractcell import ActionInteractCell
from gameworld.cell.cell import CELL_CATEGORY
import global_params
import guiwindow

"""
Harvests a resource that player is currently on

A wrapper for performing an action, including a cost function, prerequisite conditions and worker logic.
"""


class ActionInteractCellHarvestResource(ActionInteractCell):

    """
    DO NOT DELETE THIS. PASTE THIS IN FOR EVERY NEW OBJECT THAT WILL BE STORED IN A SET/DICTIONARY.
    THIS IS ESSENTIAL FOR MAKING SURE THE PROGRAM PERFORMS EXACTLY THE SAME EVERY TIME!

    assert(false) WILL CRASH THE PROGRAM IF YOU ATTEMPT TO PUT THIS OBJECT INTO A SET/DICT WITHOUT FIRST MODIFYING THE FUNCTION.
    THIS IS DONE ON PURPOSE TO PREVENT YOU FROM ACCIDENTALLY LEAKING NON-DETERMINISM INTO THE PROGRAM.
    SPEAK TO ME (TOM) AND I WILL EXPLAIN WHAT TO DO.
    """
    def __hash__(self):
        assert(False)


    def __init__(self, resource_cell_type, amount):
        super().__init__(CELL_CATEGORY.RESOURCE, resource_cell_type) # ALWAYS CALL PARENT CONSTRUCTOR
        self.resource_cell_type = resource_cell_type
        self.amount = amount
        self.amount_collected = 0



    def tick(self, human):
        human.group.average_member_locations.append(human.location)

        amount_per_tick = human.skills[
                              self.resource_cell_type.harvestable_type.skill_association] * self.resource_cell_type.harvestable_type.group_buffer_factor_association.default_harvest_rate_tick
        actual_amount_harvested = self.found_cell.harvest(amount_per_tick)
        if actual_amount_harvested != amount_per_tick:
            return False
        self.amount_collected += actual_amount_harvested
        human.inventory.weighted_slot.resources[self.resource_cell_type.harvestable_type].quantity += actual_amount_harvested
        return True

    """
    Returns true/false to indicate whether the action is complete or not.
    Called every tick before tick() is executed.    
    """

    def is_complete(self, human):
        return (human.inventory.weighted_slot.resources[self.resource_cell_type.harvestable_type].quantity >= self.amount) or (
                    self.amount_collected >= self.amount)


    def __str__(self):
        return "Harvest %s %s (%s)" % (self.amount, self.resource_cell_type.harvestable_type, self.resource_cell_type)
