from ai.action import Action
import ai.humanai.prerequisites.prerequisitehasresourceininventory
from ai.humanai.prerequisites.prerequisiteatlocation import PrerequisiteAtLocation

"""
Action for joining caravan.
No permission is required
"""

class ActionJoinCaravan(Action):

    def __init__(self, group, group_action):
        self.group = group
        self.group_action = group_action

    """
    The estimated cost of this action.
    This occurs during the decision making process of a action tree.
    For extra accuracy, use data from prerequisites.
    """

    def get_costs(self, human):
        return 0


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
        return [PrerequisiteAtLocation(self.group.stockpile_location)]

    """
    Returns true/false if the action should proceed.
    Optional final checks that occur prior to the action starting (i.e. action is currently in a action tree).
    """

    def pre_begin_checks(self, human):
        return True
    """
    This is called once when the action begins.
    """

    def begin(self, human):
        human.switch_group(self.group)

    """
    Called every tick while the action has begun and not completed yet.
    Returns True/False to indicate if an error occurs.
    """

    def tick(self, human):
        return True

    """
    Returns true/false to indicate whether the action is complete or not.
    Called every tick before tick() is executed.    
    """

    def is_complete(self, human):
        return True

    def __str__(self):
        return "Join group %s" % (self.group.id_number)
