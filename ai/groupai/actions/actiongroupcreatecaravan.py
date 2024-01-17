from ai.groupai.actions.actiongroup import ActionGroup
from ai.humanai.task.taskjoincaravan import TaskJoinCaravan
import math
from ai.need import NEED_TYPE

"""
Assigns people task of joining a caravan group (child group of group) (no permission required to join) 
"""
class ActionGroupCreateCaravan(ActionGroup):

    def __init__(self, parent_task, caravan_group, caravan_people):
        super().__init__(parent_task) # ALWAYS CALL PARENT CONSTRUCTOR
        self.caravan_group = caravan_group
        self.caravan_people = caravan_people
        self.timer = 0
        self.remind_join_timer = 100

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
        return self.caravan_people

    """
    Should give the workers there tasks.
    """
    def activate(self, hours_left, available_people, group):
        for worker in list(self.caravan_people):
            worker.needs[NEED_TYPE.GROUP_TASK].set_daily_task(worker, TaskJoinCaravan(self.caravan_group, self), 10000)

    """
    The estimated cost of this action.
    This occurs during the decision making process of a action tree.
    For extra accuracy, use data from prerequisites.
    """

    def get_costs(self, group):
        return 0

    """
    Called every tick while the action has begun and not completed yet.
    Returns True/False to indicate if an error occurs.
    """
    def tick(self, group):
        self.timer += 1
        # if self.timer == len(self.group.members):


        if self.timer >= self.remind_join_timer:

            for worker in self.caravan_people:
                if not worker.group.id_number == self.caravan_group.id_number:
                    if not isinstance(worker.current_task, TaskJoinCaravan):
                        worker.needs[NEED_TYPE.GROUP_TASK].set_daily_task(worker, TaskJoinCaravan(self.caravan_group, self),
                                                                          10000)

            self.timer = 0

        return True

    """
    Returns true/false to indicate whether the action is complete or not.
    Called every tick before tick() is executed.    
    """

    def is_complete(self, group):
        # print([member.id_number for member in self.caravan_group.members])
        # print([member.id_number for member in self.caravan_people])
        return len(self.caravan_group.members) == len(self.caravan_people)

    """
    Optional, gives tickly debug information.
    """

    def get_stats(self, group):
        return "members (%s/%s)" % (len(self.caravan_group.members), len(self.caravan_people))

    def __str__(self):
        return "Create caravan (%s)" % (self.caravan_group.id_number)
