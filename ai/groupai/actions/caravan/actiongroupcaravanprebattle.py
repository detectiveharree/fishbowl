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
class ActionGroupCaravanPreBattle(ActionGroupCaravan):

    def __init__(self, parent_task, interaction_group_participant, interaction_group_battle):
        super().__init__(parent_task) # ALWAYS CALL PARENT CONSTRUCTOR
        self.interaction_group_participant = interaction_group_participant
        self.interaction_group_battle = interaction_group_battle


    """
    Should give the workers there tasks.
    """
    def activate(self, hours_left, available_people, group):
        self.interaction_group_participant.at_battle_starting_position = True
        for worker in list(group.members):
            worker.needs[NEED_TYPE.GROUP_TASK].set_daily_task(worker, TaskStay(self), 10000)


    """
    Returns true/false to indicate whether the action is complete or not.
    Called every tick before tick() is executed.    
    """

    def is_complete(self, group):
        return not self.interaction_group_battle.pre_battle_tick() or\
               self.interaction_group_battle.wait_period_over


    def __str__(self):
        return "Pre-Battle"
