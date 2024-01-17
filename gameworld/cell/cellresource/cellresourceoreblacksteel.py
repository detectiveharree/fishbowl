from gameworld.cell.cellresource.cellresource import CellResource, RESOURCE_CELL_TYPE
from gameworld.cell.cellresource.cellresourcedepletable import CellResourceDepletable
from items.itemresources.itemresource import ResourceType
import guiwindow
import ai.pathfinding
from gameworld.worldcell import GroundType



class CellResourceOreBlackSteel(CellResourceDepletable):

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
    Returns the amount this resource starts with
    """
    def get_starting_amount(self):
        return 100000


    """
    Return the type of the cell
    """
    @staticmethod
    def get_cell_type():
        return RESOURCE_CELL_TYPE.BLACK_STEEL_ORE


    """
    If detecting this colour while loading will place this resource down.
    """
    @staticmethod
    def get_loader_colour():
        return (77, 77 ,77)

    """
    Returns the colour for displaying the cell
    """
    def get_debug_colour(self):
        return (77, 77 ,77)

    """
    Returns all the coordinates this cell can be interacted from.
    By default, it is simply the locations this cell is situated in
    """
    def get_interactable_locations(self):
        return set([coord for coord in list(ai.pathfinding.get_adjacent(list(self.locations)[0]))
                if guiwindow.WORLD_INSTANCE.world[coord[0]][coord[1]].is_explorable()])
