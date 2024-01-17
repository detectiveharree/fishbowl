
import numpy as np
import global_params
import gameworld.worldcell
from PIL import Image
from items.itemresources.itemresource import ResourceType
import pandas as pd
import random
from random import randint
from random import shuffle
from math import sqrt
from gameworld.cell.cellresource.cellresourceberrybush import CellResourceBerryBush
from gameworld.cell.cellresource.cellresourcetreesnow import CellResourceTreeSnow
from gameworld.cell.cellresource.cellresourcetreegrass import CellResourceTreeGrass
from gameworld.cell.cellresource.cellresourcefreshwaterbank import CellResourceFreshWaterBank
from gameworld.cell.cellresource.cellresourcetreedesert import CellResourceTreeDesert
from gameworld.cell.cellresource.cellresourcetreeswamp import CellResourceTreeSwamp
from gameworld.cell.cellresource.cellresourceorewhitesteel import CellResourceOreWhiteSteel
from gameworld.cell.cellresource.cellresourceoreiron import CellResourceOreIron
from gameworld.cell.cellresource.cellresourceoredarkiron import CellResourceOreDarkIron
from gameworld.cell.cellresource.cellresourceoreblacksteel import CellResourceOreBlackSteel
from gameworld.cell.cellresource.cellresourceorebronze import CellResourceOreBronze
from gameworld.cell.cellresource.cellresourceorebrass import CellResourceOreBrass
from gameworld.cell.cellresource.cellresourcerock import CellResourceRock
from datetime import datetime
from humanbase import HumanState
from ai import pathfinding
import logging
from global_params import UNCLAIMED_TERRITORY_FLAG
import copy
from ai.groupai.knowledge.knowledgegroupterritorynodes import KnowledgeGroupTerritoryNodes
import logging


loadable_resource_map = {CellResourceBerryBush.get_loader_colour() : CellResourceBerryBush,
                      CellResourceTreeSnow.get_loader_colour() : CellResourceTreeSnow,
                      CellResourceTreeGrass.get_loader_colour() : CellResourceTreeGrass,
                      CellResourceTreeDesert.get_loader_colour() : CellResourceTreeDesert,
                      CellResourceTreeSwamp.get_loader_colour() : CellResourceTreeSwamp,
                      CellResourceOreWhiteSteel.get_loader_colour() : CellResourceOreWhiteSteel,
                      CellResourceOreIron.get_loader_colour() : CellResourceOreIron,
                      CellResourceOreDarkIron.get_loader_colour() : CellResourceOreDarkIron,
                      CellResourceOreBlackSteel.get_loader_colour() : CellResourceOreBlackSteel,
                      CellResourceOreBronze.get_loader_colour() : CellResourceOreBronze,
                      CellResourceOreBrass.get_loader_colour() : CellResourceOreBrass,
                      CellResourceRock.get_loader_colour() : CellResourceRock}





"""
World class.
Stores humans array
Stores world array
"""

