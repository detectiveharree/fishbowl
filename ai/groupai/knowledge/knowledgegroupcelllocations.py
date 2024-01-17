from gameworld.territorynode import TerritoryNode
from gameworld.cell.cellbuilding.cellbuilding import BUILDING_TYPE
from items.itemresources.itemresource import ResourceType

from gameworld.cell.cell import CELL_CATEGORY
from gameworld.cell.cellresource.cellresource import RESOURCE_CELL_TYPE
from ai.humanai.relationships.knowledge.knowledgeinteractablecelllocations import KnowledgeInteractableCellLocations
import logging


class KnowledgeGroupCellLocations(KnowledgeInteractableCellLocations):

    """
    DO NOT DELETE THIS. PASTE THIS IN FOR EVERY NEW OBJECT THAT WILL BE STORED IN A SET/DICTIONARY.
    THIS IS ESSENTIAL FOR MAKING SURE THE PROGRAM PERFORMS EXACTLY THE SAME EVERY TIME!

    assert(false) WILL CRASH THE PROGRAM IF YOU ATTEMPT TO PUT THIS OBJECT INTO A SET/DICT WITHOUT FIRST MODIFYING THE FUNCTION.
    THIS IS DONE ON PURPOSE TO PREVENT YOU FROM ACCIDENTALLY LEAKING NON-DETERMINISM INTO THE PROGRAM.
    SPEAK TO ME (TOM) AND I WILL EXPLAIN WHAT TO DO.
    """
    def __hash__(self):
        assert(False)

    def __init__(self, group):
        super().__init__()
        self.group = group



    def register_cellbase(self, cellbase):

        super().register_cellbase(cellbase)
        claim_success = self.group.knowledge_group_territory_nodes.attempt_register_territory_node(cellbase.to_territory_node())
        # if claim_success:
        #     logging.info("Claimed %s" % cellbase)


    def remove_cell_at_location(self, location):
        existing_cell = super().remove_cell_at_location(location)
        # doesn't matter if we're here or not, all this operation will do is decache it

        """
        Actually, if cell is not what we were expecting to see and not visited before
        we still need to fire it.
        """

        self.group.knowledge_group_territory_nodes.attempt_down_grade_territory_node(existing_cell.to_territory_node())
        return existing_cell

    """
    Called when we spot a cell we already recognised before.
    Opportunity to update the persons knowledge of it
    """
    def update_same_cell(self, new_observation, old_observation):
        # if now visited, mark existing territory visited to allow it to expand
        if new_observation.human_spotted:
            self.group.knowledge_group_territory_nodes.mark_node_visited(new_observation.to_territory_node())



    def to_string(self):
        out = ""
        # out += "buildings: %s\n" % str([(cell_type, "%s/%s"%(len(amount), len(self.cells_territory[CELL_CATEGORY.BUILDING][cell_type]))) for cell_type, amount in self.cells[CELL_CATEGORY.BUILDING].items()])
        # out += "resources: %s" % str([(cell_type, "%s/%s"%(len(amount), len(self.cells_territory[CELL_CATEGORY.RESOURCE][cell_type]))) for cell_type, amount in self.cells[CELL_CATEGORY.RESOURCE].items()])

        out += "buildings: %s\n" % str([(cell_type, "%s"%(len(amount))) for cell_type, amount in self.cells[CELL_CATEGORY.BUILDING].items()])
        out += "resources: %s" % str([(cell_type, "%s"%(len(amount))) for cell_type, amount in self.cells[CELL_CATEGORY.RESOURCE].items()])

        return out