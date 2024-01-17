import copy
from ai.humanai.relationships.interaction.interactionfighting.fighthelper import *
from ai.humanai.relationships.interaction.interactionfighting.attack.attack import FIGHT_STATE
import global_params
import random
from enum import Enum
from items.itemwearable.itemweapon.itemweaponaxe import ItemWeaponAxe
from items.itemwearable.itemweapon.itemweaponsword import ItemWeaponSword
from items.itemwearable.itemweapon.itemweaponspear import ItemWeaponSpear
from items.itemwearable.itemweapon.itemweaponblunt import ItemWeaponBlunt
from items.itemwearable.itemarmour.itemarmourchest import ItemArmourChest
from items.itemwearable.itemarmour.itemarmourplate import ItemArmourPlate
from items.itemwearable.itemweapon.itemweapon import WEAPON_TYPE
import logging

def simulate_fight(speed1,prot1,dmg1, has_weapon1):
    speed2 = 1
    prot2 = 1
    dmg2 = 1
    has_weapon2 = False

    HITS = 10

    hit_damage_1 = 40 if has_weapon1 else 5
    hit_damage_2 = 40 if has_weapon2 else 5

    amount_hits_p1 = speed1 * HITS
    amount_hits_p2 = speed2 * HITS
    amount_damage_p1 = amount_hits_p2 * dmg2 * prot1 * hit_damage_2
    amount_damage_p2 = amount_hits_p1 * dmg1 * prot2 * hit_damage_1

    return amount_damage_p2 - amount_damage_p1


MAX_POSSIBLE_DAMAGE = simulate_fight(1, 1, 1, True)



def get_fight_constants(genetic_weight, weapon, chest, plate):
    strength = 1 # train on assumed strength 1. This is important because strength may change over time
    damage = 1 # assumed unarmed damage is 5
    speed = 1
    prot = 1

    if weapon is not None:
        damage = weapon.get_damage(genetic_weight)
        speed *= weapon.get_speed(genetic_weight)

    if chest is not None:
        prot *= chest.get_protection(genetic_weight)

    if plate is not None:
        prot *= plate.get_protection(genetic_weight)

    return (speed, damage, prot)


