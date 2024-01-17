from ai.prerequisite import Prerequisite
from ai.humanai.actions.actionlookforinteractablecell import ActionLookForInteractableCell

"""
Is the human knows of a resource location that is currently empty.

A Prerequisite is a predicate that must be true to complete a action.
It is a prediction/estimation based on information that a human has, 
that is used when a human undergoes decision making. Therefore, 
DO NOT leak information that the human does not know i.e. world data.
"""
class PrerequisiteKnowsInteractableCellLocation(Prerequisite):

    """
    DO NOT DELETE THIS. PASTE THIS IN FOR EVERY NEW OBJECT THAT WILL BE STORED IN A SET/DICTIONARY.
    THIS IS ESSENTIAL FOR MAKING SURE THE PROGRAM PERFORMS EXACTLY THE SAME EVERY TIME!

    assert(false) WILL CRASH THE PROGRAM IF YOU ATTEMPT TO PUT THIS OBJECT INTO A SET/DICT WITHOUT FIRST MODIFYING THE FUNCTION.
    THIS IS DONE ON PURPOSE TO PREVENT YOU FROM ACCIDENTALLY LEAKING NON-DETERMINISM INTO THE PROGRAM.
    SPEAK TO ME (TOM) AND I WILL EXPLAIN WHAT TO DO.
    """
    def __hash__(self):
        assert(False)


    def __init__(self, cell_category, cell_type):
        self.cell_category = cell_category
        self.cell_type = cell_type

    """
    Returns a list of possible actions that may satisfy this prerequisite.
    """
    def possible_actions(self, human):
        return [ActionLookForInteractableCell(self.cell_category, self.cell_type, human)]

    """
    Return known locations of resource
    """
    def get_data(self, human):
        return human.knowledge_cell_locations.get_interactable_cells(self.cell_category, self.cell_type, human)

    """
    Returns true/false if the current prerequisite is satisfied.
    """
    def is_satisfied(self, human):
        return len(human.knowledge_cell_locations.get_interactable_cells(self.cell_category, self.cell_type, human)) > 0





