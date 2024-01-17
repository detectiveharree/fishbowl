from ai.groupai.actions.actiongroup import ActionGroup
from ai.humanai.task.taskrejoinparentgroup import TaskRejoinParentGroup
import math
from ai.need import NEED_TYPE

"""
Combines group with its parent group (no need for permission - all accepted)
"""
class ActionGroupCaravanRejoinParentGroup(ActionGroup):


    def __init__(self, parent_task, caravan_group):
        super().__init__(parent_task) # ALWAYS CALL PARENT CONSTRUCTOR
        self.caravan_group = caravan_group
        self.original_size = len(self.caravan_group.members)


    def set_participants(self, group):
        return group.members

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
    Should give the workers there tasks.
    """
    def activate(self, hours_left, available_people, group):
        for worker in list(group.members):
            worker.needs[NEED_TYPE.GROUP_TASK].set_daily_task(worker, TaskRejoinParentGroup(group.parent_group), 10000)

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
        return len(group.members) == 0

    """
    Optional, gives tickly debug information.
    """

    def get_stats(self, group):
        return "members (%s/%s)" % (len(self.caravan_group.members), self.original_size)

    def __str__(self):
        return "Caravan rejoinparent parent (%s -> %s)" % (self.caravan_group.id_number)
