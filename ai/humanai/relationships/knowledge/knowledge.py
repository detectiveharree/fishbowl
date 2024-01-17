from abc import ABC, abstractmethod


"""
Knowledge is a framework for quickly looking up and registering information in a human.
"""
class Knowledge(ABC):

    """
    Given a human object, register the information in this class to that person.
    """
    @abstractmethod
    def register_from_information(self, human, information):
        ...

    """
    Use this method to return a random piece of information
    that you can create from the knowledge. 
    This is for use in interactions, get_random_information may be called
    to simulate random conversation being passed.
    """
    @abstractmethod
    def get_random_information(self):
        ...



