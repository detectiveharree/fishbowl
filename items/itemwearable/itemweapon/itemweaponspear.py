from items.itemwearable.itemweapon.itemweapon import ItemWeapon, WEAPON_TYPE
from items.itemresources.itemresource import ResourceType
from ai.humanai.relationships.attributes.body.limb import LIMB_TYPE

class ItemWeaponSpear(ItemWeapon):


    def __init__(self, original_owner, material_resource):
        super().__init__(original_owner, material_resource)

    """
    Returns optimal human weight
    """
    def get_optimal_weight(self):
        return 0.125

    """
    Returns ideal height to weapon length factor between 0 and 1
    """
    def get_ideal_height_factor(self):
        return 1

    """
    Returns a tuple of minimum and maximium inches weapon allowed to be
    """
    def get_allowed_weapon_length_range(self):
        return (50, 90)

    """
    Returns a list of tuples mapping a possible limb to a percent change of dismemberment
    Percent change should be between 0-1
    """
    def get_limb_dismemberment_chance(self):
        return [(LIMB_TYPE.EYE, 0.01)]

    """
    Returns dictionary containing resources required to build this item.
    """
    def get_craft_resources(self):
        return {ResourceType.WOOD : 500, self.material_resource : 600}

    """
    Returns the amount of points required to craft this item.
    """
    def get_craft_amount(self):
        return 800

    """
    Returns weapon type
    """
    def get_weapon_type(self):
        return WEAPON_TYPE.SPEAR
