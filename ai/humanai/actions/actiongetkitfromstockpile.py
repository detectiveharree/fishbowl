from ai.action import Action
from ai.humanai.prerequisites.prerequisiteatstockpile import PrerequisiteAtStockpile
from ai.humanai.prerequisites.prerequisiteknowssurvivalresourceatstockpile import PrerequisitesKnowsSurvivalResourceAtStockpile

"""
Picks up resource from stockpile.

A wrapper for performing an action, including a cost function, prerequisite conditions and worker logic.
"""
class ActionGetKitFromStockpile(Action):


    """
    Returns a list of prerequisites that must be satisfied in order to complete the action.
    
    Note the order of these prerequisites reflects the order of their potential actions that need
    to be completed for this action to be possible to do. Therefore order it appropriately.
    Note the action may not necessarily be executed if all the prerequisites are true. 
    The prerequisites are used in the decision making process, however the optional
    method pre_begin_checks returns the final check before the action is executed in case new information
    is is revealed.
    """
    def get_prerequisites(self):
        return [PrerequisiteAtStockpile()]


    """
    The estimated cost of this action.
    This occurs during the decision making process of a action tree.
    For extra accuracy, use data from prerequisites.
    """
    def get_costs(self,  human):

        return 0

    """
    Returns true/false if the action should proceed.
    Optional final checks that occur prior to the action starting (i.e. action is currently in a action tree).
    """
    def pre_begin_checks(self,  human):
        return PrerequisiteAtStockpile().is_satisfied(human)

    """
    This is called once when the action begins.
    """
    def begin(self, human):
        for item in human.group.knowledge_group_item_inventory.remove_all_items_from_collection(human.id_number):
            item.equip(human)

    """
    Called every tick while the action has begun and not completed yet.
    Returns True/False to indicate if an error occurs.
    """
    def tick(self,  human):
        return True

    """
    Returns true/false to indicate whether the action is complete or not.
    Called every tick before tick() is executed.    
    """
    def is_complete(self,  human):
        return True

    def __str__(self):
        return "Collect kit from stockpile"
