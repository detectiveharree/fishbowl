from abc import ABC, abstractmethod
from enum import Enum
import logging
"""
Limb base class, and RemovableLimb subclass
"""

class LIMB_TYPE(Enum):

    """
    DO NOT DELETE THIS. PASTE THIS IN FOR EVERY NEW OBJECT THAT WILL BE STORED IN A SET/DICTIONARY.
    THIS IS ESSENTIAL FOR MAKING SURE THE PROGRAM PERFORMS EXACTLY THE SAME EVERY TIME!

    assert(false) WILL CRASH THE PROGRAM IF YOU ATTEMPT TO PUT THIS OBJECT INTO A SET/DICT WITHOUT FIRST MODIFYING THE FUNCTION.
    THIS IS DONE ON PURPOSE TO PREVENT YOU FROM ACCIDENTALLY LEAKING NON-DETERMINISM INTO THE PROGRAM.
    SPEAK TO ME (TOM) AND I WILL EXPLAIN WHAT TO DO.
    """
    def __hash__(self):
        return hash(self.name)

    def __eq__(self, other):
        return self.__class__ == other.__class__ and self.name == other.name

    HEAD = 1
    TORSO = 2
    EYE = 3
    LEG = 4
    ARM = 5

    def __repr__(self):
        return self.name


class Limb(ABC):

    def __repr__(self):
        return str(self)

    @abstractmethod
    def get_limb_type(self):
        ...


class RemovableLimb(Limb):

    """
    DO NOT DELETE THIS. PASTE THIS IN FOR EVERY NEW OBJECT THAT WILL BE STORED IN A SET/DICTIONARY.
    THIS IS ESSENTIAL FOR MAKING SURE THE PROGRAM PERFORMS EXACTLY THE SAME EVERY TIME!

    assert(false) WILL CRASH THE PROGRAM IF YOU ATTEMPT TO PUT THIS OBJECT INTO A SET/DICT WITHOUT FIRST MODIFYING THE FUNCTION.
    THIS IS DONE ON PURPOSE TO PREVENT YOU FROM ACCIDENTALLY LEAKING NON-DETERMINISM INTO THE PROGRAM.
    SPEAK TO ME (TOM) AND I WILL EXPLAIN WHAT TO DO.
    """
    def __hash__(self):
        assert(False)

    def __init__(self):
        self.is_intact = True

    def dismember(self, human):
        logging.info("%s lost his %s!" % (human.id_number, self.get_limb_type()))
        self.is_intact = False


"""
Subclasses of Limb and Removable limb to denote all relevant limbs
"""


class Head(Limb):

    def get_limb_type(self):
        return LIMB_TYPE.HEAD

    def __str__(self):
        return "head"


class Torso(Limb):

    def get_limb_type(self):
        return LIMB_TYPE.TORSO

    def __str__(self):
        return "leg"


class Eye(RemovableLimb):

    def get_limb_type(self):
        return LIMB_TYPE.EYE

    def __str__(self):
        return "eye"


class Leg(RemovableLimb):

    def get_limb_type(self):
        return LIMB_TYPE.LEG

    def __str__(self):
        return "leg"


class Arm(RemovableLimb):


    def get_limb_type(self):
        return LIMB_TYPE.ARM

    def __str__(self):
        return "arm"
