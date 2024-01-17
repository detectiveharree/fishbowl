from ai.humanai.relationships.knowledge.knowledge import Knowledge
from gameworld.cell.cellresource.cellresource import RESOURCE_CELL_TYPE
from gameworld.cell.cellbuilding.cellbuilding import BUILDING_TYPE
from ai.humanai.relationships.information.informationlocationcell import InformationLocationCell
from gameworld.cell.cell import CELL_CATEGORY
import ai.pathfinding
import guiwindow

"""
The knowledge of all people
"""
class KnowledgeInteractableCellLocations(Knowledge):

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
        # {coord : CellBase}
        self.location_to_cell = dict()

        # {CELL_CATEGORY, {CELL_CATEGORY : {CellBase}}}
        self.cells = {CELL_CATEGORY.BUILDING : {building_type: set() for building_type in list(BUILDING_TYPE)},
                      CELL_CATEGORY.RESOURCE : {resource_cell_type: set() for resource_cell_type in list(RESOURCE_CELL_TYPE)}}

    def register_cellbase(self, cellbase):

        for location in cellbase.locations:
            self.location_to_cell[location] = cellbase

        self.cells[cellbase.cell_category][cellbase.cell_type].add(cellbase)


    def remove_cell_at_location(self, location):
        existing_cell = self.location_to_cell[location]
        for loc in existing_cell.locations:
            del self.location_to_cell[loc]
        self.cells[existing_cell.cell_category][existing_cell.cell_type].remove(existing_cell)
        return existing_cell

    """
    Called when we spot a cell we already recognised before.
    Opportunity to update the persons knowledge if it
    """
    def update_same_cell(self, new_observation, old_observation):
        old_observation.interactable_locations = new_observation.interactable_locations


    def is_same_cell_type(self, location, cellbase):
        if location in self.location_to_cell.keys():
            existing_cell = self.location_to_cell[location]
            return existing_cell == cellbase
        return False


    def register_from_information(self, human, informationcell):

        """
        Remove old cells at recording locations
        """
        for location in informationcell.location:
            if location in self.location_to_cell.keys():

                # i.e. this exact cell with same dimensions i.e. locations, type and category
                # exists here, don't bother removing anything.
                if informationcell.cellbase == self.location_to_cell[location]:
                    self.update_same_cell(informationcell.cellbase, self.location_to_cell[location])
                    break

                self.remove_cell_at_location(location)

        """
        No matter what happens, we always want to attempt to register a cellbase.
        If it already is in knowledge, nothing will happen and if it's not registered in territory, 
        it might do so.
        """
        if informationcell.cellbase is not None:
            self.register_cellbase(informationcell.cellbase)

    """
    Return True if there is a interactable cell at a location given that it should have
    a certain cell type and category.
    
    
    Appears as though 59, 94 from river cell 59, 93 gets taken, but no one on block
    """
    def get_cell_if_location_interactable(self, cell_category, cell_type, location):
        """
        This approach is a bit slimy, but its hard to cache interactable locations
        of cells due to the fact that they can overlap.

        Therefore, under the assumption that a interactable location will be next to the cell,
        we will check the perimeter around the player to see if any of them are a registered cell
        location and if so check it's interactable locations.
        """
        # optimisation - most of the time the interactable location of the cell will be its actual location
        # so check this first before preceding with the perimeter check
        if self._check_is_location_interactable(cell_category, cell_type, location, location):
            return self.location_to_cell[location]
        # else:
        #     print(guiwindow.WORLD_INSTANCE.world[location[0]][location[1]].cell_type)

        for potential_cell_location in ai.pathfinding.get_perimeter(location):
            if self._check_is_location_interactable(cell_category, cell_type, potential_cell_location, location):
                return self.location_to_cell[potential_cell_location]
            # else:
            #     print(guiwindow.WORLD_INSTANCE.world[potential_cell_location[0]][potential_cell_location[1]].cell_type)

        return None

    """
    Helper function for get_cell_if_location_interactable
    
    Given a cell location, check if the right type of cell exists at that location,
    and if so return if the interactable_location is correct
    """
    def _check_is_location_interactable(self, cell_category, cell_type, cell_location, interactable_location):
        # check if we know of a cell at that location
        if cell_location not in self.location_to_cell:
            return False

        current_cell_at_location = self.location_to_cell[cell_location]
        #  check if known cell has right types
        if current_cell_at_location.cell_type != cell_type or current_cell_at_location.cell_category != cell_category:
            return False

        #  check if known cell has right types
        # print("imagined: %s" % current_cell_at_location)
        return interactable_location in current_cell_at_location.interactable_locations


    """
    This is where you state whether someone is willing to consider a cell as interactable.
    """
    def willing_to_interact(self, location, human):
        worlcell = guiwindow.WORLD_INSTANCE.world[location[0]][location[1]]
        if worlcell.territory is None or worlcell.territory == human.group.id_number:
            return True
        if human.group.parent_group is not None:
            return worlcell.territory == human.group.parent_group.id_number
        return False


    def get_interactable_cells(self, cell_category, cell_type, human):
        return set().union(*[[location for location in cell_base.interactable_locations if self.willing_to_interact(location, human)]
                             for cell_base in self.cells[cell_category][cell_type] if len(cell_base.interactable_locations) != 0])


    def to_string(self):
        out = ""
        out += "buildings: %s\n" % str([(cell_type, len(amount)) for cell_type, amount in self.cells[CELL_CATEGORY.BUILDING].items()])
        out += "resources: %s" % str([(cell_type, len(amount)) for cell_type, amount in self.cells[CELL_CATEGORY.RESOURCE].items()])

        return out

    """
    Use this method to return a random piece of information
    that you can create from the knowledge. 
    This is for use in interactions, get_random_information may be called
    to simulate random conversation being passed.
    """
    def get_random_information(self):
        source = random.choice(list(self.location_to_cell.values()))
        return InformationLocationCell(set([source.location]), source)
