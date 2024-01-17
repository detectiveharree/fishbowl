from ai.action import Action
import ai.humanai.prerequisites.prerequisitehasresourceininventory
from ai.humanai.prerequisites.prerequisiteatlocation import PrerequisiteAtLocation
import logging

"""
Action for joining group.
Can fail if permission is refused
"""


class ActionJoinGroup(Action):

    def __init__(self, group, action_group_switch_group):
        self.group = group
        self.action_group_switch_group = action_group_switch_group

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
        pass

    """
    Called every tick while the action has begun and not completed yet.
    Returns True/False to indicate if an error occurs.
    """

    def tick(self, human):
        self.action_group_switch_group.asked = True

        # after witnessing the group again, it's possible
        # that they find their group is not as good as they thought when they finally arrive there
        # therefore don't join it
        if human.knowledge_groups.get_best_possible_group() != self.group.id_number:
            logging.info("%s decided against joining group %s after arriving there" % (human.id_number, self.group.id_number))
            self.action_group_switch_group.permission = False
        else:
            self.action_group_switch_group.permission = self.group.request_permission_to_join(human.group)
            human.knowledge_groups.get_knowledge_of_group(self.group.id_number).attempt_join()
            if self.action_group_switch_group.permission:
                human.switch_group(self.group)
                logging.info("%s allowed into group %s" % (human.id_number, self.group.id_number))
            else:
                logging.info("%s was refused entry into group %s" % (human.id_number, self.group.id_number))
        return self.action_group_switch_group.permission

    """
    Returns true/false to indicate whether the action is complete or not.
    Called every tick before tick() is executed.    
    """

    def is_complete(self, human):
        return self.action_group_switch_group.asked

    def __str__(self):
        return "Join group %s" % (self.group.id_number)
