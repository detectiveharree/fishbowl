from items.itemwearable.itemarmour.itemarmour import ItemArmour
from items.itemresources.itemresource import ResourceType


class ItemArmourChest(ItemArmour):
    # quality is given as a float between 0 and 1 (exclusive of 0), closer to 0 worse, closer to 1 best
    # quality is optional (we can remove)
    def __init__(self, original_owner, material):
        super().__init__(original_owner, material)

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
                ResourceType.BRONZE}

    """
    Equips this item
    """
    def equip(self, human):
        human.inventory.change_chest(human, self)

    """
    Returns dictionary containing resources required to build this item.
    """
    def get_craft_resources(self):
        return {self.material : 600}

    """
    Returns the amount of points required to craft this item.
    """
    def get_craft_amount(self):
        return 800

    """
    Returns correct storage shelf
    """
    @staticmethod
    def lookup_storage(chest_material, group):
        return group.knowledge_group_item_inventory.inventory_chest[chest_material]

    """
    Returns availability storage container
    """
    @staticmethod
    def get_availability_storage(group):
         return group.knowledge_group_item_inventory.available_chests



    def __str__(self):
        return f'{self.material} chest armour'