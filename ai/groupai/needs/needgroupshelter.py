from ai.groupai.needs.needgroup import NeedGroup, GROUP_NEED_TYPE
from items.itemresources.itemresource import ResourceType
from ai.groupai.task.taskgroupbuildbuilding import TaskGroupBuildBuilding
from gameworld.cell.cellbuilding.cellbuildinghouse import BuildingHouse
import global_params
import random
import ai.pathfindingbuilding
from gameworld.cell.cellbuilding.cellbuilding import BUILDING_TYPE


class NeedGroupShelter(NeedGroup):

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
        super().__init__(GROUP_NEED_TYPE.SHELTER) # ALWAYS CALL PARENT CONSTRUCTOR
        self.need_level = 0

    """
    Called once a day.
    """
    def get_task(self, group, adjusted_need_level):

        if adjusted_need_level >= 50:
            if group.all_territory_coords:
                return [TaskGroupBuildBuilding(GROUP_NEED_TYPE.SHELTER, 50, BuildingHouse(ai.pathfindingbuilding.place_building(self.building.get_cell_type(), group)), group)]

        return []
