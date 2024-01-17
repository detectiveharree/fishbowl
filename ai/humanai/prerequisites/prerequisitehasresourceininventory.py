from ai.prerequisite import Prerequisite
from ai.humanai.actions.actiongetresourcefromstockpile import ActionGetResourceFromStockpile
from gameworld.cell.cellresource.cellresource import RESOURCE_CELL_TYPE
from gameworld.cell.cell import CELL_CATEGORY
from items.itemresources.itemresource import ResourceType
from ai.humanai.actions.actioninteractcellharvestresource import ActionInteractCellHarvestResource

"""
Does the person have a certain resource and amount on him?

A Prerequisite is a predicate that must be true to complete a action.
It is a prediction/estimation based on information that a human has, 
that is used when a human undergoes decision making. Therefore, 
DO NOT leak information that the human does not know i.e. world data.
"""
class PrerequisiteHasResourceInInventory(Prerequisite):

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


    """
    Returns a list of possible actions that may satisfy this prerequisite.
    """
    def possible_actions(self, human):


        target_resource_type = None
        if self.resource == ResourceType.FOOD:
            if human.knowledge_cell_locations.get_interactable_cells(CELL_CATEGORY.RESOURCE, RESOURCE_CELL_TYPE.FARM, human):
                target_resource_type = RESOURCE_CELL_TYPE.FARM
            else:
                target_resource_type = RESOURCE_CELL_TYPE.BERRY_BUSH

        elif self.resource == ResourceType.WATER:
            target_resource_type = RESOURCE_CELL_TYPE.FRESH_WATER
        elif self.resource == ResourceType.WOOD:
            target_resource_type = RESOURCE_CELL_TYPE.TREE
        elif self.resource == ResourceType.WHITE_STEEL:
            target_resource_type = RESOURCE_CELL_TYPE.WHITE_STEEL_ORE
        elif self.resource == ResourceType.BRONZE:
            target_resource_type = RESOURCE_CELL_TYPE.BRONZE_ORE
        elif self.resource == ResourceType.BRASS:
            target_resource_type = RESOURCE_CELL_TYPE.BRASS_ORE
        elif self.resource == ResourceType.DARK_IRON:
            target_resource_type = RESOURCE_CELL_TYPE.DARK_IRON_ORE
        elif self.resource == ResourceType.BLACK_STEEL:
            target_resource_type = RESOURCE_CELL_TYPE.BLACK_STEEL_ORE
        elif self.resource == ResourceType.IRON:
            target_resource_type = RESOURCE_CELL_TYPE.IRON_ORE
        elif self.resource == ResourceType.STONE:
            target_resource_type = RESOURCE_CELL_TYPE.ROCK

        assert(target_resource_type is not None)
        if target_resource_type is None:
            print("How to get this? %s" % self.resource)

        return [ActionInteractCellHarvestResource(target_resource_type, self.amount),
                ActionGetResourceFromStockpile(self.resource, self.amount)]

    """
    Returns true/false if the current prerequisite is satisfied.
    """
    def is_satisfied(self, human):
        return human.inventory.weighted_slot.resources[self.resource].quantity >= self.amount


