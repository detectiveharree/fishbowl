from ai.action import Action
from ai.humanai.prerequisites.prerequisiteatlocation import PrerequisiteAtLocation
from ai.humanai.needs.needbettersleepinglocation import NeedBetterSleepingLocation
import global_params
import guiwindow
from ai.need import NEED_TYPE
from humanbase import HumanState

"""
Harvests a resource that player is currently on

A wrapper for performing an action, including a cost function, prerequisite conditions and worker logic.
"""


class ActionSleep(Action):

    def __init__(self, sleeping_location):
        self.sleeping_location = sleeping_location


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
        return [PrerequisiteAtLocation(self.sleeping_location)]

    """
    The estimated cost of this action.
    This occurs during the decision making process of a action tree.
    For extra accuracy, use data from prerequisites.
    """

    def get_costs(self, human):
        """
        Amount to harvest is the cost of harvesting.
        """
        return 0

    """
    Returns true/false if the action should proceed.
    Optional final checks that occur prior to the action starting (i.e. action is currently in a action tree).
    """

    def pre_begin_checks(self, human):

        if not PrerequisiteAtLocation(self.sleeping_location).is_satisfied(human):
            return False

        """
        This check is necessary for when a persons sleeping loc is invalidated while they are  travelling to it.
        """
        if human.sleeping_location is None:
            return False

        if not human.sleeping_location.check_still_valid(human):
            human.needs[NEED_TYPE.BETTER_SLEEPING_LOCATION].set_new_sleeping_location(human, None)
            return False

        human.needs[NEED_TYPE.BETTER_SLEEPING_LOCATION].update_need_level(human)
        return True

    """
    This is called once when the action begins.
    """

    def begin(self, human):
        # update the sleeping location score every time they go sleep
        human.sleep_hour = guiwindow.WORLD_INSTANCE.time_hour
        human.state = HumanState.SLEEPING
        pass

    """
    Called every tick while the action has begun and not completed yet.
    Returns True/False to indicate if an error occurs.
    """

    def tick(self, human):
        amount_reduce = global_params.tired_rejuvination_rate
        if human.needs[NEED_TYPE.SLEEP].need_level < global_params.tired_rejuvination_rate:
            amount_reduce = human.needs[NEED_TYPE.SLEEP].need_level
        human.needs[NEED_TYPE.SLEEP].need_level -= amount_reduce

        if human.needs[NEED_TYPE.SLEEP].need_level == 0:
            human.state = HumanState.AWAKE
        return True

    """
    Returns true/false to indicate whether the action is complete or not.
    Called every tick before tick() is executed.    
    """

    def is_complete(self, human):
        return human.state == HumanState.AWAKE

    def __str__(self):
        return "Go to sleep"
