from ai import task
import ai.humanai.actions.actionsleep
from ai.humanai.actions.actiongotolocation import ActionGoToLocation
from ai.humanai.actions.actionjoingroup import ActionJoinGroup

"""
Task for switching group (can fail if no permission)
"""
class TaskJoinGroup(task.Task):

    def __init__(self, caravan_group, action_group_switch_group):
        self.caravan_group = caravan_group
        self.action_group_switch_group = action_group_switch_group



    """
    Possible actions that the user can do to satisfy this pre requisite.
    Note the action with the cheapest action tree will be picked.
    """
    def possible_actions(self):
        return [ActionJoinGroup(self.caravan_group, self.action_group_switch_group)]


    def __repr__(self):
        return str("Join group %s" % self.caravan_group.id_number)