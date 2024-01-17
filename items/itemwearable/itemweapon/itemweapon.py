from abc import ABC, abstractmethod
from items.itemcraftable import ItemCraftable
from items.itemresources.itemresource import ResourceType
from enum import Enum
from items.itemwearable.itemwearable import ItemWearable
import numpy as np

class WEAPON_TYPE(Enum):

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

    AXE = 1
    BLUNT = 2
    SPEAR = 3
    SWORD = 4

    def __str__(self):
        return self.name

    def __repr__(self):
        return str(self)


"""
A item that has a quantity
"""
class ItemWeapon(ItemWearable, ABC):

    def __init__(self, original_owner, material_resource):
        super().__init__(original_owner)
        self.length = original_owner.body.height * self.get_ideal_height_factor() # made with ideal height
        self.material_resource = material_resource
    """
    Return set containing possible materials this item can be crafted from
    """
    @staticmethod
    def possible_materials():
        return {ResourceType.BLACK_STEEL,
                  ResourceType.IRON,
                  ResourceType.DARK_IRON,
                  ResourceType.WHITE_STEEL,
                  ResourceType.BRASS,
                  ResourceType.BRONZE,
                  #ResourceType.WOOD
                }

    """
    Gets lookup matrix for storage cabinet
    """
    def get_lookup_matrix(self):
         return (self.get_weapon_type(), self.material_resource)

    """
    Equips this item
    """
    def equip(self, human):
        human.inventory.change_weapon(human, self)


    """
    Returns optimal human weight
    """
    @abstractmethod
    def get_optimal_weight(self):
        ...

    """
    Returns ideal height to weapon length factor between 0 and 1
    """
    @abstractmethod
    def get_ideal_height_factor(self):
        ...

    """
    Returns a tuple of minimum and maximium inches weapon allowed to be
    """
    @abstractmethod
    def get_allowed_weapon_length_range(self):
        ...

    """
    Returns a list of tuples mapping a possible limb to a percent change of dismemberment
    Percent change should be between 0-1
    """
    @abstractmethod
    def get_limb_dismemberment_chance(self):
        ...


    """
    Returns adjusted speed of weapon given person
    """
    def get_speed(self, genetic_weight):
        speed = np.interp(1/(1 + abs(self.get_optimal_weight() - genetic_weight)), [0.5,1], [0,1]) # weapon type | effects speed based on optimal weight
        if self.material_resource.tier == 2:
            speed *= 0.8
        return speed

    """
    Returns adjusted damage of weapon given person
    """
    def get_damage(self, genetic_weight):
        damage = 1/(1 + abs(self.material_resource.optimal_weight - genetic_weight)) # weapon material | effects damage based on optimal weight
        if self.material_resource.tier == 2:
            damage *= 0.8
        return damage

    """
    Returns weapon type
    """
    @abstractmethod
    def get_weapon_type(self):
        ...

    """
    Returns correct storage shelf
    """
    @staticmethod
    def lookup_storage(weapon_matrix, group):
         (weapon_type, weapon_material) = weapon_matrix
         return group.knowledge_group_item_inventory.inventory_weapons[weapon_type][weapon_material]

    """
    Returns availability storage container
    """
    @staticmethod
    def get_availability_storage(group):
         return group.knowledge_group_item_inventory.available_plates

    """
    Get weight of item
    """
    def weight(self):
         pass

    def __str__(self):
        return "(%s) %s %s of length %s" % (self.id_number, self.material_resource, self.get_weapon_type(), self.length)

    def __repr__(self):
        return str(self)



