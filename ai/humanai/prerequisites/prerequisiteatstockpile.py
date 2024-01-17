from ai.prerequisite import Prerequisite
import ai.humanai.actions.actiongotolocation

"""
Is the human currently at the stockpile location.

A Prerequisite is a predicate that must be true to complete a action.
It is a prediction/estimation based on information that a human has, 
that is used when a human undergoes decision making. Therefore, 
DO NOT leak information that the human does not know i.e. world data.
"""
class PrerequisiteAtStockpile(Prerequisite):


    """
    Returns a list of possible actions that may satisfy this prerequisite.
    """
    def possible_actions(self, human):
        return [ai.humanai.actions.actiongotolocation.ActionGoToLocation(human.group.stockpile_location)]

    """
    Returns true/false if the current prerequisite is satisfied.
    """
    def is_satisfied(self, human):
        return human.group.stockpile_location == human.location

