from ai import task
import ai.humanai.actions.actiongotolocation
from ai.humanai.actions.actionbuildbuilding import ActionBuildBuilding


class TaskBuildBuilding(task.Task):

    def __init__(self, building, amount_ticks, group_action):
        self.building = building
        self.group_action = group_action


    """
    Possible actions that the user can do to satisfy this pre requisite.
    Note the action with the cheapest action tree will be picked.
    """
    def possible_actions(self):
        return [ActionBuildBuilding(self.building, self.group_action)]


    def __repr__(self):
        return str("Build building %s" % self.building)