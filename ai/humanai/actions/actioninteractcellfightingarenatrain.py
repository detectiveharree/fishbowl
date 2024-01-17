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
from ai.humanai.skill import SKILL_TYPE
from entities.groupbase import GroupBase, GROUP_BUFFER_FACTOR
from ai.humanai.actions.actioninteractcellbuildinginteract import ActionInteractCellBuildingInteract
from ai.humanai.relationships.interaction.interactionfighting.interactionfight import InteractionFight


"""
Harvests a resource that player is currently on

A wrapper for performing an action, including a cost function, prerequisite conditions and worker logic.
"""


class ActionInteractCellFightingArenaTrain(ActionInteractCellBuildingInteract):

    """
    DO NOT DELETE THIS. PASTE THIS IN FOR EVERY NEW OBJECT THAT WILL BE STORED IN A SET/DICTIONARY.
    THIS IS ESSENTIAL FOR MAKING SURE THE PROGRAM PERFORMS EXACTLY THE SAME EVERY TIME!

    assert(false) WILL CRASH THE PROGRAM IF YOU ATTEMPT TO PUT THIS OBJECT INTO A SET/DICT WITHOUT FIRST MODIFYING THE FUNCTION.
    THIS IS DONE ON PURPOSE TO PREVENT YOU FROM ACCIDENTALLY LEAKING NON-DETERMINISM INTO THE PROGRAM.
    SPEAK TO ME (TOM) AND I WILL EXPLAIN WHAT TO DO.
    """
    def __hash__(self):
        assert(False)


    def __init__(self, interaction):
        super().__init__(BUILDING_TYPE.FIGHTINGARENA, interaction) # ALWAYS CALL PARENT CONSTRUCTOR


    def __str__(self):
        return "Interact (%s) with %s in building %s" % (self.interact_type.get_interaction_type(), self.current_interaction_target, self.building_type)
