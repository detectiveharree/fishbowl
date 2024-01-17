from abc import ABC, abstractmethod
from items.item import Item
from items.itemshelfable import ItemShelfable

class ItemCraftable(Item, ItemShelfable):


    def __init__(self, original_owner):
        super().__init__()
        self.craft_progress_tick = 0
        self.crafted_for_id = original_owner.id_number
        pass

    """
    Return set containing possible materials this item can be crafted from
    """
    @staticmethod
    @abstractmethod
    def possible_materials():
        ...

    """
    Get weight of item
    """
    @abstractmethod
    def weight(self):
         ...

    """
    Returns dictionary containing resources required to build this item.
    """
    @abstractmethod
    def get_craft_resources(self):
        ...

    """
    Returns the amount of points required to craft this item.
    """
    @abstractmethod
    def get_craft_amount(self):
        ...

    def increase_craft_progress(self, amount):
        if self.is_crafting_complete():
            return
        if self.craft_progress_tick + amount >= self.get_craft_amount():
            # building is finished
            self.craft_progress_tick = self.get_craft_amount()
            return
        self.craft_progress_tick += amount

    """
    Return true if building is complete.
    """
    def is_crafting_complete(self):
        return self.craft_progress_tick >= self.get_craft_amount()
