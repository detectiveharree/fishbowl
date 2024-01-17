from abc import ABC, abstractmethod
import guiwindow
from gameworld.cell.cellbase import CellBase

from enum import Enum

class CELL_CATEGORY(Enum):

    BUILDING = 1
    RESOURCE = 2

    def __repr__(self):
        return self.name


class Cell(CellBase, ABC):


    def __init__(self, locations):
        super(). __init__(locations, self.get_cell_type(), self.get_cell_category())


    def register_to_world(self):
        self.interactable_locations = self.get_interactable_locations()
        self.default_interactable_locations = frozenset(self.get_interactable_locations())

        for location in self.locations:
            guiwindow.WORLD_INSTANCE.world[location[0]][location[1]].cell_type = self
            guiwindow.WORLD_INSTANCE.rerender_location(location)
        guiwindow.WORLD_INSTANCE.cells.add(self)


    """
    Called every tick to check to see if destroyed
    """
    def remove_from_world(self):
        for location in self.locations:
            guiwindow.WORLD_INSTANCE.world[location[0]][location[1]].cell_type = None
            guiwindow.WORLD_INSTANCE.rerender_location(location)
        guiwindow.WORLD_INSTANCE.cells.remove(self)


    def begin_interact(self, coord, human):
        self.current_interactions += 1

    def end_interact(self, human):
        self.current_interactions -= 1


    """
    Returns all the coordinates this cell can be interacted from.
    By default, it is simply the locations this cell is situated in
    """
    def get_interactable_locations(self):
        return set(self.locations)


    """
    Returns the colour for displaying the cell
    """
    @abstractmethod
    def get_debug_colour(self):
        ...

    """
    Return the type of the cell
    """
    @staticmethod
    @abstractmethod
    def get_cell_type():
        ...

    """
    Return the category of the cell
    """
    @staticmethod
    @abstractmethod
    def get_cell_category():
        ...


    """
    Called every tick
    """
    def tick(self):
        pass


    """
    Called every hourly tick
    """
    def hourly_update(self):
        pass

    """
    Called every daily tick
    """
    def daily_update(self):
        pass

    """
    (Optional) Returns string containing info for debugging.
    """
    def debug_info(self):
        return ""

    def __repr__(self):
        return str(self.get_cell_type())


    def to_cell_base(self, human):
        cellbase = CellBase(self.locations, self.cell_type, self.cell_category)
        cellbase.interactable_locations = set(self.interactable_locations)
        cellbase.default_interactable_locations = self.default_interactable_locations
        cellbase.human_spotted = human is not None
        return cellbase