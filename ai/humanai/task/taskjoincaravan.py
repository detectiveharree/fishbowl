from ai import task
import ai.humanai.actions.actionsleep
from ai.humanai.actions.actiongotolocation import ActionGoToLocation
from ai.humanai.actions.actionjoincaravan import ActionJoinCaravan

"""
Task for joining a caravan
"""
class TaskJoinCaravan(task.Task):

    def __init__(self, caravan_group, group_action):
        self.caravan_group = caravan_group
        self.group_action = group_action



    """
    Possible actions that the user can do to satisfy this pre requisite.
    Note the action with the cheapest action tree will be picked.
    """
    def possible_actions(self):
        return [ActionJoinCaravan(self.caravan_group, self.group_action)]


    def __repr__(self):
        return str("Join group %s" % self.caravan_group.id_number)