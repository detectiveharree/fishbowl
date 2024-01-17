from ai.groupai.task.taskgroup import TaskGroup
from ai.groupai.actions.caravan.actiongroupcaravanmove import ActionGroupCaravanMove
from ai.groupai.actions.caravan.actiongroupcaravanprebattle import ActionGroupCaravanPreBattle
from ai.groupai.actions.caravan.actiongroupcaravanbattle import ActionGroupCaravanBattle
from ai.groupai.needs.needgroup import GROUP_NEED_TYPE
from enum import Enum


class BATTLE_ACTION(Enum):
    RETREAT = 1 # Group retreats back to base
    FIGHT = 2 # proceed with battle
    SCATTER = 3 # Caravan group splits up

    def __repr__(self):
        return self.name

class TaskGroupCaravanBattle(TaskGroup):


    def __init__(self, group, interaction_group_participant, interaction_group_battle, callback = lambda outcome : None):
        super(). __init__(0, GROUP_NEED_TYPE.NONE)
        self.group = group
        self.interaction_group_participant = interaction_group_participant
        self.interaction_group_battle = interaction_group_battle
        self.battle_over_callback = callback


    """
    Must return true/false.
    In some cases (especially for caravan tasks) it is necessary that when the task is registered
    it becomes the sole task of the group i.e. clears all other tasks.
    This will also prevent other non only tasks but will be replaced by a only task another being registered.
    """
    def should_be_only_group_task(self):
        return True

    """
    Must return True/False
    If true, resets the progress of all actions and the action queue
    every time this task is activated i.e. activate() function is called 
    Action queue will be assigned to possible_actions().
    """
    def reset_action_tree_on_activation(self):
        return False

    """
    Possible actions that the user can do to satisfy this pre requisite.
    Note the action with the cheapest action tree will be picked.
    """
    def possible_actions(self):
        return [[ActionGroupCaravanMove(self, False, self.group, self.interaction_group_participant.starting_position_location)],
                [ActionGroupCaravanPreBattle(self, self.interaction_group_participant, self.interaction_group_battle)],
                [ActionGroupCaravanBattle(self, self.interaction_group_participant, self.interaction_group_battle)]]


    """
    Called when the task is finished.
    This can occur naturally (i.e. action tree finishing) or if a task is force quited. 
    """
    def finish_task(self, group):
        self.interaction_group_battle.leave_interaction(self.interaction_group_participant)
        self.battle_over_callback(self.interaction_group_participant.battle_outcome)


    def __repr__(self):
        return str("Battle\n Started: %s" % self.interaction_group_battle.wait_period_over)