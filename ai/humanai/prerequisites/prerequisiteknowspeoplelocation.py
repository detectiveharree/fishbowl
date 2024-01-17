from ai.prerequisite import Prerequisite
import ai.humanai.actions.actionlookforfreeresource
from ai import pathfinding
import math

"""
Is the human knows of a resource location that is currently empty.

A Prerequisite is a predicate that must be true to complete a action.
It is a prediction/estimation based on information that a human has, 
that is used when a human undergoes decision making. Therefore, 
DO NOT leak information that the human does not know i.e. world data.
"""
class PrerequisiteKnowsPeopleLocation(Prerequisite):


    """
    Returns a list of possible actions that may satisfy this prerequisite.
    """
    def possible_actions(self, human):
        return []

    """
    Return known locations of resource
    """
    def get_data(self, human):

        """
        Basically, for all locations person knows of people,
        find the smallest euclidan distance in those locations to find someone.
        """
        possible_locs = [(pathfinding.get_euclidean_distance(human.location, location), location)
                         for location in  human.knowledge_people_locations.get_all_locations()]

        target = sorted(possible_locs
            , key=lambda x: x[0])[0][1]
        return target

    """
    Returns true/false if the current prerequisite is satisfied.
    """
    def is_satisfied(self, human):
        return human.knowledge_people_locations.amount_known_locations_with_people() > 0



