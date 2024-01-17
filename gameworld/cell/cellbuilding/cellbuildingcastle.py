from gameworld.cell.cellbuilding.cellbuilding import Building, BUILDING_TYPE
from items.itemresources.itemresource import ResourceType

"""
Tavern building class. Conceptually, building classes should contain:
    - Number of tiles taken up by the building
    - occupants of building
    - maximum building occupancy
    - trait coefficients associated with the building
    - category (productive, recreation, hygiene etc.)
    - amount of cell needed to build (in terms of raw materials and effort)
    - build progress (how much recorded build output and how much more needed)
    - location of building
"""
class BuildingCastle(Building):

    def __init__(self, locations):
        super(). __init__(locations)

    """
    Return the type of the cell
    """
    @staticmethod
    def get_cell_type():
        return BUILDING_TYPE.CASTLE


    """
    Returns the colour for displaying building in debug mode
    """
    def get_building_colour(self):
        return (255, 0, 0)


    """
    Gets the maximum capacity of the building
    """
    @staticmethod
    def get_building_capacity():
        return 30


    """
    Should return a dictionary of cell and amount required
    to build this building.
    ResourceTypes : int
    e.g.
    return {ResourceType.WOOD : 100, ResourceType.STONE : 50}
    """
    def get_required_resources(self):
        return {ResourceType.WOOD : 1000}


    """
    Get building ticks is the amount of ticks required to build 
    this building.
    e.g.
    return 1200
    """
    def get_building_ticks(self):
        return 1200

