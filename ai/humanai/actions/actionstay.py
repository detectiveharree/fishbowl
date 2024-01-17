from ai.humanai.actions.actioninteractcell import ActionInteractCell
from gameworld.cell.cell import CELL_CATEGORY
from ai.humanai.actions.actioninteractpersoninitiate import ActionInteractPersonInitiate
from ai.need import NEED_TYPE
import guiwindow
from ai.humanai.prerequisites.prerequisiteknowspersonlocation import PrerequisiteKnowsPersonLocation
from ai.humanai.actions.actiongotoperson import ActionGoToPerson
from ai.humanai.relationships.interaction.interactionfighting.interactionfightbattle import InteractionFightBattle
from ai.action import Action

"""
Harvests a resource that player is currently on

A wrapper for performing an action, including a cost function, prerequisite conditions and worker logic.
"""


class ActionStay(Action):

    """
    DO NOT DELETE THIS. PASTE THIS IN FOR EVERY NEW OBJECT THAT WILL BE STORED IN A SET/DICTIONARY.
    THIS IS ESSENTIAL FOR MAKING SURE THE PROGRAM PERFORMS EXACTLY THE SAME EVERY TIME!

    assert(false) WILL CRASH THE PROGRAM IF YOU ATTEMPT TO PUT THIS OBJECT INTO A SET/DICT WITHOUT FIRST MODIFYING THE FUNCTION.
    THIS IS DONE ON PURPOSE TO PREVENT YOU FROM ACCIDENTALLY LEAKING NON-DETERMINISM INTO THE PROGRAM.
    SPEAK TO ME (TOM) AND I WILL EXPLAIN WHAT TO DO.
    """
    def __hash__(self):
        assert(False)


    """
    This is called once when the action begins.
    """
    def begin(self, human):
        pass

    """
    The estimated cost of this action.
    This occurs during the decision making process of a action tree.
    For extra accuracy, use data from prerequisites.
    """
    def get_costs(self, human):
        return 0


    def tick(self, human):
        return True

    """
    Returns true/false to indicate whether the action is complete or not.
    Called every tick before tick() is executed.    
    """
    def is_complete(self, human):
        return False

    def __str__(self):
        return "Stay put"
