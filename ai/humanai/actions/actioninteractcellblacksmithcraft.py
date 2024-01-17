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


"""
Harvests a resource that player is currently on

A wrapper for performing an action, including a cost function, prerequisite conditions and worker logic.
"""


class ActionInteractCellBlacksmithCraft(ActionInteractCell):

    """
    DO NOT DELETE THIS. PASTE THIS IN FOR EVERY NEW OBJECT THAT WILL BE STORED IN A SET/DICTIONARY.
    THIS IS ESSENTIAL FOR MAKING SURE THE PROGRAM PERFORMS EXACTLY THE SAME EVERY TIME!

    assert(false) WILL CRASH THE PROGRAM IF YOU ATTEMPT TO PUT THIS OBJECT INTO A SET/DICT WITHOUT FIRST MODIFYING THE FUNCTION.
    THIS IS DONE ON PURPOSE TO PREVENT YOU FROM ACCIDENTALLY LEAKING NON-DETERMINISM INTO THE PROGRAM.
    SPEAK TO ME (TOM) AND I WILL EXPLAIN WHAT TO DO.
    """
    def __hash__(self):
        assert(False)


    def __init__(self, amount_ticks, group_action):

        super().__init__(CELL_CATEGORY.BUILDING, BUILDING_TYPE.BLACKSMITH) # ALWAYS CALL PARENT CONSTRUCTOR
        self.group_action = group_action
        self.amount_ticks = amount_ticks
        self.tick_count = 0


    """
    Called every tick while the action has begun and not completed yet.
    Returns True/False to indicate if an error occurs.
    """
    def tick(self, human):
        human.group.average_member_locations.append(human.location)
        self.tick_count += 1
        amount_per_tick = human.skills[SKILL_TYPE.CRAFTING] * GROUP_BUFFER_FACTOR.CRAFTING.default_harvest_rate_tick
        self.group_action.register_progress(human, amount_per_tick, human.group)
        return True


    """
    Returns true/false to indicate whether the action is complete or not.
    Called every tick before tick() is executed.    
    """
    def is_complete(self, human):
        return (not human.group.need_crafting.is_items_left()) or self.tick_count >= self.amount_ticks


    def __str__(self):
        return "Craft item %s in %s"
