from ai.need import Need, NEED_TYPE
from items.itemresources.itemresource import ResourceType
from ai.humanai.task.taskinitiateinteraction import TaskInitiateInteraction
from ai.humanai.relationships.interaction.interactionfighting.interactionfighttrain import InteractionFightTrain
from items.itemwearable.itemweapon.itemweapon import WEAPON_TYPE
from gameworld.timestamp import TimeStamp
from items.iteminnovation import innovate_one_dimension, get_fight_constants, simulate_fight, MAX_POSSIBLE_DAMAGE
from sortedcollections import ValueSortedDict
from items.itemwearable.itemweapon.itemweaponaxe import ItemWeaponAxe
from items.itemwearable.itemweapon.itemweaponsword import ItemWeaponSword
from items.itemwearable.itemweapon.itemweaponspear import ItemWeaponSpear
from items.itemwearable.itemweapon.itemweaponblunt import ItemWeaponBlunt
from items.itemwearable.itemweapon.itemweapon import ItemWeapon
from items.itemwearable.itemarmour.itemarmourchest import ItemArmourChest
from items.itemwearable.itemarmour.itemarmourplate import ItemArmourPlate
from ai.humanai.task.taskgetkitfromstockpile import TaskGetKitFromStockpile
from enum import Enum
import random
import logging




FIGHT_LOSS_PERCENT_INNOVATE_TRIGGER = 0.5
FIGHTS_MEMORY_SIZE = 3
ITEM_REQUEST_DEMAND = 50


# when enabled requested items are automatically given to the person rather
# then initiating the group task to do it
DEBUG_MODE = True

