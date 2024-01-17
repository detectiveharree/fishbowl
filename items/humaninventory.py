from items.inventoryslot import InventorySlot
from items.inventoryweightedslot import InventoryWeightedSlot
from ai.need import NEED_TYPE

class HumanInventory():


    def __init__(self):

        # weapon
        self.weapon_slot = InventorySlot()


        # light armour slots
        self.armour_chest_slot = InventorySlot()
        self.armour_plate_slot = InventorySlot()

        # clothing layers
        self.clothing_chest_slot = InventorySlot()
        self.clothing_leg_slot = InventorySlot()

        # accessories
        self.crown = InventorySlot()
        self.footwear = InventorySlot()
        self.cloak = InventorySlot()
        self.pelt = InventorySlot()



        # how much can human's store in their inventory
        self.weighted_slot = InventoryWeightedSlot(500)



    def change_weapon(self, human, new_weapon):
        human.needs[NEED_TYPE.TRAIN].kit_changed()
        self.weapon_slot.set_item(new_weapon, human)

    def change_chest(self, human, new_chest):
        human.needs[NEED_TYPE.TRAIN].kit_changed()
        self.armour_chest_slot.set_item(new_chest, human)

    def change_plate(self, human, new_chest):
        human.needs[NEED_TYPE.TRAIN].kit_changed()
        self.armour_plate_slot.set_item(new_chest, human)

    def get_material_stats(self):
        armour_chest = self.armour_chest_slot.get_item()
        armour_plate = self.armour_plate_slot.get_item()
        weapon = self.weapon_slot.get_item()
        materials = []
        if armour_chest is not None:
            materials.append(armour_chest.material)
        if armour_plate is not None:
            materials.append(armour_plate.material)
        if weapon is not None:
            materials.append(weapon.material_resource)
        return materials


    def to_string(self):
        out = "%s | %s | %s" % (self.weapon_slot, self.armour_chest_slot, self.armour_plate_slot)
        return out


