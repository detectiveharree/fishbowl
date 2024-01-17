import guiwindow
from items.itemwearable.itemweapon.itemweapon import ItemWeapon, WEAPON_TYPE
from items.itemwearable.itemarmour.itemarmourchest import ItemArmourChest
from items.itemwearable.itemarmour.itemarmourplate import ItemArmourPlate
import logging
from collections import Counter

class KnowledgeGroupInventoryShelf():

    """
    DO NOT DELETE THIS. PASTE THIS IN FOR EVERY NEW OBJECT THAT WILL BE STORED IN A SET/DICTIONARY.
    THIS IS ESSENTIAL FOR MAKING SURE THE PROGRAM PERFORMS EXACTLY THE SAME EVERY TIME!

    assert(false) WILL CRASH THE PROGRAM IF YOU ATTEMPT TO PUT THIS OBJECT INTO A SET/DICT WITHOUT FIRST MODIFYING THE FUNCTION.
    THIS IS DONE ON PURPOSE TO PREVENT YOU FROM ACCIDENTALLY LEAKING NON-DETERMINISM INTO THE PROGRAM.
    SPEAK TO ME (TOM) AND I WILL EXPLAIN WHAT TO DO.
    """
    def __hash__(self):
        return hash(self.hash_id)

    def __eq__(self, other):
        return self.__class__ == other.__class__ and self.hash_id == other.hash_id

    def __init__(self, group):
        self.group = group
        self.hash_id = guiwindow.WORLD_INSTANCE.knowledge_sleeping_location_house_id_counter
        guiwindow.WORLD_INSTANCE.knowledge_sleeping_location_house_id_counter += 1
        # actual storage of real items for fast retrieval
        self.inventory_weapons = {weapon_type : {material : [] for material in list(ItemWeapon.possible_materials())} for weapon_type in list(WEAPON_TYPE)}
        self.inventory_chest = {material : [] for material in list(ItemArmourChest.possible_materials())}
        self.inventory_plate = {material : [] for material in list(ItemArmourPlate.possible_materials())}
        # fast way of checking what's currently available in the inventory above
        # (sets so we can use fast difference to see what people haven't tried out)
        self.available_weapons = set()
        self.available_chests = set()
        self.available_plates = set()

        # temp storage for freshly made items
        # {human_id : [items]}
        self.item_collection = dict()

    def move_to_collect(self, item, human_id):
        if human_id in self.group.member_ids:
            if human_id in self.item_collection.keys():
                self.item_collection[human_id].append(item)
            else:
                self.item_collection[human_id] = [item]
        else:
            item.add_item_to_shelf(self.group)

    """
    Returns true if the human has items to collect.
    """
    def has_items_to_collect(self, human):
        return human.id_number in self.item_collection.keys()

    """
    Removes and deletes item from someone's collection
    """
    def remove_all_items_from_collection(self, person_id):
        if person_id not in self.item_collection.keys():
            return []
        items = self.item_collection[person_id]
        del self.item_collection[person_id]
        return items


    """
    Merges another shelf into ourself
    """
    def transfer_items(self, other_group):

        # merge weapons
        for (weapon_type, weapon_material_dict) in self.inventory_weapons.items():
            for (weapon_material, storage) in weapon_material_dict.items():
                weapon_matrix = (weapon_type, weapon_material)
                all_other_weapons = ItemWeapon.remove_all_items_from_shelf(weapon_matrix, other_group)
                ItemWeapon.add_all_items_to_shelf(weapon_matrix, self.group, all_other_weapons)

        # merge chests
        for (chest_material, storage) in self.inventory_chest.items():
            all_other_chests = ItemArmourChest.remove_all_items_from_shelf(chest_material, other_group)
            ItemArmourChest.add_all_items_to_shelf(chest_material, self.group, all_other_chests)

        # merge plates
        for (plate_material, storage) in self.inventory_plate.items():
            all_other_plates = ItemArmourPlate.remove_all_items_from_shelf(plate_material, other_group)
            ItemArmourPlate.add_all_items_to_shelf(plate_material, self.group, all_other_plates)

        # finally add all items stuck in collection from other group
        for (person_id, items) in other_group.knowledge_group_item_inventory.item_collection.items():
            for item in items:
                item.add_item_to_shelf(self.group)

        other_group.knowledge_group_item_inventory.item_collection.clear()

    def to_string(self):
        materials = []
        for member in self.group.members:
            materials += member.inventory.get_material_stats()
        mappd = Counter(materials)
        # getting total using sum
        total_val = sum(mappd.values())
        # getting share of each word
        res = {key: round(val / total_val, 2) for key,
               val in mappd.items()}

        out = ""
        out += "Sword: %s\n" % sum([len(self.inventory_weapons[WEAPON_TYPE.SWORD][weapon_material]) for weapon_material in list(ItemWeapon.possible_materials())])
        out += "Spear: %s\n" % sum([len(self.inventory_weapons[WEAPON_TYPE.SPEAR][weapon_material]) for weapon_material in list(ItemWeapon.possible_materials())])
        out += "Axe: %s\n" % sum([len(self.inventory_weapons[WEAPON_TYPE.AXE][weapon_material]) for weapon_material in list(ItemWeapon.possible_materials())])
        out += "Blunt: %s\n" % sum([len(self.inventory_weapons[WEAPON_TYPE.BLUNT][weapon_material]) for weapon_material in list(ItemWeapon.possible_materials())])
        out += "Chest armour: %s\n" % sum([len(self.inventory_chest[chest_material]) for chest_material in list(ItemArmourChest.possible_materials())])
        out += "Plate armour: %s\n" % sum([len(self.inventory_plate[plate_material]) for plate_material in list(ItemArmourPlate.possible_materials())])
        out += "To collect: %s\n" % len(self.item_collection)
        out += "Kit material %% %s" % res
        return out

