from abc import ABC, abstractmethod
import guiwindow
from ai.need import Need
from enum import Enum
from gameworld.cell.cell import CELL_CATEGORY, Cell, CellBase
from ai.humanai.relationships.information.informationlocationcell import InformationLocationCell
import ai.pathfinding
import logging

class BUILDING_TYPE(Enum):

    def __new__(cls, *args, **kwds):
        value = len(cls.__members__) + 1
        obj = object.__new__(cls)
        obj._value_ = value
        return obj

    def __init__(self, rng_placement_probability, cells):
        self.rng_placement_probability = rng_placement_probability
        self.cells = cells


    BLACKSMITH = (0.2, 1)
    HOUSE = (0.1, 1)
    FIGHTINGARENA = (0.2, 2)
    CASTLE = (1, 3)
    TAVERN = (0.05, 1)

    def __repr__(self):
        return self.name

"""
Base building class for building assets. Conceptually, building classes should contain:
    - Number of tiles taken up by the building
    - occupants of building
    - maximum building occupancy
    - trait coefficients associated with the building
    - category (productive, recreation, hygiene etc.)
    - amount of cell needed to build (in terms of raw materials and effort)
    - build progress (how much recorded build output and how much more needed)
    - location of building
"""
class Building(Cell, ABC):


    def __init__(self, locations):
        super(). __init__(locations)

        # current tick of building
        self.build_progress_tick = 0

        self.current_occupants = set() # {human_id}


    def register_to_world(self):
        super().register_to_world()
        for loc in self.locations:
            for cell in ai.pathfinding.get_perimeter(loc):
                if guiwindow.WORLD_INSTANCE.world[cell[0]][cell[1]].is_farm():
                    guiwindow.WORLD_INSTANCE.world[cell[0]][cell[1]].cell_type.remove_from_world()



    def begin_interact(self, coord, human):

        logging.info("%s entered the %s" % (human.id_number, self))
        human.current_building = self
        guiwindow.WORLD_INSTANCE.world[human.location[0]][human.location[1]].people_on_cell.remove(human.id_number)
        guiwindow.WORLD_INSTANCE.rerender_location(human.location)
        self.current_occupants.add(human.id_number)
        if len(self.current_occupants) >= self.get_building_capacity():
            self.interactable_locations.clear()

    def end_interact(self, human):

        self.interactable_locations = self.get_interactable_locations()

        human.current_building = None
        guiwindow.WORLD_INSTANCE.rerender_location(human.location)
        if human.id_number in self.current_occupants:
            logging.info("%s left the %s" % (human.id_number, self))
            self.current_occupants.remove(human.id_number)
            guiwindow.WORLD_INSTANCE.world[human.location[0]][human.location[1]].people_on_cell.add(human.id_number)

    def increase_build_progress(self, amount):
        if self.is_building_complete():
            return
        if self.build_progress_tick + amount >= self.get_building_ticks():
            # building is finished
            self.build_progress_tick = self.get_building_ticks()
            for location in self.locations:
                guiwindow.WORLD_INSTANCE.world[location[0]][location[1]].building = self
                guiwindow.WORLD_INSTANCE.rerender_location(location)
            return
        self.build_progress_tick += amount

    """
    Return the category of cell
    """
    @staticmethod
    def get_cell_category():
        return CELL_CATEGORY.BUILDING

    """
    Returns the building colour
    """
    @abstractmethod
    def get_building_colour(self):
      ...


    """
    Gets the maximum capacity of the building
    """
    @staticmethod
    @abstractmethod
    def get_building_capacity():
        ...


    """
    Returns the colour for displaying the cell
    """
    def get_debug_colour(self):
        """
        To help with debug, we will make the cell colour
        a bit darker based on it's occupancy.
        Maximum occupancy = Black
        """
        colours = []
        for colour in list(self.get_building_colour()):
            delta_max_colour = colour
            per_occupant_colour = delta_max_colour / self.get_building_capacity()
            new_colour = colour - (len(self.current_occupants) * per_occupant_colour)
            colours.append(new_colour)
        return tuple(colours)



    """
    Should return a dictionary of cell and amount required
    to build this building.
    ResourceTypes : int
    e.g.
    return {ResourceType.WOOD : 100, ResourceType.STONE : 50}
    """
    @abstractmethod
    def get_required_resources(self):
        ...


    """
    Get building ticks is the amount of ticks required to build 
    this building.
    e.g.
    return 1200
    """
    @abstractmethod
    def get_building_ticks(self):
        ...

    """
    Return true if building is complete.
    """
    def is_building_complete(self):
        return self.build_progress_tick >= self.get_building_ticks()



    """
    (Optional) Returns string containing info for debugging.
    """
    def debug_info(self):
        return "capacity %s/%s\nis_built (%s/%s)" % (len(self.current_occupants), self.get_building_capacity(), self.build_progress_tick, self.get_building_ticks())



