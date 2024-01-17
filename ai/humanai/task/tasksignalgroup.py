from ai import task
import ai.humanai.actions.actiongotolocation
from ai.humanai.actions.actiongotolocation import ActionGoToLocation
from ai.need import NEED_TYPE


class TaskSignalGroup(task.Task):

    def __init__(self, human):
        self.human = human


    """
    Possible actions that the user can do to satisfy this pre requisite.
    Note the action with the cheapest action tree will be picked.
    """
    def possible_actions(self):
        return [ActionGoToLocation(self.human.group.stockpile_location)]


    """
    Called when the action tree is completed.
    Returns True/False. If true, task will terminate, else the task will be restarted via begin()
    Default: returns true
    """
    def is_task_complete(self, human):
        """
        This just confirms that the person does not attempt
        to interact again (although he may have found someone who agrees,
        this task may get activated again)
        """
        human.needs[NEED_TYPE.SIGNAL_GROUP].finish_signal(human)
        return True


    def __repr__(self):
        return str("Signalling group")