from ai import task
import ai.humanai.actions.actiongotolocation
from ai.humanai.actions.actionbattle import ActionBattle


class TaskBattle(task.Task):

    def __init__(self, human, group_action, personal_safe_zone_location):
        self.human = human
        self.group_action = group_action
        self.personal_safe_zone_location = personal_safe_zone_location

    """
    Possible actions that the user can do to satisfy this pre requisite.
    Note the action with the cheapest action tree will be picked.
    """
    def possible_actions(self):
        return [ActionBattle(self.human, self.group_action, self.personal_safe_zone_location)]


    def __repr__(self):
        return str("Battling")