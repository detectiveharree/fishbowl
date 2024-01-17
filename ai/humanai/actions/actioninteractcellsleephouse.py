from ai.action import Action
import ai.humanai.prerequisites.prerequisiteatlocation
from ai.humanai.needs.needbettersleepinglocation import NeedBetterSleepingLocation
import global_params
import guiwindow
from ai.need import NEED_TYPE
from ai.humanai.prerequisites.prerequisiteatspecificinteractablecell import PrerequisiteAtSpecificInteractableCell
from ai.humanai.prerequisites.prerequisiteatlocation import PrerequisiteAtLocation
from ai.humanai.actions.actioninteractcell import ActionInteractCell
from ai.humanai.actions.actionsleep import ActionSleep
from gameworld.cell.cell import CELL_CATEGORY
from gameworld.cell.cellbuilding.cellbuilding import BUILDING_TYPE

"""
Harvests a resource that player is currently on

A wrapper for performing an action, including a cost function, prerequisite conditions and worker logic.
"""


class ActionInteractCellSleepHouse(ActionInteractCell, ActionSleep):

    """
    DO NOT DELETE THIS. PASTE THIS IN FOR EVERY NEW OBJECT THAT WILL BE STORED IN A SET/DICTIONARY.
    THIS IS ESSENTIAL FOR MAKING SURE THE PROGRAM PERFORMS EXACTLY THE SAME EVERY TIME!

    assert(false) WILL CRASH THE PROGRAM IF YOU ATTEMPT TO PUT THIS OBJECT INTO A SET/DICT WITHOUT FIRST MODIFYING THE FUNCTION.
    THIS IS DONE ON PURPOSE TO PREVENT YOU FROM ACCIDENTALLY LEAKING NON-DETERMINISM INTO THE PROGRAM.
    SPEAK TO ME (TOM) AND I WILL EXPLAIN WHAT TO DO.
    """
    def __hash__(self):
        assert(False)


    def __init__(self, house_location):
        ActionInteractCell.__init__(self, CELL_CATEGORY.BUILDING, BUILDING_TYPE.HOUSE) # ALWAYS CALL PARENT CONSTRUCTOR
        ActionSleep.__init__(self, house_location) # ALWAYS CALL PARENT CONSTRUCTOR
        self.house_location = house_location

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
        return [PrerequisiteAtLocation(self.house_location)]



    """
    Returns true/false if the action should proceed.
    Optional final checks that occur prior to the action starting (i.e. action is currently in a action tree).
    """

    def pre_begin_checks(self, human):
        # human.knowledge_cell_locations.get_cell_if_location_interactable(CELL_CATEGORY.BUILDING, BUILDING_TYPE.HOUSE, human.location)
        if not ActionInteractCell.pre_begin_checks(self, human):
            return False
        if not ActionSleep.pre_begin_checks(self, human):
            return False
        return True

    """
    This is called once when the action begins.
    """

    def begin(self, human):
        ActionInteractCell.begin(self, human)
        ActionSleep.begin(self, human)

    """
    Called every tick while the action has begun and not completed yet.
    Returns True/False to indicate if an error occurs.
    """

    def tick(self, human):
        human.group.average_member_locations.append(human.location)
        return ActionSleep.tick(self, human)


    """
    Returns true/false to indicate whether the action is complete or not.
    Called every tick before tick() is executed.    
    """

    def is_complete(self, human):
        return ActionSleep.is_complete(self, human)


    """
    Called whenever a action is completed 
    """
    def on_finish(self, human):
        ActionInteractCell.on_finish(self, human)

    def __str__(self):
        return "Go to sleep in house"
