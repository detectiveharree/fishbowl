import guiwindow
from entities.groupbase import GroupType
from ai.humanai.relationships.information.informationlocationcell import InformationLocationCell
from functools import lru_cache
from ai import pathfinding
from gameworld.territorynode import TerritoryNode,MAX_POSSIBLE_CORRIDOR_SIZE
from copy import deepcopy
from gameworld.cell.cell import CELL_CATEGORY
from gameworld.cell.cellbuilding.cellbuilding import BUILDING_TYPE
from gameworld.cell.cellresource.cellresource import RESOURCE_CELL_TYPE
import logging
from items.itemwearable.itemweapon.itemweapon import WEAPON_TYPE
from items.itemwearable.itemweapon.itemweapon import ItemWeapon
from items.itemwearable.itemarmour.itemarmourchest import ItemArmourChest
from items.itemwearable.itemarmour.itemarmourplate import ItemArmourPlate

class KnowledgeGroupTerritoryNodes():


    def __init__(self, group):
        self.group = group
        self.all_territory_coords = set()

        # territory node locations to territory nodes (helper for below territory node containers)
        self.all_territory_nodes = dict()

        # contains territory nodes that don't contain an active cell (building/resource).
        # Only possible if a cell is depleted
        self.territory_nodes_empty = set()
        # contains territory nodes that contain an active cell (building/resource)
        self.territory_nodes_cells = {CELL_CATEGORY.BUILDING : {building_type: set() for building_type in list(BUILDING_TYPE)},
                          CELL_CATEGORY.RESOURCE : {resource_cell_type: set() for resource_cell_type in list(RESOURCE_CELL_TYPE)}}

        self.stockpile_buffer_coords = set()
        self.stockpile_territory_buffer = 3

        pass



    def get_available_weapon_types(self):
        return {WEAPON_TYPE.AXE,
                  WEAPON_TYPE.SPEAR,
                  WEAPON_TYPE.SWORD,
                  WEAPON_TYPE.BLUNT}

    def get_available_weapon_materials(self):
        return {resource_ore_type.harvestable_type for resource_ore_type, amount in self.territory_nodes_cells[CELL_CATEGORY.RESOURCE].items()
                if self.territory_nodes_cells[CELL_CATEGORY.RESOURCE][resource_ore_type] and resource_ore_type.harvestable_type in ItemWeapon.possible_materials()}

    def get_available_chest_materials(self):
        return {resource_ore_type.harvestable_type for resource_ore_type, amount in self.territory_nodes_cells[CELL_CATEGORY.RESOURCE].items()
                if self.territory_nodes_cells[CELL_CATEGORY.RESOURCE][resource_ore_type] and resource_ore_type.harvestable_type in ItemArmourChest.possible_materials()}

    def get_available_plate_materials(self):
        return {resource_ore_type.harvestable_type for resource_ore_type, amount in self.territory_nodes_cells[CELL_CATEGORY.RESOURCE].items()
                if self.territory_nodes_cells[CELL_CATEGORY.RESOURCE][resource_ore_type] and resource_ore_type.harvestable_type in ItemArmourPlate.possible_materials()}


    """
    Should call when we see that a cell is empty and we believe it may have been a previous territory node.
    Will downgrade the node so that it represents a cell not 
    """
    def attempt_down_grade_territory_node(self, territory_node):
        #  the order of these steps are very deliberate
        # because the territory cells are hashed on their cellbase value

        # could be case territory node not in all territory nodes
        # because it belonged to someone else
        if territory_node in self.all_territory_nodes:
            correct_node = self.all_territory_nodes[territory_node]
            del self.all_territory_nodes[territory_node]

            old_cell_base = correct_node.cellbase
            self.territory_nodes_cells[old_cell_base.cell_category][old_cell_base.cell_type].remove(correct_node)
            correct_node.cellbase = None
            self.territory_nodes_empty.add(correct_node)
            self.all_territory_nodes[correct_node] = correct_node
    """
    Finds existing node and marks it as now being visited
    """
    def mark_node_visited(self, territory_node):
        # reason for this check is that a water node will not necessarily be recorded
        # because it cannot be picked up by the corridor path back
        # logging.info(self.all_territory_nodes)
        if territory_node in self.all_territory_nodes.keys():
            self.all_territory_nodes[territory_node].set_visited()

    def _add_node(self, territory_node):
        cellbase = territory_node.cellbase
        # print("registered %s" % cellbase)
        if cellbase is not None:
            self.territory_nodes_cells[cellbase.cell_category][cellbase.cell_type].add(territory_node)
            if cellbase.cell_type == BUILDING_TYPE.HOUSE:
                self.group.knowledge_sleeping_location_house.register_house(self.group, list(cellbase.locations)[0])
        else:
            self.territory_nodes_empty.add(territory_node)
        # cache its location
        self.all_territory_nodes[territory_node] = territory_node


    def _remove_node(self, territory_node):
        cellbase = territory_node.cellbase
        if cellbase is not None:
            self.territory_nodes_cells[cellbase.cell_category][cellbase.cell_type].remove(territory_node)

            if cellbase.cell_type == BUILDING_TYPE.HOUSE:
                self.group.knowledge_sleeping_location_house.remove_house(list(cellbase.locations)[0])
        else:
            self.territory_nodes_empty.remove(territory_node)
        del self.all_territory_nodes[territory_node]

    """
    Should call when attempting to gain new territory
    Will return true if successful
    """
    def attempt_register_territory_node(self, territory_node):
        # only settlements can grab territory

        if self.group.group_type == GroupType.SETTLEMENT:
            # if we have a equivalent territory node of same locations don't record again
            if territory_node in self.all_territory_nodes.keys():
                return False
            # check to make sure each location in the node won't violate another persons territory
            if not self.can_claim_territory(territory_node, guiwindow.WORLD_INSTANCE.territory_change_counter):
                return False

            # logging.info("Claimed: %s (%s)" % (str(territory_node.location), self.id_number))

            # if territory exists change it
            self._add_node(territory_node)
            territory_node.update_route_back(self.group)
            for coord in territory_node.all_territory_pixels:
                self.take_territory_pixel(coord)
            return True
        return False

    def take_territory_pixel(self, coord):
        self.all_territory_coords.add(coord)
        guiwindow.WORLD_INSTANCE.set_territory(coord, self.group)
        cell = (guiwindow.WORLD_INSTANCE.world[coord[0]][coord[1]])
        # register cells
        # but don't take them as territory nodes immediately (aka None for human location)
        # else theres the risk it could cause a domino effect overtime
        if cell.cell_type is not None:
            cell_base = cell.cell_type.to_cell_base(None)
            InformationLocationCell(cell_base.locations, cell_base).register_to_knowledge(self.group)
        else:
            InformationLocationCell({coord}, None).register_to_knowledge(self.group)

    def lose_all_territory(self):
        # surrender all territory
        # logging.info("removed %s territory %s" % (len(self.all_territory_coords), self.all_territory_coords))
        for loc in self.all_territory_coords:
            guiwindow.WORLD_INSTANCE.set_territory(loc, None)

        self.all_territory_coords = set()

        # territory node locations to territory nodes (helper for below territory node containers)
        self.all_territory_nodes = dict()

        # contains territory nodes that don't contain an active cell (building/resource).
        # Only possible if a cell is depleted
        self.territory_nodes_empty = set()
        # contains territory nodes that contain an active cell (building/resource)
        self.territory_nodes_cells = {CELL_CATEGORY.BUILDING : {building_type: set() for building_type in list(BUILDING_TYPE)},
                          CELL_CATEGORY.RESOURCE : {resource_cell_type: set() for resource_cell_type in list(RESOURCE_CELL_TYPE)}}

        self.stockpile_buffer_coords = set()



    """
    territory counter is a cache parameter     
    """
    @lru_cache(maxsize=1000)
    def can_claim_territory(self, territory_node, territory_counter):


        # print("node %s from group %s" % (territory_node.location, self.id_number))

        for location in territory_node.locations:
            other_group_claim = guiwindow.WORLD_INSTANCE.world[location[0]][location[1]].territory

            # can't be claimed already
            if not (other_group_claim is None or other_group_claim == self.group.id_number):
                return False

        territory_node.update_route_back(self.group)

        # must have a route back
        return len(territory_node.last_route_to_stockpile) != 0



    def daily_update_territories(self):

        """
        Lose all territory if not own stockpile land
        """
        if not self.group.acceptable_stockpile_location(self.group.stockpile_location):
            self.lose_all_territory()


        new_territory = set()
        for node in self.all_territory_nodes.values():
            new_territory.update(node.daily_update(self.group))

        for position in new_territory:
            self.take_territory_pixel(position)

    """
    UPDATE THIS
    
    """
    def update_stockpile_territory(self):

        class LossStats():

            def __init__(self, group_id, territory_nodes, all_territory_coords):
                self.group_id = group_id
                self.amount_original_territory_coords = len(all_territory_coords)
                self.amount_original_territory_nodes = len(territory_nodes)
                self.amount_new_territory_coords = 0
                self.lost_territory_nodes = set()
                self.loss_stockpile = False

            def __repr__(self):
                out = "Group %s\n" % self.group_id
                out += "Territory nodes loss: %s%%\n" % round(((len(self.lost_territory_nodes) / self.amount_original_territory_nodes) * 100))
                out += "    %s/%s\n" % (self.amount_original_territory_nodes - len(self.lost_territory_nodes), self.amount_original_territory_nodes)
                out += "Territory pixels loss: %s%%\n" % round(100 - ((self.amount_new_territory_coords / self.amount_original_territory_coords) * 100))
                out += "    %s/%s\n" % (self.amount_original_territory_coords - self.amount_new_territory_coords, self.amount_original_territory_coords)
                out += "Loss stockpile: %s" % self.loss_stockpile
                return out

        stats = LossStats(self.group.id_number, self.all_territory_nodes.values(), self.all_territory_coords)


        if self.group.group_type == GroupType.SETTLEMENT:

            node_requires_updates = set()

            for territory_node in self.all_territory_nodes.values():
                # if territory node is still connected - do nothing
                if not territory_node.connected_to_stockpile(self.group) or territory_node.must_update:
                    node_requires_updates.add(territory_node)
                    territory_node.must_update = False

            # logging.info("Updating stockpile for %s (%s)" % (self.group.id_number, self.all_territory_coords))

            # temporarily unmap all territory
            # ONLY unmap if not belong to us on group level.
            # other group may have taken over our territory
            for coord in self.all_territory_coords:
                if guiwindow.WORLD_INSTANCE.world[coord[0]][coord[1]].territory != self.group.id_number:
                    continue
                guiwindow.WORLD_INSTANCE.set_territory(coord, None)

            self.all_territory_coords.clear()

            # first get coords of stockpile location
            #self.stockpile_buffer_coords = {self.stockpile_location} #pathfinding.flood_fill_radius(self.stockpile_location, self.current_expansion_level + self.stockpile_territory_buffer)
            self.stockpile_buffer_coords = pathfinding.flood_fill_radius(self.group.stockpile_location, self.group.current_expansion_level + self.stockpile_territory_buffer)
            # """
            # Edge case. If stockpile location on land that doesn't belong to you surrender it all.
            # Note. Might have to be extended to entire stockpile + sleeper buffer
            # """
            # if not self.group.can_place_stockpile(self.group.stockpile_location):
            #     print("FUCKKKK!!!")
            #     print(self.group.id_number)
            #     # self.lose_all_territory()
            #     # stats.lost_territory_nodes = self.territory_nodes
            #     # stats.amount_new_territory_coords = len(self.all_territory_coords)
            #     # return stats
            # else:
            #     print("KYS")

            # register stockpile coords before next bit
            for coord in self.stockpile_buffer_coords:
                if not (guiwindow.WORLD_INSTANCE.world[coord[0]][coord[1]].territory == self.group.id_number or guiwindow.WORLD_INSTANCE.world[coord[0]][coord[1]].territory is None):
                    stats.loss_stockpile = True
                    continue
                self.take_territory_pixel(coord)



            # no need to update these ones as they still have a connection to stockpile somehow
            for node in (set(self.all_territory_nodes.values()) - node_requires_updates):
                for coord in node.all_territory_pixels:
                    self.take_territory_pixel(coord)



            bad_nodes = set()
            # map special points to territories
            for territory_node in node_requires_updates:
                territory_node.update_route_back(self.group)
                # if path cannot be made, save this coordiante as we will remove it next
                if len(territory_node.last_route_to_stockpile) == 0:
                    bad_nodes.add(territory_node)
                    continue

                for coord in territory_node.all_territory_pixels:
                    self.take_territory_pixel(coord)


            # remove nodes where we can't pathfind to
            for node in bad_nodes:
                self._remove_node(node)
            stats.lost_territory_nodes = bad_nodes
            stats.amount_new_territory_coords = len(self.all_territory_coords)


        return stats

    """
        # territory node locations to territory nodes (helper for below territory node containers)
        self.all_territory_nodes = dict()

        # contains territory nodes that don't contain an active cell (building/resource).
        # Only possible if a cell is depleted
        self.territory_nodes_empty = set()
        # contains territory nodes that contain an active cell (building/resource)
        self.territory_nodes_cells = {CELL_CATEGORY.BUILDING : {building_type: set() for building_type in list(BUILDING_TYPE)},
                          CELL_CATEGORY.RESOURCE : {resource_cell_type: set() for resource_cell_type in list(RESOURCE_CELL_TYPE)}}

    """

    def take_over_territory(self, coord, allowed_take_overs, stats_only = False):

        """
        For use in stats mode:
        Stores backup of territory data for each group so it can be restored after
        """
        class TerritoryBackupData():
            def __init__(self, group_id,
                         all_territory_nodes_backup,
                         territory_nodes_empty_backup,
                         territory_nodes_cells_backup,
                         all_territory_coords_backup):
                self.group_id = group_id
                self.all_territory_nodes_backup = all_territory_nodes_backup
                self.territory_nodes_empty_backup = territory_nodes_empty_backup
                self.territory_nodes_cells_backup = territory_nodes_cells_backup
                self.all_territory_coords_backup = all_territory_coords_backup

        # (stats mode) save a copy of the world to restore it afterwards
        save_territory_map = guiwindow.WORLD_INSTANCE.territory_map.copy() if stats_only else guiwindow.WORLD_INSTANCE.territory_map

        # actual node to take over
        takeover_node = TerritoryNode(coord, None, True)

        # coord data of corridor to this node: will include the max corridor size
        takeover_territories = takeover_node.hostile_takeover_max_territory_pixels(self.group, allowed_take_overs)

        violated_groups = set()

        # if coords of takeover overlap with any other groups, record the group
        for coord in takeover_territories:
            previous_territory_owner = guiwindow.WORLD_INSTANCE.world[coord[0]][coord[1]].territory
            # set land to null where we invade enemy territory
            if previous_territory_owner != self.group.id_number and previous_territory_owner is not None:
                violated_groups.add(previous_territory_owner)
                guiwindow.WORLD_INSTANCE.set_territory(coord, None)

        # (stats mode) used to associate territory backup data with group {group_id : TerritoryBackupData}
        group_backup_territory_data = {}

        for group_id in violated_groups:

            group = guiwindow.WORLD_INSTANCE.groups[group_id]
            # (stats mode) record territory data of group before making manipulations
            if stats_only:

                group_backup_territory_data[group_id] = TerritoryBackupData(self.group.id_number,
                                                                            deepcopy(group.knowledge_group_territory_nodes.all_territory_nodes),
                                                                            deepcopy(group.knowledge_group_territory_nodes.territory_nodes_empty),
                                                                            deepcopy(group.knowledge_group_territory_nodes.territory_nodes_cells),
                                                                            deepcopy(group.knowledge_group_territory_nodes.all_territory_coords))

            for node in group.knowledge_group_territory_nodes.all_territory_nodes.values():

                # calculate shortest route back for all nodes
                node.calculate_route_back(group, [])

                # create a imaginary cooridoor using this new route
                imagination_cooridoor = node.get_territory_at_maturity(MAX_POSSIBLE_CORRIDOR_SIZE, [group_id])

                # set all its pixels to this imaginary route - but with correct corridor size.
                # This is important because all pixels may contain a lot of old data due to stockpile location
                # moving around a lot.
                node.all_territory_pixels = node.get_territory_at_maturity(node.get_current_size(), [group_id])

                # if theres any intersection with takeover territories in the bounds of
                # these imaginary cooridoors, we need to recalculate their path
                if not imagination_cooridoor.isdisjoint(takeover_territories):
                    node.reset_size()



        # (stats mode) save this groups territory data so can backup after
        all_territory_coords_save = deepcopy(self.all_territory_coords) if stats_only else self.all_territory_coords
        all_territory_nodes_save = deepcopy(self.all_territory_nodes) if stats_only else self.all_territory_nodes
        territory_nodes_empty_save = deepcopy(self.territory_nodes_empty) if stats_only else self.territory_nodes_empty
        territory_nodes_cells_save = deepcopy(self.territory_nodes_cells) if stats_only else self.territory_nodes_cells

        # update this groups territory data reo reflect new point
        self.attempt_register_territory_node(takeover_node)
        self.update_stockpile_territory()

        out_stats = []

        for group in violated_groups:
            stats = guiwindow.WORLD_INSTANCE.groups[group].knowledge_group_territory_nodes.update_stockpile_territory()
            out_stats.append(stats)


        # restore this groups territory


        # (stats mode) set the world map back to what it was prior


        guiwindow.WORLD_INSTANCE.territory_map = save_territory_map

        guiwindow.WORLD_INSTANCE.apply_territory_map()

        # for item in guiwindow.WORLD_INSTANCE.territory_map:
        #     print(list(item))

        self.all_territory_coords = all_territory_coords_save
        self.all_territory_nodes = all_territory_nodes_save
        self.territory_nodes_empty = territory_nodes_empty_save
        self.territory_nodes_cells = territory_nodes_cells_save


        # self.update_stockpile_territory()

        # if stats mode, restore world territory and restore each groups territory prior to this function
        if stats_only:
            guiwindow.WORLD_INSTANCE.apply_territory_map()
            for group_id in group_backup_territory_data.keys():
                group = guiwindow.WORLD_INSTANCE.groups[group_id]
                group.knowledge_group_territory_nodes.all_territory_coords = group_backup_territory_data[group_id].all_territory_coords_backup
                group.knowledge_group_territory_nodes.all_territory_nodes = group_backup_territory_data[group_id].all_territory_nodes_backup
                group.knowledge_group_territory_nodes.territory_nodes_empty = group_backup_territory_data[group_id].territory_nodes_empty_backup
                group.knowledge_group_territory_nodes.territory_nodes_cells = group_backup_territory_data[group_id].territory_nodes_cells_backup
                # group.update_stockpile_territory()

        return out_stats


    def to_string(self):
        out = ""
        out += "territory buildings: %s\n" % str([(cell_type, "%s"%(len(amount))) for cell_type, amount in self.territory_nodes_cells[CELL_CATEGORY.BUILDING].items()])
        out += "territory resources: %s\n" % str([(cell_type, "%s"%(len(amount))) for cell_type, amount in self.territory_nodes_cells[CELL_CATEGORY.RESOURCE].items()])
        out += "territory empty: %s\n" % len(self.territory_nodes_empty)
        return out