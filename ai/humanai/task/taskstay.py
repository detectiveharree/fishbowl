from ai import task
import ai.humanai.actions.actiongotolocation
from ai.humanai.actions.actionstay import ActionStay


class TaskStay(task.Task):

    def __init__(self, group_action):
        self.group_action = group_action

    """
    Possible actions that the user can do to satisfy this pre requisite.
    Note the action with the cheapest action tree will be picked.
    """
    def possible_actions(self):
        return [ActionStay()]


    def __repr__(self):
        return str("Staying")