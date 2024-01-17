from enum import Enum
from abc import ABC, abstractmethod

class BATTLE_RESULT(Enum):
    WON = 1 # proceed with battle
    LOST = 2 # surrender become subjagated

    def __repr__(self):
        return self.name

"""
When a person enters a interaction, they are each assigned
their own InteractionParticipant object.
Its used for optimisations mainly.
"""
class InteractionGroupParticipant(ABC):

    """
    DO NOT DELETE THIS. PASTE THIS IN FOR EVERY NEW OBJECT THAT WILL BE STORED IN A SET/DICTIONARY.
    THIS IS ESSENTIAL FOR MAKING SURE THE PROGRAM PERFORMS EXACTLY THE SAME EVERY TIME!

    assert(false) WILL CRASH THE PROGRAM IF YOU ATTEMPT TO PUT THIS OBJECT INTO A SET/DICT WITHOUT FIRST MODIFYING THE FUNCTION.
    THIS IS DONE ON PURPOSE TO PREVENT YOU FROM ACCIDENTALLY LEAKING NON-DETERMINISM INTO THE PROGRAM.
    SPEAK TO ME (TOM) AND I WILL EXPLAIN WHAT TO DO.
    """
    def __hash__(self):
        assert(False)

    def __init__(self, army):
        self.group = army.caravan_group
        self.other_group = None
        self.starting_position_location = None
        self.at_battle_starting_position = False # true when they arrive on their side of battlefield
        self.battle_outcome = None
        self.army = army
        self.active_soldiers = set()

    def soldier_join_battle(self, human):
        self.active_soldiers.add(human.id_number)

    def soldier_leave_battle(self, human):
        self.active_soldiers.remove(human.id_number)


    """
    Return true if participant wants to surrender
    """
    def should_surrender(self):
        return self.army.should_surrender(self)


