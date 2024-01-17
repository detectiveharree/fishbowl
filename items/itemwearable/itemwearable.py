from abc import ABC, abstractmethod
from items.itemcraftable import ItemCraftable


"""
A item that has a quantity
"""
class ItemWearable(ItemCraftable,ABC):

    def __init__(self, original_owner):
        super().__init__(original_owner)

    """
    Equips this item
    """
    @abstractmethod
    def equip(self, human):
        ...

    """
    Get weight of item
    """
    def weight(self):
         pass

    def __repr__(self):
        return str(self)
