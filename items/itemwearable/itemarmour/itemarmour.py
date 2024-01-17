from abc import ABC, abstractmethod
from items.itemwearable.itemwearable import ItemWearable
import math

"""
A item that has a quantity
"""
class ItemArmour(ItemWearable,ABC):


    # quality is given as a float between 0 and 1 (exclusive of 0), closer to 0 worse, closer to 1 best
    # quality is optional (we can remove)
    def __init__(self, original_owner, material):
        super().__init__(original_owner)
        self.material = material

    """
    Gets lookup matrix for storage cabinet
    """
    def get_lookup_matrix(self):
         return self.material

    """
    Gets protection given defender
    """
    def get_protection(self, genetic_weight):
        prot1 = 1/(1 + abs(self.material.optimal_weight - genetic_weight)) # 0.5 and 1
        prot1 = ((abs(2*(prot1-0.5) - 1))/2) + 0.5 # inverse

        if self.material.tier == 2:
            prot1 *= 1.2
            prot1 = min(1, prot1) # potential to go above 1
        prot1 = math.sqrt(prot1)
        return prot1

    """
    Get weight of item
    """
    def weight(self):
         pass

    def __repr__(self):
        return str(self)
