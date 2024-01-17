from ai import task
from ai.humanai.actions.actiongetkitfromstockpile import ActionGetKitFromStockpile


"""
Task for consuming a resource
"""
class TaskGetKitFromStockpile(task.Task):


    def __init__(self, need_type):
        self.need_type = need_type

    """
    Possible actions that the user can do to satisfy this pre requisite.
    Note the action with the cheapest action tree will be picked.
    """
    def possible_actions(self):
        return [ActionGetKitFromStockpile()]


    def __repr__(self):
        return str("Get kit from stockpile")
