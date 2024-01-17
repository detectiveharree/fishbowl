from ai import task
from ai.humanai.actions.actionconsumeresource import ActionConsumeResource


"""
Task for consuming a resource
"""
class TaskConsumeResource(task.Task):


    def __init__(self, need_type, resource, amount):
        self.need_type = need_type
        self.resource = resource
        self.amount = amount

    """
    Possible actions that the user can do to satisfy this pre requisite.
    Note the action with the cheapest action tree will be picked.
    """
    def possible_actions(self):
        return [ActionConsumeResource(self.need_type, self.resource, self.amount)]


    def __repr__(self):
        return str("Consume %s %s" % (self.amount, self.resource))
