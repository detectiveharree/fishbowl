from ai import action
from abc import ABC, abstractmethod
from ai.humanai.task.taskassignedtimedtask import TaskAssignedTimedTask
import global_params
from ai.need import NEED_TYPE
from copy import deepcopy
from ai.humanai.skill import SKILL_TYPE


"""
A wrapper for performing an group action, including a cost function, prerequisite conditions and worker logic.
"""
class ActionGroup(action.Action):

    # """
    # DO NOT DELETE THIS. PASTE THIS IN FOR EVERY NEW OBJECT THAT WILL BE STORED IN A SET/DICTIONARY.
    # THIS IS ESSENTIAL FOR MAKING SURE THE PROGRAM PERFORMS EXACTLY THE SAME EVERY TIME!
    #
    # assert(false) WILL CRASH THE PROGRAM IF YOU ATTEMPT TO PUT THIS OBJECT INTO A SET/DICT WITHOUT FIRST MODIFYING THE FUNCTION.
    # THIS IS DONE ON PURPOSE TO PREVENT YOU FROM ACCIDENTALLY LEAKING NON-DETERMINISM INTO THE PROGRAM.
    # SPEAK TO ME (TOM) AND I WILL EXPLAIN WHAT TO DO.
    # """
    # def __hash__(self):
    #     assert(False)


    def __init__(self, parent_task):
        self.parent_task = parent_task
        self.is_activated = False
        self.terminated = False # when action no longer active at all including buffer factor window closed


    """
    Called every tick while the action has begun and not completed yet.
    Returns True/False to indicate if an error occurs.
    """
    def tick(self, group):
        return True




    """
    IF requires_hourly_task_allocation_algo is true,
    will take into account the estimated hours below.
    """
    @abstractmethod
    def estimated_hours(self, group):
        ...


    """
    Returns true/false if we should include this action in the typical task allocation.
    If false, will be removed from the task calculations.
    
    Called when task actions are recalculated.
    """
    @abstractmethod
    def requires_hourly_task_allocation_algo(self):
        ...


    """
    Reserves people from the task allocation algorithm.
    """
    def excluded_people_from_task_allocation_algo(self, group):
        return set()

    """
    Returns true/false if the action should proceed.
    Optional final checks that occur prior to the action starting (i.e. action is currently in a action tree).
    """
    def pre_begin_checks(self, human):
        return True

    """
    This is called once when the action is activated.
    Implement the logic for allocation here.
    NOTE:
    Even if requires_hourly_task_allocation_algo is set to false, you will still
    have access to the task_hours and task_people list.
    """
    def activate(self, hours_left, available_people, group):
        pass

    """
    This is called when the action is deactivated.
    """
    def deactivate(self, group):

        """
        Record and reset buffer factors
        """
        pass

    """
    Optional, gives tickly debug information.
    """
    def get_stats(self, group):
        return ""


    """
    IGNORE DOES NOTHING
    """
    def begin(self, group):
        pass


