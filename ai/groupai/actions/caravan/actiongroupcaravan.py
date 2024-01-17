from ai.groupai.actions.actiongroup import ActionGroup
from ai.humanai.task.taskjoingroup import TaskJoinGroup
from ai.humanai.task.taskmovewithcaravan import TaskMoveWithCaravan
from ai.humanai.task.taskassignedtask import TaskAssignedTask
import math
from ai.humanai.task.taskbattle import TaskBattle
from ai.need import NEED_TYPE
from ai import pathfinding

"""
Action group caravan is one of which applies to entire group
and is excluded from task allocation algorithm
"""
class ActionGroupCaravan(ActionGroup):

    def __init__(self, parent_task):
        super().__init__(parent_task) # ALWAYS CALL PARENT CONSTRUCTOR


    """
    Returns true/false if we should include this action in the typical task allocation.
    If false, will be removed from the task calculations.

    Called when task actions are recalculated.
    """
    def requires_hourly_task_allocation_algo(self):
        return False

    """
    IF requires_hourly_task_allocation_algo is true,
    will take into account the estimated hours below.
    """
    def estimated_hours(self, group):
        return 0

    """
    Reserves people from the task allocation algorithm.
    """
    def excluded_people_from_task_allocation_algo(self, group):
        return group.members


    """
    The estimated cost of this action.
    This occurs during the decision making process of a action tree.
    For extra accuracy, use data from prerequisites.
    """

    def get_costs(self, group):
        return 0

    """
    Returns true/false to indicate whether the action is complete or not.
    Called every tick before tick() is executed.    
    """

    def is_complete(self, group):
        return not self.interaction_group_battle.battle_tick(self.interaction_group_participant)


    """
    Optional, gives tickly debug information.
    """
    def get_stats(self, group):
        return "Action Caravan"

    def __str__(self):
        return "Action Caravan"