class NeedTrain(Need):

    """
    DO NOT DELETE THIS. PASTE THIS IN FOR EVERY NEW OBJECT THAT WILL BE STORED IN A SET/DICTIONARY.
    THIS IS ESSENTIAL FOR MAKING SURE THE PROGRAM PERFORMS EXACTLY THE SAME EVERY TIME!

    assert(false) WILL CRASH THE PROGRAM IF YOU ATTEMPT TO PUT THIS OBJECT INTO A SET/DICT WITHOUT FIRST MODIFYING THE FUNCTION.
    THIS IS DONE ON PURPOSE TO PREVENT YOU FROM ACCIDENTALLY LEAKING NON-DETERMINISM INTO THE PROGRAM.
    SPEAK TO ME (TOM) AND I WILL EXPLAIN WHAT TO DO.
    """
    def __hash__(self):
        assert(False)


    def __init__(self):
        super().__init__(NEED_TYPE.TRAIN) # ALWAYS CALL PARENT CONSTRUCTOR
        self.past_opponents = [] # {interaction_id : TheoreticalFight}

        # {((WEAPON_TYPE, WEAPON_MATERIAL), CHEST_MATERIAL, PLATE_MATERIAL) : score}
        # {None, None, None} = No weapons or armour
        self.best_kit_combos = ValueSortedDict()
        self.weapon_type_dimension = dict() # {(WEAPON_MATERIAL, CHEST_MATERIAL, PLATE_MATERIAL) : set()}
        self.weapon_material_dimension = dict() # {(WEAPON_TYPE, CHEST_MATERIAL, PLATE_MATERIAL) : set()}
        self.plate_material_dimension = dict() # {(WEAPON_TYPE, WEAPON_MATERIAL, CHEST_MATERIAL) : set()}
        self.chest_material_dimension = dict()# {(WEAPON_TYPE, WEAPON_MATERIAL, PLATE_MATERIAL) : set()}
        self.all_tried_weapons = set() # set of all possible weapons that have been tried
        self.all_tried_chests = set() # set of all possible chests that have been tried
        self.all_tried_plates = set() # set of all possible plates that have been tried

        self.current_kit_real_damge_ratio = 0
        self.current_kit_score = 0
        self.current_kit_rating = 0 # rating between 0 and 1, 1 being the max possible score one can get for a kit
        self.last_requested = TimeStamp()
        # the person will work to achieve this
        self.current_optimal_kit_matrix = (None, None, None, None)


    """
    Resets kit change so they are able to request
    new kits again.
    """
    def reset_kit_change_request(self, human):
        self.current_optimal_kit_matrix = self.inventory_to_kit_matrix(human)

    """
    Returns true if person has achieved their current optimal kit
    matrix.
    """
    def has_achieved_optimal_kit_matrix(self, human):
        return self.current_optimal_kit_matrix == self.inventory_to_kit_matrix(human)


    def switch_to_next_best_kit(self, human):

        """
        Don't switch if no change
        """
        if self.has_achieved_optimal_kit_matrix(human):
            return

        current_kit = self.inventory_to_kit_matrix(human)
        current_kit_score = self.best_kit_combos[current_kit]

        logging.info("%s decided to switch from kit %s (%s) to kit: %s (%s)" % (human.id_number, current_kit,
                                                               current_kit_score, str(self.current_optimal_kit_matrix),
                                                               self.best_kit_combos[self.current_optimal_kit_matrix]))


        """
        Equip or request items 
        """
        (weapon_type, weapon_material, chest_material, plate_material) = self.current_optimal_kit_matrix
        self.current_kit_score = self.best_kit_combos[self.current_optimal_kit_matrix]
        self.current_kit_rating = self.current_kit_score / MAX_POSSIBLE_DAMAGE
        (current_weapon_type, current_weapon_material, current_chest_material, current_plate_material) = self.inventory_to_kit_matrix(human)

        # if we don't already have that weapon
        if (weapon_type, weapon_material) != (current_weapon_type, current_weapon_material):

            # if weapon to switch to is none, change to nothing
            if weapon_type is None and weapon_material is None:
                human.inventory.change_weapon(human, None)
            else:
                # else search group inventories for weapon
                existing_weapon = ItemWeapon.remove_item_from_shelf((weapon_type, weapon_material), human.group)
                if existing_weapon is not None:
                    # mark it as to be collected for the human
                    human.group.knowledge_group_item_inventory.move_to_collect(existing_weapon, human.id_number)
                # if group doesn't already have it, then request its built
                else:
                    weapon_to_be_requested = None
                    if weapon_type == WEAPON_TYPE.AXE:
                        weapon_to_be_requested = (ItemWeaponAxe(human, weapon_material))
                    elif weapon_type == WEAPON_TYPE.BLUNT:
                        weapon_to_be_requested = (ItemWeaponBlunt(human,  weapon_material))
                    elif weapon_type == WEAPON_TYPE.SPEAR:
                        weapon_to_be_requested = (ItemWeaponSpear(human,  weapon_material))
                    elif weapon_type == WEAPON_TYPE.SWORD:
                        weapon_to_be_requested = (ItemWeaponSword(human,  weapon_material))

                    if DEBUG_MODE:
                        human.inventory.change_weapon(human, weapon_to_be_requested)
                    else:
                        human.group.need_request_item.request_item_crafted(weapon_to_be_requested, ITEM_REQUEST_DEMAND)

        if chest_material != current_chest_material:
            # if chest to switch to is none, change to nothing
            if chest_material is None:
                human.inventory.change_chest(human, None)
            else:
                # else search group inventories for chest
                existing_chest = ItemArmourChest.remove_item_from_shelf(chest_material, human.group)

                if existing_chest is not None:
                    # mark it as to be collected for the human
                    human.group.knowledge_group_item_inventory.move_to_collect(existing_chest, human.id_number)
                # if group doesn't already have it, then request its built
                else:
                    chest_to_be_requested = ItemArmourChest(human, chest_material)
                    if DEBUG_MODE:
                        human.inventory.change_chest(human, chest_to_be_requested)
                    else :
                        human.group.need_request_item.request_item_crafted(chest_to_be_requested, ITEM_REQUEST_DEMAND)


        if plate_material != current_plate_material:
            # if plate to switch to is none, change to nothing
            if plate_material is None:
                human.inventory.change_plate(human, None)
            else:
                # else search group inventories for plate
                existing_plate = ItemArmourPlate.remove_item_from_shelf(plate_material, human.group)
                if existing_plate is not None:
                    # mark it as to be collected for the human
                    human.group.knowledge_group_item_inventory.move_to_collect(existing_plate, human.id_number)
                # if group doesn't already have it, then request its built
                else:
                    plate_to_be_requested = ItemArmourPlate(human, plate_material)
                    if DEBUG_MODE:
                        human.inventory.change_plate(human, plate_to_be_requested)
                    else:
                        human.group.need_request_item.request_item_crafted(plate_to_be_requested, ITEM_REQUEST_DEMAND)




    """
    Should really consider outsourcing damage, protection and speed functions such that
    we don't have to construct the items every time in order to use get these values.
    """
    def kit_matrix_to_inventory(self, kit_matrix, human):
        (weapon_type, weapon_material, chest_material, plate_material) = kit_matrix

        weapon = None
        chest = None
        plate = None

        if not (weapon_type is None and weapon_material is None):
            if weapon_type == WEAPON_TYPE.AXE:
                weapon = ItemWeaponAxe(human, weapon_material)
            elif weapon_type == WEAPON_TYPE.BLUNT:
                weapon = ItemWeaponBlunt(human,  weapon_material)
            elif weapon_type == WEAPON_TYPE.SPEAR:
                weapon = ItemWeaponSpear(human,  weapon_material)
            elif weapon_type == WEAPON_TYPE.SWORD:
                weapon = ItemWeaponSword(human,  weapon_material)

        if chest_material is not None:
            chest = ItemArmourChest(human, chest_material)

        if plate_material is not None:
            plate = ItemArmourPlate(human, plate_material)

        return (weapon, chest, plate)


    def inventory_to_kit_matrix(self, human):
        current_weapon = human.inventory.weapon_slot.get_item()
        current_chest = human.inventory.armour_chest_slot.get_item()
        current_plate = human.inventory.armour_plate_slot.get_item()

        weapon_type, weapon_material, chest_material, plate_material = None, None, None, None
        if current_weapon is not None:
            weapon_type = current_weapon.get_weapon_type()
            weapon_material = current_weapon.material_resource

        if current_chest is not None:
            chest_material = current_chest.material

        if current_plate is not None:
            plate_material = current_plate.material

        return (weapon_type, weapon_material, chest_material, plate_material)


    """
    Registers a performance of a weapon given its type and material
    """
    def register_kit_performance(self, kit_matrix, weapon_performance_score):


        """
        Edge case, we shouldn't have a reason to pick all None matrixes ever again
        """
        if kit_matrix == (None, None, None, None):
            weapon_performance_score = -100


        (weapon_type, weapon_material, chest_material, plate_material) = kit_matrix

        # register individual components as tried
        self.all_tried_weapons.add((weapon_type, weapon_material))
        self.all_tried_chests.add(chest_material)
        self.all_tried_plates.add(plate_material)

        # weapon material should never by non non if weapon type is
        assert(not (weapon_material is None and weapon_type is not None))

        plate_dimensions = (weapon_type, weapon_material, chest_material) # plate
        chest_dimensions = (weapon_type, weapon_material, plate_material) # chest
        weapon_type_dimensions = (weapon_material, chest_material, plate_material) # weapon type
        weapon_material_dimensions = (weapon_type, chest_material, plate_material) # weapon material
        self.best_kit_combos[(weapon_type, weapon_material, chest_material, plate_material)] = weapon_performance_score
        self.current_optimal_kit_matrix, score = self.best_kit_combos.items()[-1]

        # plate registry
        if plate_dimensions in self.plate_material_dimension.keys():
            self.plate_material_dimension[plate_dimensions].add(plate_material)
        else:
            self.plate_material_dimension[plate_dimensions] = {plate_material}

        # chest registry
        if chest_dimensions in self.chest_material_dimension.keys():
            self.chest_material_dimension[chest_dimensions].add(chest_material)
        else:
            self.chest_material_dimension[chest_dimensions] = {chest_material}

        """
        If weapon type is None, we register none for all other similar weapon types.        
        """
        if weapon_type is None:
            for material2 in (ItemWeapon.possible_materials().union({None})):
                new_type_with_none = (material2, chest_material, plate_material)
                if new_type_with_none in self.weapon_type_dimension.keys():
                    self.weapon_type_dimension[new_type_with_none].add(weapon_type)
                else:
                    self.weapon_type_dimension[new_type_with_none] = {weapon_type}

            for type2 in (list(WEAPON_TYPE) + [None]):
                new_mat_with_none = (type2, chest_material, plate_material)
                if new_mat_with_none in self.weapon_material_dimension.keys():
                    self.weapon_material_dimension[new_mat_with_none].add(None)
                else:
                    self.weapon_material_dimension[new_mat_with_none] = {None}
            return

        # weapon type registry
        if weapon_type_dimensions in self.weapon_type_dimension.keys():
            self.weapon_type_dimension[weapon_type_dimensions].add(weapon_type)

        else:
            self.weapon_type_dimension[weapon_type_dimensions] = {weapon_type}

        # weapon material registry
        if weapon_material_dimensions in self.weapon_material_dimension.keys():
            self.weapon_material_dimension[weapon_material_dimensions].add(weapon_material)
        else:
            self.weapon_material_dimension[weapon_material_dimensions] = {weapon_material}

        # register kit


    """
    Converts a informationinteraction fight object into a theoretical fight object
    """
    def register_theoretical_fight(self, human, informationinteraction):
        if len(self.past_opponents) == FIGHTS_MEMORY_SIZE:
            self.past_opponents.pop(0)
        self.past_opponents.append(informationinteraction.get_fight_score(human.id_number))
        self.current_kit_real_damge_ratio = sum(self.past_opponents) / len(self.past_opponents)

    """
    Note this method will not change the humans weapon,
    just used to reset performance recordings
    """
    def kit_changed(self):
        self.past_opponents.clear()
        self.current_kit_real_damge_ratio = 0

    """
    Returns false if the person has underperformed by some threshold in n
    most recent fights.
    """
    def can_request_new_kit_part(self, human):
        return (self.has_achieved_optimal_kit_matrix(human)) and\
               (len(self.past_opponents) >= FIGHTS_MEMORY_SIZE) and\
               (self.current_kit_real_damge_ratio < 0)

    # ((TimeStamp().convert_to_hours() - self.last_requested.convert_to_hours()) > 1) and\



    def train_kit(self, human, kit):

        (weapon, chest, plate) = self.kit_matrix_to_inventory(kit, human)

        (theor_speed, theor_damage, theor_prot) = get_fight_constants(human.body.genetic_weight, weapon, chest, plate)

        score = simulate_fight(theor_speed, theor_prot, theor_damage,  weapon is not None)

        self.register_kit_performance(kit, score)

        return score

    """
    Updates current best matrix to include a random
    untried item from the groups inventory.
    If tried all items in group inventory, return None
    """
    def try_random_group_item(self, human, best_kit_matrix):

        (weapon_type, weapon_material, chest_material, plate_material) = best_kit_matrix

        # work out all unique equipment items not tried yet
        available_weapons = human.group.knowledge_group_item_inventory.available_weapons - self.all_tried_weapons
        available_chests = human.group.knowledge_group_item_inventory.available_chests - self.all_tried_chests
        available_plates = human.group.knowledge_group_item_inventory.available_plates - self.all_tried_plates

        # tried everything in group stockpile, move on
        if not available_weapons and not available_chests and not available_plates:
            return None

        class DECISION_TYPE(Enum):
            WEAPON = 0
            CHEST = 1
            PLATE = 2
        choices = []

        # register equipment type as a valid decision if not yet
        if available_weapons:
            choices.append(DECISION_TYPE.WEAPON)
        if available_chests:
            choices.append(DECISION_TYPE.CHEST)
        if available_plates:
            choices.append(DECISION_TYPE.PLATE)

        decision = random.choices(choices)
        # return updated kit matrix to reflect new equipment
        if decision == DECISION_TYPE.WEAPON:
            (weapon_type_to_try, weapon_material_to_try) = random.choices(available_weapons)
            return (weapon_type_to_try, weapon_material_to_try, chest_material, plate_material)
        elif decision == DECISION_TYPE.CHEST:
            chest_to_try = random.choices(available_chests)
            return (weapon_type, weapon_material, chest_to_try, plate_material)
        elif decision == DECISION_TYPE.PLATE:
            plate_to_try = random.choices(available_plates)
            return (weapon_type, weapon_material, chest_material, plate_to_try)



    def reinvent_kit(self, human):

        best_kit_matrix = self.best_kit_combos.items()[-1][0]

        # first try update best kit with random item from inventory that has not been tried yet
        innovated_kit_matrix = self.try_random_group_item(human, best_kit_matrix)

        # if tried all individual items in group inventory, innovate
        if innovated_kit_matrix is None:
            innovated_kit_matrix = innovate_one_dimension(self, best_kit_matrix, human.group)

        self.train_kit(human, innovated_kit_matrix)
        self.switch_to_next_best_kit(human)



    """
    Each person will tick 
    """
    def tick(self, human):
        self.need_level = 0


    def minimum_level_for_switch(self):
        return 30


    """
    Called when this need is the highest out of all of needs 
    """
    def get_task(self, human):
        if human.group.knowledge_group_item_inventory.has_items_to_collect(human):
            return TaskGetKitFromStockpile(NEED_TYPE.TRAIN)

        if self.can_request_new_kit_part(human):
            self.last_requested = TimeStamp()
            current_kit = self.inventory_to_kit_matrix(human)
            current_kit_score = self.train_kit(human, current_kit)

            best_kit, best_score = self.best_kit_combos.items()[-1]
            if best_score > current_kit_score:
                self.switch_to_next_best_kit(human)
            else:
                self.reinvent_kit(human)
        if human.body.health.get() >= 100:
            return TaskInitiateInteraction(InteractionFightTrain(human, 80), human)


    def __str__(self):
        return "Train : %s" % self.need_level
