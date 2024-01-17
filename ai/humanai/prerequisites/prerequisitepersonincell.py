from ai.prerequisite import Prerequisite
import ai.humanai.actions.actiongotoperson
import guiwindow

"""

A Prerequisite is a predicate that must be true to complete a action.
It is a prediction/estimation based on information that a human has, 
that is used when a human undergoes decision making. Therefore, 
DO NOT leak information that the human does not know i.e. world data.
"""
class PrerequisitePersonInCell(Prerequisite):

    def __init__(self, target_person_id):
        self.target_person_id = target_person_id

    """
    Returns a list of possible actions that may satisfy this prerequisite.
    """
    def possible_actions(self, human):
        return [ai.humanai.actions.actiongotoperson.ActionGoToPerson(self.target_person_id)]

    """
    Returns true/false if the current prerequisite is satisfied.
    """
    def is_satisfied(self, human):
        # if guiwindow.WORLD_INSTANCE.humanDict[self.target_person_id].current_building is not None:
        #     return False
        return self.target_person_id in guiwindow.WORLD_INSTANCE.world[human.location[0]][human.location[1]].people_on_cell
