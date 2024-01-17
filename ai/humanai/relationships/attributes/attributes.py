from abc import ABC, abstractmethod


class BoundedNumber(object):
    def __init__(self, value, min_, max_):
        self.min_ = min_
        self.max_ = max_
        self.n = value
        self.set(value)

    def set(self, newValue):
        self.n = max(self.min_, min(self.max_, newValue))

    def get(self):
        return self.n

    def change(self, delta):
        self.set(self.get() + delta)

"""
Attribute base class.

"""
class Attribute(ABC):


    """
    Used to determine if a task is "similar" to a other task.
    """
    @abstractmethod
    def difference(self, other):
         ...


"""
Scale attribute:
A value between -1 and 1
Also contains name correlating to -1 and 1 score.
"""
class ScaleAttribute():

    """
    DO NOT DELETE THIS. PASTE THIS IN FOR EVERY NEW OBJECT THAT WILL BE STORED IN A SET/DICTIONARY.
    THIS IS ESSENTIAL FOR MAKING SURE THE PROGRAM PERFORMS EXACTLY THE SAME EVERY TIME!

    assert(false) WILL CRASH THE PROGRAM IF YOU ATTEMPT TO PUT THIS OBJECT INTO A SET/DICT WITHOUT FIRST MODIFYING THE FUNCTION.
    THIS IS DONE ON PURPOSE TO PREVENT YOU FROM ACCIDENTALLY LEAKING NON-DETERMINISM INTO THE PROGRAM.
    SPEAK TO ME (TOM) AND I WILL EXPLAIN WHAT TO DO.
    """
    def __hash__(self):
        assert(False)

    def __init__(self, min_name, max_name, value):
        self.max_name = max_name
        self.min_name = min_name
        self.value = value

    """
    
    """
    @abstractmethod
    def as_percentage(self):
         ...


    def as_percentage(self):
        return (self.value + 1) / 2

    """
    I.e. max possible difference between two different scales
    """
    @staticmethod
    def max_difference():
        return 2

    def difference(self, other):
        return abs(self.value - other.value)


"""
Binary attribute.
Something thats true/false
"""
class BinaryAttribute():

    """
    DO NOT DELETE THIS. PASTE THIS IN FOR EVERY NEW OBJECT THAT WILL BE STORED IN A SET/DICTIONARY.
    THIS IS ESSENTIAL FOR MAKING SURE THE PROGRAM PERFORMS EXACTLY THE SAME EVERY TIME!

    assert(false) WILL CRASH THE PROGRAM IF YOU ATTEMPT TO PUT THIS OBJECT INTO A SET/DICT WITHOUT FIRST MODIFYING THE FUNCTION.
    THIS IS DONE ON PURPOSE TO PREVENT YOU FROM ACCIDENTALLY LEAKING NON-DETERMINISM INTO THE PROGRAM.
    SPEAK TO ME (TOM) AND I WILL EXPLAIN WHAT TO DO.
    """
    def __hash__(self):
        assert(False)

    def __init__(self, value, name):
        self.name = name
        self.value = value

    """
    If both are true, return 0, else 1
    """
    def difference(self, other):
        return 0 if self.value == other.value else 1