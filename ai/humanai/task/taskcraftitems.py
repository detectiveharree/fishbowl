from ai import task
import ai.humanai.actions.actiongotolocation
from ai.humanai.actions.actionbuildbuilding import ActionBuildBuilding
from ai.humanai.actions.actioninteractcellblacksmithcraft import ActionInteractCellBlacksmithCraft


class TaskCraftItems(task.Task):

    def __init__(self, amount_ticks, group_action):
        self.group_action = group_action
        self.amount_ticks = amount_ticks


    """
    Possible actions that the user can do to satisfy this pre requisite.
    Note the action with the cheapest action tree will be picked.
    """
    def possible_actions(self):
        return [ActionInteractCellBlacksmithCraft(self.amount_ticks, self.group_action)]


    def __repr__(self):
        return str("Crafting items")