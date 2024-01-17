from ai.action import Action
from ai.humanai.prerequisites.prerequisiteknowsinteractablecelllocation import PrerequisiteKnowsInteractableCellLocation
from ai import pathfinding
import logging

"""
Goes to a free resource.

A wrapper for performing an action, including a cost function, prerequisite conditions and worker logic.
"""


class ActionGoToInteractableCell(Action):

    """
    DO NOT DELETE THIS. PASTE THIS IN FOR EVERY NEW OBJECT THAT WILL BE STORED IN A SET/DICTIONARY.
    THIS IS ESSENTIAL FOR MAKING SURE THE PROGRAM PERFORMS EXACTLY THE SAME EVERY TIME!

    assert(false) WILL CRASH THE PROGRAM IF YOU ATTEMPT TO PUT THIS OBJECT INTO A SET/DICT WITHOUT FIRST MODIFYING THE FUNCTION.
    THIS IS DONE ON PURPOSE TO PREVENT YOU FROM ACCIDENTALLY LEAKING NON-DETERMINISM INTO THE PROGRAM.
    SPEAK TO ME (TOM) AND I WILL EXPLAIN WHAT TO DO.
    """
    def __hash__(self):
        assert(False)

    def __init__(self, cell_category, cell_type):
        self.cell_category = cell_category
        self.cell_type = cell_type
        self.closest_loc = None


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
        return [PrerequisiteKnowsInteractableCellLocation(self.cell_category, self.cell_type)]

    """
    The estimated cost of this action.
    This occurs during the decision making process of a action tree.
    For extra accuracy, use data from prerequisites.
    """

    def get_costs(self, human):
        if PrerequisiteKnowsInteractableCellLocation(self.cell_category, self.cell_type).is_satisfied(human):
            possible_locs = tuple(PrerequisiteKnowsInteractableCellLocation(self.cell_category, self.cell_type).get_data(human))
            closest_loc = pathfinding.flood_fill_find_closest(human.location, possible_locs)
            # logging.info("Closest loc is %s out of %s" % (str(closest_loc), possible_locs))
            # if closest_loc == ():
            #     exit(1)
            return len(pathfinding.get_route(human.location, closest_loc))
        """
        If we don't know a free location here is the cost.
        """
        return 1000

    """
    Returns true/false if the action should proceed.
    Optional final checks that occur prior to the action starting (i.e. action is currently in a action tree).
    """

    def pre_begin_checks(self, human):
        possible_locs = tuple(PrerequisiteKnowsInteractableCellLocation(self.cell_category, self.cell_type).get_data(human))
        self.closest_loc = pathfinding.flood_fill_find_closest(human.location, possible_locs)
        # if self.closest_loc is None:
        #     logging.info("WHY NONE %s -> %s" % (human.location, possible_locs))
        return self.closest_loc is not None

    """
    This is called once when the action begins.
    """

    def begin(self, human):
        human.find(self.closest_loc)

    """
    Called every tick while the action has begun and not completed yet.
    Returns True/False to indicate if an error occurs.
    """

    def tick(self, human):
        human.step_towards_route()
        return True

    """
    Returns true/false to indicate whether the action is complete or not.
    Called every tick before tick() is executed.    
    """

    def is_complete(self, human):
        return human.arrived_at_location()

    def __str__(self):
        return "Going to interactable cell %s %s" % (self.cell_category, self.cell_type)

