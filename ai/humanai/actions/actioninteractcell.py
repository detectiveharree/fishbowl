from ai.action import Action
from ai.humanai.prerequisites.prerequisiteatinteractablecell import PrerequisiteAtInteractableCell
from gameworld.cell.cell import CELL_CATEGORY
import global_params
import guiwindow

"""
Harvests a resource that player is currently on

A wrapper for performing an action, including a cost function, prerequisite conditions and worker logic.
"""


class ActionInteractCell(Action):

    def __init__(self, cell_type, cell_category):
        self.cell_type = cell_type
        self.cell_category = cell_category

        self.found_cell = None  # actual cell object node assigned in pre begin

    """
    Returns a list of prerequisites that must be satisfied in order to complete the action.

    Note the order of these prerequisites reflects the order of their potential actions that need
    to be completed for this action to be possible to do. Therefore order it appropriately.
    Note the action may not necessarily be executed if all the prerequisites are true. 
    The prerequisites are used in the decision making process, however the optional
    method pre_begin_checks returns the final check before the action is executed in case new information
    is is revealed.
    """

    def get_prerequisites(self):
        return [PrerequisiteAtInteractableCell(self.cell_type, self.cell_category)]

    """
    The estimated cost of this action.
    This occurs during the decision making process of a action tree.
    For extra accuracy, use data from prerequisites.
    """

    def get_costs(self, human):
        """
        Amount to harvest is the cost of harvesting.
        """
        return 0

    """
    Returns true/false if the action should proceed.
    Optional final checks that occur prior to the action starting (i.e. action is currently in a action tree).
    """

    def pre_begin_checks(self, human):
        if not PrerequisiteAtInteractableCell(self.cell_type, self.cell_category).is_satisfied(human):
            return False
        chosen_cell = PrerequisiteAtInteractableCell(self.cell_type, self.cell_category).get_data(human)
        # grab the real object
        any_coord = list(chosen_cell.locations)[0]
        self.found_cell = guiwindow.WORLD_INSTANCE.world[any_coord[0]][any_coord[1]].cell_type
        if self.found_cell is None:
            print("WHAT!!!???")
            exit(1)
        return True

    """
    This is called once when the action begins.
    """

    def begin(self, human):
        self.found_cell.begin_interact(human.location, human)

    """
    Called whenever a action is completed 
    """
    def on_finish(self, human):
        if self.found_cell is not None:
            self.found_cell.end_interact(human)

    def __str__(self):
        return "interact cell %s %s" % (self.cell_category, self.cell_type)
