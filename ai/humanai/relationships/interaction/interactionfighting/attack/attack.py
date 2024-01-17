from enum import Enum
from abc import ABC, abstractmethod

class FIGHT_STATE(Enum):
    FEET = 1
    CLINCH = 2
    GROUND = 3


    def __repr__(self):
        return self.name

class ATTACK_TYPES(Enum):
    PUNCH = 1
    KICK = 2
    ELBOW = 3
    KNEE = 4
    WEAPON = 5
    HEADBUTT = 7
    EYE_GOUGE = 8
    CHOKE = 9
    ENTER_GROUND = 10
    ENTER_CLINCH = 11
    ENTER_FEET = 12

    def __repr__(self):
        return self.name

class Attack(ABC):

    """
    DO NOT DELETE THIS. PASTE THIS IN FOR EVERY NEW OBJECT THAT WILL BE STORED IN A SET/DICTIONARY.
    THIS IS ESSENTIAL FOR MAKING SURE THE PROGRAM PERFORMS EXACTLY THE SAME EVERY TIME!

    assert(false) WILL CRASH THE PROGRAM IF YOU ATTEMPT TO PUT THIS OBJECT INTO A SET/DICT WITHOUT FIRST MODIFYING THE FUNCTION.
    THIS IS DONE ON PURPOSE TO PREVENT YOU FROM ACCIDENTALLY LEAKING NON-DETERMINISM INTO THE PROGRAM.
    SPEAK TO ME (TOM) AND I WILL EXPLAIN WHAT TO DO.
    """
    def __hash__(self):
        return hash(self.get_attack_type())

    def __eq__(self, other):
        return self.__class__ == other.__class__ and self.get_attack_type() == other.attack_type

    def __str__(self):
        return str(self.get_attack_type())

    def __repr__(self):
        return str(self)

    """
    Get the type of attack this class does
    """
    @staticmethod
    @abstractmethod
    def get_attack_type():
        ...

    @abstractmethod
    def get_damage(self, attacker, defender, fight_state):
        ...

    @abstractmethod
    def make_attack(self, attacker, defender, mean_damage, fight_state):
        ...

    @abstractmethod
    def acceptable_states(self):
        ...

    """
    You need all of these limbs to perform the attack
    """

    @abstractmethod
    def prerequisites(self, attacker, unarmed):
        ...
