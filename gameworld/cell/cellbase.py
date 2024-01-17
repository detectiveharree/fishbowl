from ai.humanai.relationships.information.informationlocationcell import InformationLocationCell
from copy import deepcopy
from gameworld.territorynode import TerritoryNode

class CellBase():

    def __init__(self, locations, cell_type, cell_category):
        self.locations = frozenset(locations)
        self.interactable_locations = set()
        self.default_interactable_locations = frozenset()
        self.current_interactions = 0
        self.cell_type = cell_type
        self.cell_category = cell_category

        # helper for territories. We may want to set the spotted at location
        self.human_spotted = True

    def reset_interactable_locations(self):
        self.interactable_locations = set(self.default_interactable_locations)

    def to_territory_node(self):
        return TerritoryNode(self.locations, self, self.human_spotted)

    def __hash__(self):
        return hash((self.locations, self.cell_type, self.cell_category))

    def __eq__(self, other):
        return self.__class__ == other.__class__ and self.locations == other.locations and\
               self.cell_type == other.cell_type and\
               self.cell_category == other.cell_category

    def __repr__(self):
        return "CellBase %s %s %s interactable %s" % (self.cell_category, self.cell_type, self.locations, self.interactable_locations)