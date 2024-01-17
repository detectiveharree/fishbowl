from ai.groupai.actions.actiongroup import ActionGroup
from ai.humanai.task.taskjoingroup import TaskJoinGroup
from ai.humanai.task.taskmovewithcaravan import TaskMoveWithCaravan
from ai.humanai.task.taskassignedtask import TaskAssignedTask
import math
from ai.humanai.task.taskbattle import TaskBattle
from ai.need import NEED_TYPE
from ai.humanai.task.taskstay import TaskStay
from ai import pathfinding
from ai.groupai.actions.caravan.actiongroupcaravan import ActionGroupCaravan


"""
Waits for opposite army to arrive, registers occupant information
then decides on what to do.
"""
class ActionGroupCaravanOccupy(ActionGroupCaravan):

    def __init__(self, parent_task):
        super().__init__(parent_task) # ALWAYS CALL PARENT CONSTRUCTOR
        self.amount_time_to_obtain = 100
        self.timer = 0


    """
    Should give the workers there tasks.
    """
    def activate(self, hours_left, available_people, group):
        # self.interaction_group_participant.at_battle_starting_position = True
        for worker in list(group.members):
            worker.needs[NEED_TYPE.GROUP_TASK].set_daily_task(worker, TaskStay(self), 10000)


    def tick(self, group):
        self.timer += 1


    """
    Returns true/false to indicate whether the action is complete or not.
    Called every tick before tick() is executed.    
    """

    def is_complete(self, group):
        return self.timer >= self.amount_time_to_obtain or\
               self.parent_task.campaign.interaction_group_battle is not None


    def __str__(self):
        return "Occupy"
