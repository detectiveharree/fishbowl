from ai.action import Action
import ai.humanai.prerequisites.prerequisitepersonincell
import global_params
import ai.humanai.task.taskinitiateinteraction
import guiwindow
# import ai.humanai.relationships.interaction.interactionsocialise.interActionInitiateInteractiontalk
from ai.humanai.prerequisites.prerequisitepersonincell import PrerequisitePersonInCell
from ai.need import NEED_TYPE

"""
Harvests a resource that player is currently on

A wrapper for performing an action, including a cost function, prerequisite conditions and worker logic.
"""


class ActionInteractPersonInitiate(Action):

    """
    DO NOT DELETE THIS. PASTE THIS IN FOR EVERY NEW OBJECT THAT WILL BE STORED IN A SET/DICTIONARY.
    THIS IS ESSENTIAL FOR MAKING SURE THE PROGRAM PERFORMS EXACTLY THE SAME EVERY TIME!

    assert(false) WILL CRASH THE PROGRAM IF YOU ATTEMPT TO PUT THIS OBJECT INTO A SET/DICT WITHOUT FIRST MODIFYING THE FUNCTION.
    THIS IS DONE ON PURPOSE TO PREVENT YOU FROM ACCIDENTALLY LEAKING NON-DETERMINISM INTO THE PROGRAM.
    SPEAK TO ME (TOM) AND I WILL EXPLAIN WHAT TO DO.
    """
    def __hash__(self):
        assert(False)

    def __init__(self, interaction_type, target_person_id):
        self.interaction_type = interaction_type
        self.target_person_id = target_person_id
        assert(target_person_id != -1)




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
        return [PrerequisitePersonInCell(self.target_person_id)]



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
        other_person = guiwindow.WORLD_INSTANCE.humanDict[self.target_person_id]
        if not self.interaction_type.participate(human, other_person):
            # print("%s refused to interact with %s in building: %s" % (other_person.id_number, human.id_number, human.current_building))
            return False
        if human.current_building != other_person.current_building:
            return False
        self.interaction_type.start_interaction(other_person)
        return True

    """
    This is called once when the action begins.
    """

    def begin(self, human):
        pass

    """
    Called every tick while the action has begun and not completed yet.
    Returns True/False to indicate if an error occurs.
    """

    def tick(self, human):
        return True

    """
    Returns true/false to indicate whether the action is complete or not.
    Called every tick before tick() is executed.    
    """

    def is_complete(self, human):
        return human.needs[NEED_TYPE.CURRENT_INTERACTION] != -1

    def __str__(self):
        return "Initiate interaction"
