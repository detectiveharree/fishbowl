from ai.groupai.task.taskgroup import TaskGroup
from ai.groupai.actions.caravan.actiongroupcaravanmove import ActionGroupCaravanMove
from ai.groupai.actions.caravan.actiongroupcaravanoccupy import ActionGroupCaravanOccupy
from ai.groupai.needs.needgroup import GROUP_NEED_TYPE


class TaskGroupCaravanCampaignOccupy(TaskGroup):



    def __init__(self, group, occupy_location, campaign, callback = lambda interaction_battle : None):
        super(). __init__(0, GROUP_NEED_TYPE.NONE)
        self.group = group
        self.occupy_location = occupy_location
        self.occupation_response_callback = callback
        self.campaign = campaign

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
        return [[ActionGroupCaravanMove(self, False, self.group, self.occupy_location, self.group.stockpile_location)],
                [ActionGroupCaravanOccupy(self)]]

    """
    Called when the task is finished.
    This can occur naturally (i.e. action tree finishing) or if a task is force quited. 
    """
    def finish_task(self, group):
        self.occupation_response_callback()

    def __repr__(self):
        return str("Hold position %s" % str(self.occupy_location))