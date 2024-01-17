from gameworld.cell.cellresource.cellresource import CellResource, RESOURCE_CELL_TYPE
from items.itemresources.itemresource import ResourceType
import guiwindow
import ai.pathfinding
from abc import ABC, abstractmethod


class CellResourceDepletable(CellResource, ABC):


    def __init__(self, locations):
        super(). __init__(locations)
        self.amount_available = self.get_starting_amount()


    """
    Returns the amount this resource starts with
    """
    @abstractmethod
    def get_starting_amount(self):
        ...


    """
    Called when attempt is made to harvest this item.
    Must return some amount.
    """
    def harvest(self, amount):

        if self.amount_available == 0:
            return 0

        if amount >= self.amount_available:
            amount_harvested = self.amount_available
            self.amount_available = 0
            self.interactable_locations.clear()
            self.occupied_locations_helper.clear()
            self.remove_from_world()
            return amount_harvested

        self.amount_available -= amount
        return amount


    """
    (Optional) Returns string containing info for debugging.
    """
    def debug_info(self):
        return "amount left: %s/%s" % (round(self.amount_available, 2), self.get_starting_amount())