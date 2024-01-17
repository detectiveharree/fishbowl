from ai.groupai.actions.actiongroup import ActionGroup
from ai.humanai.task.taskrejoinparentgroup import TaskRejoinParentGroup
from ai.humanai.task.taskjoingroup import TaskJoinGroup
import math
from ai.need import NEED_TYPE
import logging
from ai.groupai.actions.caravan.actiongroupcaravan import ActionGroupCaravan

"""
Trys to let a group combine with another (permission is required from the other group)
"""
class ActionGroupCaravanSwitchGroup(ActionGroupCaravan):


    def __init__(self, parent_task, caravan_group, other_group):
        super().__init__(parent_task) # ALWAYS CALL PARENT CONSTRUCTOR
        self.caravan_group = caravan_group
        self.other_group = other_group
        self.asked = False
        self.permission = False

        self.timer = 0
        self.remind_join_timer = 100

    """
    Should give the workers there tasks.
    """
    def activate(self, hours_left, available_people, group):
        for worker in list(group.members):
            worker.needs[NEED_TYPE.GROUP_TASK].set_daily_task(worker, TaskJoinGroup(self.other_group, self), 10000)


    """
    Called every tick while the action has begun and not completed yet.
    Returns True/False to indicate if an error occurs.
    """
    def tick(self, human):

        self.timer += 1

        if self.timer >= self.remind_join_timer:

            for worker in self.caravan_group.members:
                if not isinstance(worker.current_task, TaskJoinGroup):
                    worker.needs[NEED_TYPE.GROUP_TASK].set_daily_task(worker, TaskJoinGroup(self.other_group, self),
                                                                      10000)

            self.timer = 0

        return True

    """
    Returns true/false to indicate whether the action is complete or not.
    Called every tick before tick() is executed.    
    """

    def is_complete(self, group):
        # if self.asked:
        return self.asked


    def __str__(self):
        return "Switch group (%s -> %s)" % (self.caravan_group.id_number, self.other_group.id_number)
