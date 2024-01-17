from ai.groupai.actions.actiongroup import ActionGroup
from ai.humanai.task.taskjoingroup import TaskJoinGroup
from ai.humanai.task.taskmovewithcaravan import TaskMoveWithCaravan
from ai.humanai.task.taskassignedtask import TaskAssignedTask
import math
from ai.humanai.task.taskbattle import TaskBattle
from ai.need import NEED_TYPE
from ai import pathfinding
from ai.groupai.actions.caravan.actiongroupcaravan import ActionGroupCaravan

"""
Moves an entire group along a specific path
"""
class ActionGroupCaravanBattle(ActionGroupCaravan):

    def __init__(self, parent_task, interaction_group_participant, interaction_group_battle):
        super().__init__(parent_task) # ALWAYS CALL PARENT CONSTRUCTOR
        self.interaction_group_battle = interaction_group_battle
        self.interaction_group_participant = interaction_group_participant
        self.damage_requirement = 0

    """
    Should give the workers there tasks.
    """
    def activate(self, hours_left, available_people, group):
        formation_shape = pathfinding.flood_fill_radius

        expansion_size = pathfinding.find_minimum_expansion_function_size(formation_shape,
                                                                               self.interaction_group_participant.starting_position_location,
                                                                               1,
                                                                               len(group.members))

        locations = list(formation_shape(self.interaction_group_participant.starting_position_location, expansion_size))
        members = list(group.members)

        for i in range(len(members)):
            member = members[i]
            safe_zone_location = locations[i]

            member.needs[NEED_TYPE.GROUP_TASK].set_daily_task(member, TaskBattle(member, self, safe_zone_location), 10000)



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
        return "Battle"

    def __str__(self):
        return "Battle"
