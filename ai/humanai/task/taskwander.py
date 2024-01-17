from ai import task
from ai.humanai.actions.actionwander import ActionWander


class TaskWander(task.Task):


    def __init__(self, human):

        self.human = human

    """
    Possible actions that the user can do to satisfy this pre requisite.
    Note the action with the cheapest action tree will be picked.
    """
    def possible_actions(self):
        return [ActionWander(self.human)]


    def __repr__(self):
        return str("Wander around")