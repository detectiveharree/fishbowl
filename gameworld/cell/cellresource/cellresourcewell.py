from gameworld.cell.cellresource.cellresource import CellResource, RESOURCE_CELL_TYPE
from items.itemresources.itemresource import ResourceType
import guiwindow
import ai.pathfinding
from gameworld.worldcell import GroundType

"""
Clone of River,
We just have this separated so we can tell in the frontend
"""

class CellResourceWell(CellResource):

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


    """
    Return the type of the cell
    """
    @staticmethod
    def get_cell_type():
        return RESOURCE_CELL_TYPE.FRESH_WATER


    """
    If detecting this colour while loading will place this resource down.
    """
    @staticmethod
    def get_loader_colour():
        return (140, 140, 140)

    """
    Returns the colour for displaying the cell
    """
    def get_debug_colour(self):
        return (140, 140, 140)

