from ai import task
import ai.humanai.actions.actionsleep
from ai.need import NEED_TYPE
import guiwindow


class TaskGoSleep(task.Task):

    def __init__(self, human):
        self.human = human



    """
    Possible actions that the user can do to satisfy this pre requisite.
    Note the action with the cheapest action tree will be picked.
    """
    def possible_actions(self):
        return [self.human.sleeping_location.get_action()]


    """
    Called when the a action in a task has failed.
    Must Return a action tree.
    Default: returns best action tree
    """
    def action_failed_response(self, human):
        return []

    def __repr__(self):
        return str("Go to sleep")