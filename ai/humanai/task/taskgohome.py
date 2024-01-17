from ai import task
import ai.humanai.actions.actiongotolocation


"""
Task for consuming a resource
"""
class TaskGoHome(task.Task):


    def __init__(self, location):
        self.location = location

    """
    Possible actions that the user can do to satisfy this pre requisite.
    Note the action with the cheapest action tree will be picked.
    """
    def possible_actions(self):
        return [ai.humanai.actions.actiongotolocation.ActionGoToLocation(self.location)]

    def __repr__(self):
        return str("Go go home %s" % (str(self.location)))