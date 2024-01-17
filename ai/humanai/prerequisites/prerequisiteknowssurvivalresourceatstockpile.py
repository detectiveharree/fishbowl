from ai.prerequisite import Prerequisite

"""
Is the human believes a certain amount of resource exists at their stockpile.

A Prerequisite is a predicate that must be true to complete a action.
It is a prediction/estimation based on information that a human has, 
that is used when a human undergoes decision making. Therefore, 
DO NOT leak information that the human does not know i.e. world data.
"""
class PrerequisitesKnowsSurvivalResourceAtStockpile(Prerequisite):

    def __init__(self, resource, amount):
        self.resource = resource
        self.amount = amount

    """
    Return known locations of resource
    """
    def get_data(self, human):
        return human.knowledge_group_stockpile_contents.get_stockpile_resource_contents(human.group.id_number, self.resource)

    """
    Returns true/false if the current prerequisite is satisfied.
    """
    def is_satisfied(self, human):
        # print(human.knowledge_group_stockpile_contents.get_stockpile_resource_contents(human.group.id_number, self.resource))
        return human.knowledge_group_stockpile_contents.get_stockpile_resource_contents(human.group.id_number, self.resource) >= self.amount

