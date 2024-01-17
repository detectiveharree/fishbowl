from ai.groupai.task.taskgroup import TaskGroup
from ai.groupai.actions.actiongroupcreatecaravan import ActionGroupCreateCaravan
from ai.groupai.actions.caravan.actiongroupcaravanmove import ActionGroupCaravanMove
from ai.groupai.actions.caravan.actiongroupcaravanswitchgroup import ActionGroupCaravanSwitchGroup
from ai.groupai.actions.caravan.actiongroupcaravanrejoinparentgroup import ActionGroupCaravanRejoinParentGroup
from ai.groupai.task.caravan.taskgroupcaravanrejoinparentgroup import TaskGroupCaravanRejoinParentGroup
import global_params
from items.itemresources.itemresource import ResourceType
from ai.groupai.needs.needgroup import GROUP_NEED_TYPE

"""
Task for trying to combine two groups (should be applied to caravan) (requires permission from other group)
"""
class TaskGroupCaravanSwitchGroup(TaskGroup):

    def __init__(self, group, other_group, group_destination):
        super(). __init__(0, GROUP_NEED_TYPE.SWITCHING_GROUP)
        self.group = group
        self.original_group_meeting_point = group.stockpile_location
        self.group_destination = group_destination
        self.other_group = other_group
        self.switch_group_action = None


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
        self.switch_group_action = ActionGroupCaravanSwitchGroup(self, self.group, self.other_group)
        return [[ActionGroupCaravanMove(self, True, self.group, self.group_destination)],
                [self.switch_group_action]]



    """
    Called when the task is finished.
    This can occur naturally (i.e. action tree finishing) or if a task is force quited.
    """
    def finish_task(self, human):
        if self.switch_group_action is not None:
            if not self.switch_group_action.permission:
                self.group.add_task(TaskGroupCaravanRejoinParentGroup(self.group))


    def __repr__(self):
        return str("Switch to group %s" % str(self.other_group.id_number))