from ai.prerequisite import Prerequisite

from ai.humanai.actions.actiongotointeractablecell import ActionGoToInteractableCell
from ai.humanai.prerequisites.prerequisiteatinteractablecell import PrerequisiteAtInteractableCell
from ai.humanai.actions.actiongotolocation import ActionGoToLocation
import guiwindow

"""

"""
class PrerequisiteAtSpecificInteractableCell(PrerequisiteAtInteractableCell):

    """
    DO NOT DELETE THIS. PASTE THIS IN FOR EVERY NEW OBJECT THAT WILL BE STORED IN A SET/DICTIONARY.
    THIS IS ESSENTIAL FOR MAKING SURE THE PROGRAM PERFORMS EXACTLY THE SAME EVERY TIME!

    assert(false) WILL CRASH THE PROGRAM IF YOU ATTEMPT TO PUT THIS OBJECT INTO A SET/DICT WITHOUT FIRST MODIFYING THE FUNCTION.
    THIS IS DONE ON PURPOSE TO PREVENT YOU FROM ACCIDENTALLY LEAKING NON-DETERMINISM INTO THE PROGRAM.
    SPEAK TO ME (TOM) AND I WILL EXPLAIN WHAT TO DO.
    """
    def __hash__(self):
        assert(False)


    def __init__(self, cellbase):
        super().__init__(cellbase.cell_category, cellbase.cell_type) # ALWAYS CALL PARENT CONSTRUCTOR


    """
    Returns a list of possible actions that may satisfy this prerequisite.
    """
    def possible_actions(self, human):
        return [ActionGoToLocation(cellbase.locations[0])]



