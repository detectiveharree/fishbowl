from abc import ABC, abstractmethod

from enum import Enum

class INVENTORY_SLOT_TYPE(Enum):

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

    ARMOUR_PLATE_SLOT = 1
    ARMOUR_CHEST_SLOT = 2
    ARMOUR_WEAPON_SLOT = 3

    def __repr__(self):
        return self.name

class InventorySlot(ABC):

    def __init__(self, item=None):
        self.item = item

    def is_empty(self):
        return self.item is None

    def get_item(self):
        return self.item

    """
    If human arg is specified, 
    will deposit previous item in human's group shelf, 
    """
    def set_item(self, item, human = None):
        if human is not None:
            if self.item is not None:
                self.item.add_item_to_shelf(human.group)
        self.item = item

    def __repr__(self):
        return "slot: " + str(self.item)


