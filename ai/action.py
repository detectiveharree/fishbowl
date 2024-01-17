from abc import ABC, abstractmethod

"""
A wrapper for performing an action, including a cost function, prerequisite conditions and worker logic.

ABC is a abstract base class.
Means we can never instantiate a Action object.
Instead we have to extend it, and complete the functions to do it. 
"""
class Action(ABC):


    def get_unsatisifed_prerequisites(self, human):
        unsatisifed = []
        for prerequisite in self.get_prerequisites():
            if not prerequisite.is_satisfied(human):
                unsatisifed.append(prerequisite)
        return unsatisifed


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
        return []


    """
    The estimated cost of this action.
    This occurs during the decision making process of a action tree.
    For extra accuracy, use data from prerequisites.
    """
    @abstractmethod
    def get_costs(self, human):
        ...

    """
    Returns true/false if the action should proceed.
    Optional final checks that occur prior to the action starting (i.e. action is currently in a action tree).
    """
    def pre_begin_checks(self, human):
        return True

    """
    This is called once when the action begins.
    """
    @abstractmethod
    def begin(self, human):
        ...

    """
    Called every tick while the action has begun and not completed yet.
    Returns True/False to indicate if an error occurs.
    """
    @abstractmethod
    def tick(self, human):
        ...

    """
    Returns true/false to indicate whether the action is complete or not.
    Called every tick before tick() is executed.    
    """
    @abstractmethod
    def is_complete(self, human):
        ...

    """
    Called whenever a action is completed 
    """
    def on_finish(self, human):
        pass

    def __repr__(self):
        return str(self)