# img= Image.open("filename.jpeg")
# print(np.asarray(img))
# self.world = self.colour_to_data_map(np.asarray(img))
class World():

    def __init__(self):

        self.human_id_counter = 0
        self.group_id_counter = 0
        self.skilled_get_resource_id_counter = 0
        self.skilled_get_build_id_counter = 0
        self.skilled_get_craft_id_counter = 0
        self.task_get_survival_resources_id_counter = 0
        self.task_build_id_counter = 0
        self.task_craft_item_id_counter = 0
        self.buffer_factor_id_counter = 0
        self.item_id_counter = 0
        self.knowledge_sleeping_location_tent_id_counter = 0
        self.knowledge_sleeping_location_house_id_counter = 0
        self.public_info_id_counter = 0
        self.interaction_id_counter = 1



        # re renders all pixels every tick where players are on
        self.rerender_player_locations = True
        self.rerender_group_sleeper_cells = False
        self.rerender_group_territories = False
        self.rerender_group_territories_on_top = False

        # id to human
        self.humanDict = {}
        self.groups = {}
        self.update_pixels = []
        self.cells = set()

        """
        Start the world 8 hours in.
        This is because people are initaised with 0 tiredness.
        """
        self.time_ticks = global_params.hourly_ticks * 8
        self.time_hour = 8
        self.time_day = 0

        # optimisation: ticks up whenever a change is made to territory map
        self.territory_change_counter = 0
        self.last_day_complete = datetime.now()
        self.last_day_taken = datetime.now()
        self.est_year_taken = datetime.now()




    def init_world(self):
        # the world with actual data in now
        img= Image.open("gameworld/map.png")

        temp_image = (np.array(img).copy())[:,:,:3]

        imgresources = Image.open("gameworld/resourcemap.png")
        temp_image_resources = (np.array(imgresources).copy())[:, :, :3]


        print("Converting map.png to cell map")
        self.colour_to_ground_map(temp_image)

        print("Converting map.png to cell map")
        self.apply_resources_from_colour(temp_image_resources)


        # self.world = self.colour_to_data_map((np.load("test_map.npy")))
        print("Generating traversable map")
        self.traverse_map = self.data_to_traversable_map(self.world)

        print("Generating territory map")
        self.territory_map = self.data_to_territory_map(self.world)


        # the world as a image
        print("Generating display")
        self.display = self.data_to_colour_map(self.world)
        print("Done loading map")





    def set_territory(self, loc, group):

        # group id + 10000
        new_val = group.id_number + 10000 if group is not None else UNCLAIMED_TERRITORY_FLAG
        old_val = self.territory_map[loc[0]][loc[1]]

        self.world[loc[0]][loc[1]].set_territory(group)
        self.territory_map[loc[0]][loc[1]] = new_val
        self.rerender_location(loc)

        # if no change then don't execute below logic which will reset caches
        if old_val == new_val:
            return
        # optimisation - resets cache
        self.territory_change_counter += 1

    """
    Transfers all territory from one group to another
    """
    def transfer_territories(self, original_group, new_group):
        logging.info("Transfering territory from %s to %s" % (original_group.id_number, new_group.id_number))
        new_group.knowledge_group_territory_nodes = original_group.knowledge_group_territory_nodes
        new_group.knowledge_group_territory_nodes.group = new_group
        original_group.knowledge_group_territory_nodes = KnowledgeGroupTerritoryNodes(original_group)
        new_val = new_group.id_number + 10000
        # for coord in new_group.knowledge_group_territory_nodes.all_territory_coords:
        #     self.set_territory(coord, new_group)
        for i, row in enumerate(self.world):
            for y, cell in enumerate(row):
                if cell.territory == original_group.id_number:
                    self.world[i][y].set_territory(new_group)
                    self.territory_map[i][y] = new_val
                    self.rerender_location((i, y))

        self.territory_change_counter += 1

    """
    Signals that we need to rerender a location
    """
    def rerender_location(self, location):
        self.update_pixels.append(location)
        pass

    """
    Applys territory data to world cells.
    """
    def apply_territory_map(self):
        for i, row in enumerate(self.territory_map):
            for y, cell in enumerate(row):
                id = self.territory_map[i][y]
                if id >= 10000:
                    try:
                        self.set_territory((i, y), self.groups[id - 10000])
                    except Exception as e:
                        print("Error: leftover territory")
                    continue
                if id == -1:
                    continue
                self.set_territory((i, y), None)


    """
    Converts data map to picture
    """
    def data_to_traversable_map(self, data_map):
        traversable_map = np.zeros((len(self.world), len(self.world[0])), dtype="int32")
        for i, row in enumerate(data_map):
            for y, cell in enumerate(row):
                traversable_map[i][y] = 1000 if cell.is_explorable() else -1
        return traversable_map


    """
    Converts data map to picture
    -1 Not traversable
    """
    def data_to_territory_map(self, data_map):
        traversable_map = np.zeros((len(self.world), len(self.world[0])), dtype="int32")
        for i, row in enumerate(data_map):
            for y, cell in enumerate(row):
                traversable_map[i][y] = UNCLAIMED_TERRITORY_FLAG if cell.is_explorable() else -1
        return traversable_map


    """
    Reads map.png and places ground
    """
    def colour_to_ground_map(self, picture):
        self.world = np.ndarray((picture.shape[0], picture.shape[1],),dtype=np.object)
        for iy, ix, _ in np.ndindex(picture.shape):
            rgb = picture[iy][ix]
            self.world[iy][ix] = gameworld.worldcell.Cell(iy, ix, rgb)

    """
    Converts picture to data map
    """
    def apply_resources_from_colour(self, picture):

        # first time just place ground type if required
        for iy, ix, _ in np.ndindex(picture.shape):
            rgb = tuple(picture[iy][ix])
            if rgb in loadable_resource_map.keys():
                type = loadable_resource_map[rgb]
                if type.get_loader_ground_cell_type() is not None:
                    self.world[iy][ix].ground_type = type.get_loader_ground_cell_type()



        # second time actually place resources, because sometime its dependent on the ground type
        for iy, ix, _ in np.ndindex(picture.shape):
            rgb = tuple(picture[iy][ix])
            if rgb in loadable_resource_map.keys():
                if not self.world[iy][ix].is_explorable():
                    continue
                type = loadable_resource_map[rgb]
                type({(iy, ix)}).register_to_world()


        # finally load fresh water bank resource cells
        for iy, ix, _ in np.ndindex(picture.shape):
            loc = (iy, ix)
            ground_type = self.world[iy][ix].ground_type
            if ground_type == gameworld.worldcell.GroundType.LAKE or ground_type == gameworld.worldcell.GroundType.RIVER:
                for coord in list(pathfinding.get_adjacent(loc)):
                    if self.world[coord[0]][coord[1]].is_explorable():
                        CellResourceFreshWaterBank({(coord[0], coord[1])}).register_to_world()





    """
    Converts data map to picture
    """
    def data_to_colour_map(self, data_map):
        colour_map = np.ndarray((data_map.shape[0], data_map.shape[1],),dtype="int8, int8, int8")
        for i, row in enumerate(data_map):
            for y, cell in enumerate(row):
                if cell is None:
                    # (default value is None so in personalised map this is useful)
                    colour_map[i][y] = (0, 0, 0)
                else:
                    colour_map[i][y] = cell.get_colour(self.rerender_group_territories, self.rerender_group_territories_on_top)

        return colour_map


    """
    Updates all humans
    """
    def tick(self):
        self.time_ticks += 1

        for cell in self.cells:
            cell.tick()

        #
        for human in list(self.humanDict.values()):
            if human.state == HumanState.DEAD:
                human.force_finish_task()
                del self.humanDict[human.id_number]
                human.group.remove_member(human)
                self.world[human.location[0]][human.location[1]].people_on_cell.remove(human.id_number)
                self.rerender_location(human.location)
                continue
            # logging.info("%s %s %s" % (human.id_number, human.state, human.body.health.get()) )
            human.tickly_update()


        # if self.humanDict:
        #     if randint(0, 50) == 30:
        #         random.choice(list(self.humanDict.values())).die()



        for group in self.groups.values():
            group.tickly_update()

        if self.time_ticks % global_params.hourly_ticks == 0:

            for human in self.humanDict.values():
                human.hourly_update()

            for cell in self.cells:
                cell.hourly_update()

            for group in self.groups.values():
                group.hourly_update()
            self.time_hour += 1


        # print(self.time_ticks)
        # print(global_params.daily_ticks)
        # print(self.time_ticks % global_params.daily_ticks == 0)
        if self.time_ticks % global_params.daily_ticks == 0:

            for human in self.humanDict.values():
                human.daily_update()

            for cell in self.cells:
                cell.daily_update()

            for group in self.groups.values():
                group.daily_update()

            self.time_ticks = 0
            self.time_hour = 0
            self.time_day += 1
            complete_time = datetime.now()
            self.last_day_taken = complete_time - self.last_day_complete
            self.est_year_taken = (self.last_day_taken * 365)
            self.last_day_complete = complete_time
            print("Day | %s" % self.last_day_taken)
            print("Year | %s" % self.est_year_taken)
            print("Max | %s" % (self.est_year_taken * 100))


        # stop updating group if it is empty
        for group in self.groups.values():
            if group.should_disable():
                group.disable()

        self.groups = {group_id: group for group_id, group in self.groups.items() if not group.should_disable()}




    """
    Returns the display
    """
    def get_display(self):

        """
        Re renders the pixel where people are on.
        This is useful for attributes that change often.
        """
        if self.rerender_player_locations:
            for human in self.humanDict.values():
                self.rerender_location(human.location)

        """
        Updates all the pixels
        """
        while self.update_pixels:
            update_pixel = self.update_pixels.pop(0)
            cell = self.world[update_pixel[0]][update_pixel[1]]
            self.display[update_pixel[0]][update_pixel[1]] = cell.get_colour(self.rerender_group_territories, self.rerender_group_territories_on_top)


        if self.rerender_group_sleeper_cells:
            for group in self.groups.values():
                for sleeper_cell in group.knowledge_sleeping_location_tents.get_sleeping_locations():
                    self.display[sleeper_cell[0]][sleeper_cell[1]] = (0, 0, 0)


        return self.display

    def get_debug_info(self):
        out = ""
        out += "amount updates: %s\n" % len(self.update_pixels)
        return out



