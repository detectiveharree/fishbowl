from ai.prerequisite import Prerequisite

from ai.humanai.actions.actiongotointeractablecell import ActionGoToInteractableCell
import guiwindow

"""

"""
class PrerequisiteAtInteractableCell(Prerequisite):

    def __init__(self, cell_category, cell_type):
        self.cell_category = cell_category
        self.cell_type = cell_type

    """
    Returns a list of possible actions that may satisfy this prerequisite.
    """
    def possible_actions(self, human):
        return [ActionGoToInteractableCell(self.cell_category, self.cell_type)]


    """
    Return known locations of resource
    """
    def get_data(self, human):
        return human.knowledge_cell_locations.get_cell_if_location_interactable(self.cell_category, self.cell_type, human.location)

    """
    Returns true/false if the current prerequisite is satisfied.
    """
    def is_satisfied(self, human):
        return human.knowledge_cell_locations.get_cell_if_location_interactable(self.cell_category, self.cell_type, human.location) is not None




