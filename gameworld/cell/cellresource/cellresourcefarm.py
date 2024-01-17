from gameworld.cell.cellresource.cellresource import CellResource, RESOURCE_CELL_TYPE
from items.itemresources.itemresource import ResourceType
from gameworld.worldcell import GroundType

DEFAULT_DAILY_AMOUNT = 40

class CellResourceFarm(CellResource):

    """
    DO NOT DELETE THIS. PASTE THIS IN FOR EVERY NEW OBJECT THAT WILL BE STORED IN A SET/DICTIONARY.
    THIS IS ESSENTIAL FOR MAKING SURE THE PROGRAM PERFORMS EXACTLY THE SAME EVERY TIME!

    assert(false) WILL CRASH THE PROGRAM IF YOU ATTEMPT TO PUT THIS OBJECT INTO A SET/DICT WITHOUT FIRST MODIFYING THE FUNCTION.
    THIS IS DONE ON PURPOSE TO PREVENT YOU FROM ACCIDENTALLY LEAKING NON-DETERMINISM INTO THE PROGRAM.
    SPEAK TO ME (TOM) AND I WILL EXPLAIN WHAT TO DO.
    """
    def __hash__(self):
        return hash(self.locations)

    def __eq__(self, other):
        return self.__class__ == other.__class__ and self.locations == other.locations

    def __init__(self, locations):
        super(). __init__(locations)
        self.amount_available = DEFAULT_DAILY_AMOUNT
        # self.interactable_locations = set()
        # self.default_interactable_locations = frozenset()



    """
    Called every tick
    """
    def daily_update(self):
        self.amount_available = DEFAULT_DAILY_AMOUNT
        self.interactable_locations = set(self.default_interactable_locations)
        pass

    """
    Called when attempt is made to harvest this item.
    Must return some amount.
    """
    def harvest(self, amount):
        if amount >= self.amount_available:
            amount_harvested = self.amount_available
            self.amount_available = 0
            self.interactable_locations.clear()
            self.occupied_locations_helper.clear()
            return amount_harvested

        self.amount_available -= amount
        return amount

    """
    Return the type of the cell
    """
    @staticmethod
    def get_cell_type():
        return RESOURCE_CELL_TYPE.FARM


    """
    If detecting this colour while loading will place this resource down.
    """
    @staticmethod
    def get_loader_colour():
        return (0, 150, 0)

    """
    Returns the colour for displaying the cell
    """
    def get_debug_colour(self):
        return (0, 150, 0)


    """
    (Optional) Returns string containing info for debugging.
    """
    def debug_info(self):
        return "daily left: %s/%s" % (round(self.amount_available, 2), DEFAULT_DAILY_AMOUNT)



