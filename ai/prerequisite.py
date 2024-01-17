from abc import ABC, abstractmethod

"""
A Prerequisite is a predicate that must be true to complete a action.
It is a prediction/estimation based on information that a human has, 
that is used when a human undergoes decision making. Therefore, 
DO NOT leak information that the human does not know i.e. world data.

ABC is a abstract base class.
Means we can never instantiate a Prerequisite object.
Instead we have to extend it, and complete the functions to do it. 
"""
class Prerequisite(ABC):


    """
    Returns a list of possible actions that may satisfy this prerequisite.
    """
    def possible_actions(self, human):
        return []

    """
    Returns true/false if the current prerequisite is satisfied.
    """
    @abstractmethod
    def is_satisfied(self, human):
        ...