def innovate_one_dimension(need_training, current_best_kit_matrix, group):

    max_weapon_type_combos = (group.knowledge_group_territory_nodes.get_available_weapon_types())
    max_weapon_material_combos = (group.knowledge_group_territory_nodes.get_available_weapon_materials())
    max_plate_combos = (group.knowledge_group_territory_nodes.get_available_plate_materials())
    max_chest_combos = (group.knowledge_group_territory_nodes.get_available_chest_materials())

    # register none types (weapon material below)
    max_weapon_type_combos.add(None)
    max_plate_combos.add(None)
    max_chest_combos.add(None)

    class INNOVATION_TYPE(Enum):
        WEAPON_TYPE = 0
        WEAPON_MATERIAL = 1
        CHEST = 2
        PLATE = 3

    (weapon_type, weapon_material, chest_material, plate_material) = current_best_kit_matrix

    innovation_options = []

    tried_plate_combos = set()
    tried_chest_combos = set()
    tried_weapon_type_combos = set()
    tried_weapon_material_combos = set()


    if (weapon_type, weapon_material, chest_material) in need_training.plate_material_dimension.keys():
        tried_plate_combos = need_training.plate_material_dimension[(weapon_type, weapon_material, chest_material)]

        # if not tried all combos record it as available to innovate
        remaining_available = max_plate_combos - tried_plate_combos
        if remaining_available:
            innovation_options.append(INNOVATION_TYPE.PLATE)
    else:
        # otherwise its a fresh entry therefore we can innovate this item
        innovation_options.append(INNOVATION_TYPE.PLATE)

    if (weapon_type, weapon_material, plate_material) in need_training.chest_material_dimension.keys():
        tried_chest_combos = need_training.chest_material_dimension[(weapon_type, weapon_material, plate_material)]
        # if not tried all combos record it as available to innovate
        remaining_available = max_chest_combos - tried_chest_combos
        if remaining_available:
            innovation_options.append(INNOVATION_TYPE.CHEST)
    else:
        # otherwise its a fresh entry therefore we can innovate this item
        innovation_options.append(INNOVATION_TYPE.CHEST)


    # only consider weapon if we have weapon materials available
    if max_weapon_material_combos:
        if (weapon_material, chest_material, plate_material) in need_training.weapon_type_dimension.keys():
            tried_weapon_type_combos = need_training.weapon_type_dimension[(weapon_material, chest_material, plate_material)]
            # if not tried all combos record it as available to innovate
            remaining_available = max_weapon_type_combos - tried_weapon_type_combos
            # print("weapon type %s" % remaining)
            if remaining_available:
                innovation_options.append(INNOVATION_TYPE.WEAPON_TYPE)
        else:
            # otherwise its a fresh entry therefore we can innovate this item
            innovation_options.append(INNOVATION_TYPE.WEAPON_TYPE)


        if (weapon_type, chest_material, plate_material) in need_training.weapon_material_dimension.keys():
            tried_weapon_material_combos = need_training.weapon_material_dimension[(weapon_type, chest_material, plate_material)]


            # if not tried all combos record it as available to innovate
            remaining_available = max_weapon_material_combos - tried_weapon_material_combos
            # print("weapon material %s" % remaining)
            if remaining_available:
                innovation_options.append(INNOVATION_TYPE.WEAPON_MATERIAL)
        else:
            # otherwise its a fresh entry therefore we can innovate this item
            innovation_options.append(INNOVATION_TYPE.WEAPON_MATERIAL)

    # register weapon material here because we don't want them to take it into account before hand
    tried_weapon_material_combos.add(None)

    # innovated everything: stuck at local maximum
    if not innovation_options:
        # print("local maximum")
        # print(len(need_training.best_kit_combos))
        # for val in sorted([str(thing) for thing in need_training.best_kit_combos.keys()]):
        #     print(val)
        return current_best_kit_matrix

    new_weapon_type = weapon_type
    new_weapon_material = weapon_material
    new_chest_material = chest_material
    new_plate_material = plate_material
    innovation_dimension = random.choice(innovation_options)
    if innovation_dimension == INNOVATION_TYPE.WEAPON_TYPE:
        remaining = max_weapon_type_combos - tried_weapon_type_combos
        new_weapon_type = random.choice(list(remaining))
    elif innovation_dimension == INNOVATION_TYPE.WEAPON_MATERIAL:
        remaining = max_weapon_material_combos - tried_weapon_material_combos
        new_weapon_material = random.choice(list(remaining))
    elif innovation_dimension == INNOVATION_TYPE.CHEST:
        remaining = max_chest_combos - tried_chest_combos
        new_chest_material = random.choice(list(remaining))
    elif innovation_dimension == INNOVATION_TYPE.PLATE:
        remaining = max_plate_combos - tried_plate_combos
        new_plate_material = random.choice(list(remaining))

    """
    Edge case, if person goes from no weapon to weapon, pick him a material too.
    He should always have a material available because theres more material types
    then weapons.
    """
    if new_weapon_type is not None and new_weapon_material is None:
        tried_weapon_material_combos.add(None)
        tried_weapon_material_combos = need_training.weapon_material_dimension[(weapon_type, chest_material, plate_material)]
        remaining = max_weapon_material_combos - tried_weapon_material_combos
        new_weapon_material = random.choice(list(remaining))


    """
    Edge case, if person decides to go handless, make sure we return no
    weapon material.
    """
    if new_weapon_type is None:
        return (None, None, new_chest_material, new_plate_material)
    return (new_weapon_type, new_weapon_material, new_chest_material, new_plate_material)



def calculate_fight_ratio(initator_damage_taken, opponent_damage_taken):
    # print("what (%s, %s)" % (opponent_damage_taken, initator_damage_taken))
    return opponent_damage_taken - initator_damage_taken

