from abc import ABC, abstractmethod

class Information(ABC):


    """
    Given a human object, register the information in this class to that person.
    """
    @abstractmethod
    def register_to_knowledge(self, human):
        ...

    def __repr__(self):
        return "info: %s" % str(self)