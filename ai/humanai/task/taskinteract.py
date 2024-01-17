from ai import task
import global_params
from ai.humanai.actions.actioninteractperson import ActionInteractPerson
from ai.need import NEED_TYPE
from ai.humanai.relationships.interaction.interaction import INTERACTION_TYPE


class TaskInteract(task.Task):

    """
    DO NOT DELETE THIS. PASTE THIS IN FOR EVERY NEW OBJECT THAT WILL BE STORED IN A SET/DICTIONARY.
    THIS IS ESSENTIAL FOR MAKING SURE THE PROGRAM PERFORMS EXACTLY THE SAME EVERY TIME!

    assert(false) WILL CRASH THE PROGRAM IF YOU ATTEMPT TO PUT THIS OBJECT INTO A SET/DICT WITHOUT FIRST MODIFYING THE FUNCTION.
    THIS IS DONE ON PURPOSE TO PREVENT YOU FROM ACCIDENTALLY LEAKING NON-DETERMINISM INTO THE PROGRAM.
    SPEAK TO ME (TOM) AND I WILL EXPLAIN WHAT TO DO.
    """
    def __hash__(self):
        assert(False)

    def __init__(self, human, interaction_type):
        self.interaction_participant = interaction_type.get_interaction_participant(human)
        self.interaction_type = interaction_type

    """
    NOTE: This will never get fired because the CURRENT_INTERACTION need is set to 10000
    which will almost always be higher. Redo this.
    """
    def terminate_task_early(self, human):
        human_highest_need = human.current_highest_need.need_type
        return human_highest_need == NEED_TYPE.GROUP_TASK or\
               human_highest_need == NEED_TYPE.HUNGER or\
               human_highest_need == NEED_TYPE.THIRST or\
               human_highest_need == NEED_TYPE.SLEEP or \
               human_highest_need == NEED_TYPE.BETTER_SLEEPING_LOCATION or \
               (human_highest_need == NEED_TYPE.FRUSTRATION and
                self.interaction_type.get_interaction_type() != INTERACTION_TYPE.FIGHT_BRAWL and
                self.interaction_type.get_interaction_type() != INTERACTION_TYPE.FIGHT_BATTLE and
                self.interaction_type.get_interaction_type() != INTERACTION_TYPE.INSULT) or \
               (human_highest_need == NEED_TYPE.ANGER and
                self.interaction_type.get_interaction_type() != INTERACTION_TYPE.FIGHT_BRAWL and
                self.interaction_type.get_interaction_type() != INTERACTION_TYPE.FIGHT_BATTLE and
                self.interaction_type.get_interaction_type() != INTERACTION_TYPE.INSULT) or \
               human_highest_need == NEED_TYPE.NONE
    """
    Possible actions that the user can do to satisfy this pre requisite.
    Note the action with the cheapest action tree will be picked.
    """
    def possible_actions(self):
        return [ActionInteractPerson(self.interaction_participant, self.interaction_type)]

    """
    Called when the action tree is completed.
    Returns True/False. If true, task will terminate, else the task will be restarted via begin()
    Default: returns true
    """
    def is_task_complete(self, human):
        return True


    def action_failed_response(self, human):
        """
        Technically the only action ActionInteractPerson will fail when the interaction tick returns false.
        I.e. usually when the other person leaves the interaction
        """
        return []


    def __repr__(self):
        return str("Interact (%s)" % self.interaction_type.get_interaction_type())