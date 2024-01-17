from ai.action import Action
from ai.humanai.prerequisites.prerequisiteatlocation import PrerequisiteAtLocation
import global_params
from ai.humanai.skill import SKILL_TYPE
import guiwindow

"""
Harvests a resource that player is currently on

A wrapper for performing an action, including a cost function, prerequisite conditions and worker logic.
"""
class ActionBuildBuilding(Action):

    """
    DO NOT DELETE THIS. PASTE THIS IN FOR EVERY NEW OBJECT THAT WILL BE STORED IN A SET/DICTIONARY.
    THIS IS ESSENTIAL FOR MAKING SURE THE PROGRAM PERFORMS EXACTLY THE SAME EVERY TIME!

    assert(false) WILL CRASH THE PROGRAM IF YOU ATTEMPT TO PUT THIS OBJECT INTO A SET/DICT WITHOUT FIRST MODIFYING THE FUNCTION.
    THIS IS DONE ON PURPOSE TO PREVENT YOU FROM ACCIDENTALLY LEAKING NON-DETERMINISM INTO THE PROGRAM.
    SPEAK TO ME (TOM) AND I WILL EXPLAIN WHAT TO DO.
    """
    def __hash__(self):
        assert(False)


    def __init__(self, building, group_action):
        self.building = building
        self.group_action = group_action


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
        return [PrerequisiteAtLocation(list(self.building.locations)[0])]


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
        return PrerequisiteAtLocation(list(self.building.locations)[0]).is_satisfied(human)

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
        amount_per_tick = human.skills[SKILL_TYPE.BUILDING] * SKILL_TYPE.BUILDING.default_harvest_rate_tick
        self.group_action.register_progress(human, amount_per_tick, human.group)
        return True


    """
    Returns true/false to indicate whether the action is complete or not.
    Called every tick before tick() is executed.    
    """
    def is_complete(self, human):
        return self.building.is_building_complete()




    def __str__(self):
        return "Building %s at %s" % (self.building, str(self.building.locations))
