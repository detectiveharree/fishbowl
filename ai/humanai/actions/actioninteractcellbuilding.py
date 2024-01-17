from ai.action import Action
from ai.humanai.prerequisites.prerequisiteatinteractablecell import PrerequisiteAtInteractableCell
from ai.humanai.actions.actioninteractcell import ActionInteractCell
from gameworld.cell.cell import CELL_CATEGORY
import global_params
import guiwindow
from ai.humanai.actions.actioninteractpersoninitiate import ActionInteractPersonInitiate

"""
Harvests a resource that player is currently on

A wrapper for performing an action, including a cost function, prerequisite conditions and worker logic.
"""


class ActionInteractCellBuilding(ActionInteractCell):

    """
    DO NOT DELETE THIS. PASTE THIS IN FOR EVERY NEW OBJECT THAT WILL BE STORED IN A SET/DICTIONARY.
    THIS IS ESSENTIAL FOR MAKING SURE THE PROGRAM PERFORMS EXACTLY THE SAME EVERY TIME!

    assert(false) WILL CRASH THE PROGRAM IF YOU ATTEMPT TO PUT THIS OBJECT INTO A SET/DICT WITHOUT FIRST MODIFYING THE FUNCTION.
    THIS IS DONE ON PURPOSE TO PREVENT YOU FROM ACCIDENTALLY LEAKING NON-DETERMINISM INTO THE PROGRAM.
    SPEAK TO ME (TOM) AND I WILL EXPLAIN WHAT TO DO.
    """
    def __hash__(self):
        assert(False)


    def __init__(self, building_type):
        super().__init__(CELL_CATEGORY.BUILDING, building_type) # ALWAYS CALL PARENT CONSTRUCTOR
        self.building_type = building_type


    def tick(self, human):
        return True


    def __str__(self):
        return "Enter building %s" % (self.building_type)
