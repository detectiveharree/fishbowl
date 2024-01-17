from ai.humanai.relationships.interaction.interaction import Interaction, INTERACTION_TYPE
from ai.humanai.relationships.information.informationinteraction.informationinteractioninsult import InformationInteractionInsult
from ai.humanai.actions.actioninteractcellsocialisingtavern import ActionInteractCellSocialisingTavern
from ai.need import NEED_TYPE
import human
from ai.humanai.relationships.interaction.interactionsocialise.interactionsocialise import InteractionSocialise
import numpy as np
from humanbase import HumanState
from ai.humanai.relationships.interaction.interaction import ANGER_REASON
from ai.humanai.relationships.interaction.interaction import FRUSTRATION_REASON

class InteractionInsult(InteractionSocialise):

    """
    DO NOT DELETE THIS. PASTE THIS IN FOR EVERY NEW OBJECT THAT WILL BE STORED IN A SET/DICTIONARY.
    THIS IS ESSENTIAL FOR MAKING SURE THE PROGRAM PERFORMS EXACTLY THE SAME EVERY TIME!

    assert(false) WILL CRASH THE PROGRAM IF YOU ATTEMPT TO PUT THIS OBJECT INTO A SET/DICT WITHOUT FIRST MODIFYING THE FUNCTION.
    THIS IS DONE ON PURPOSE TO PREVENT YOU FROM ACCIDENTALLY LEAKING NON-DETERMINISM INTO THE PROGRAM.
    SPEAK TO ME (TOM) AND I WILL EXPLAIN WHAT TO DO.
    """
    def __hash__(self):
        assert(False)

    def __init__(self, initiator, insult_reason):
        super().__init__(initiator)
        self.insult_reason = insult_reason


    """
    For cases when we are looking for person outside of a building.
    Returns a factor to multiply target score on based by their distance.
    Return -1 to indicate too far and skip this person.
    """
    def target_distance_score_factor(self, distance):
        MAX_DISTANCE = 10

        if distance > MAX_DISTANCE:
            return -1

        score = distance / MAX_DISTANCE
        score += 0.1 # just do it's not 0
        return score

    """
    Return a number to indicate how bias they have to interact with a certain available person.
    Note: Should return number between 0 and 1.
    Note: returning -1 will prevent you from interaction with them whatsoever.
    Note: distance arg will be 0 if its a building interaction.
    Default: distance to the person.
    """
    def calculate_target_score(self, initiator, target_id):

        """
        Short distance is essential.
        Least love the more likely.
        The least respect the more likely (but lesser extent then love)
        Fear makes it less likely (however this is dampened by carelessness)
        """

        person_knowledge = initiator.knowledge_of_people.get_knowledge_of_person(target_id)
        love =  initiator.knowledge_of_people.human_opinions.most_love_sorted[target_id]
        respect =  initiator.knowledge_of_people.human_opinions.most_respect_sorted[target_id]
        fear = initiator.knowledge_of_people.human_opinions.most_fear_sorted[target_id]
        carelessness = initiator.personality_attributes.carelessness.value

        love *= -1
        love += 1
        love /= 2

        respect *= -1
        respect += 1
        respect /= 2

        fear *= -1
        fear += 1
        fear /= 2

        carelessness += 1
        carelessness /= 2

        loverespect = ((love * 2) + respect) / 3

        score = np.clip(np.random.normal(fear, carelessness / 3), 0, 1) * loverespect

        score *= -1
        score += 1
        return score


    """
    Calculate a pre-determined constant indicating how successful a interaction will be at start.
    Must return a number between -1 and 1
    """
    def calculate_success_constant(self):

        """
        Emotions
        The more angry of initator (0 to 100) the higher success
        The more fear of initator (0 to 100), the less success
        Higher AgreeablenessAttribute of initator (-1 to 1), the less success

        The higher fear of participant (0-100) the more success
        The more charisma of participant (-1 to 1) the less success
        """

        agreeable1 =  self.initiator.personality.agreeable.value
        charisma2 = self.participant.personality.charisma.value
        fear1 = self.initiator.emotions.fear.value.get()
        frustration1 = self.initiator.emotions.frustration.value.get()

        fear1 *= -1
        fear1 += 100

        charisma2 -= 1
        charisma2 *= -1
        charisma2 /= 2

        fearfrustration = (((2 * frustration1) + (fear1)) / 3) / 100

        agreeable1 -= 1
        agreeable1 /= 2
        agreeable1 *= -1

        charismaagreeable = ((agreeable1 * 4) + charisma2) / 5

        total_score = fearfrustration * charismaagreeable
        total_score -= 0.5
        total_score *= 2


        return round(total_score, 2)



    """
    Return true/false to indicate whether the person would like to join the interaction.
    This is a static method therefore you cannot use self i.e. data cannot be accessed from this Interaction class
    """
    def to_string(self):
        if len(self.active_participants) <= 1:
            return "%s looking for participant (%s) in building %s because %s" % (self.initiator.id_number, self.get_interaction_type(), self.initiator.current_building, self.insult_reason)
        return "%s interacting with %s (%s) (%s) in building %s because %s" % (self.initiator.id_number,
                                                               self.participant.id_number,
                                                                self.get_interaction_type(),
                                                                self.success_constant,
                                                               self.initiator.current_building, self.insult_reason)

    """
    The public interaction information object that will be viewable to all
    as soon as the interaction begins.
    Created once when the interaction starts.
    Must return a InformationInteraction object.
    """
    def information_interaction_on_begin(self):
        return InformationInteractionInsult(self.interaction_id, self.initiator.id_number, self.participant.id_number, self.success_constant)

    """
    The public interaction information object that will be viewable to all
    when the interaction ends.
    Created when the interaction ends.
    Must return a InformationInteraction object.
    """
    def information_interaction_on_end(self):
        return InformationInteractionInsult(self.interaction_id, self.initiator.id_number, self.participant.id_number, self.success_constant)


    """
    If the person couldn't find anyone to interact with, execute this action to 
    go to a ActionInteractCellBuildingInteract variant that will cause the person to go interact
    there.
    Return None if you don't want the interaction to be done in a building
    """
    def interact_in_building_action(self):
        return ActionInteractCellSocialisingTavern(self)

    """
    Gets delta change in initator emotions per tick
    NOTE Called only for one tick.
    """
    def get_initator_tick_delta_emotions(self, human):

        """
        We want to create a new success constant for initator for situations
        where the insult doesn't land.
        Where it doesn't land we want him to become more frustrated + angry
        """

        frust_delta = -80
        anger_delta = -60

        constant = np.clip(self.success_constant + 1, 0, 1)
        human.emotions.frustration.change(human, frust_delta, FRUSTRATION_REASON.GOT_COUNTER_INSULTED)
        human.emotions.anger.change(human, anger_delta * constant, (self.participant.id_number, ANGER_REASON.GOT_COUNTER_INSULTED))


    """
    Gets delta change in participant emotions per tick
    NOTE Called only for one tick.
    """
    def get_participant_tick_delta_emotions(self, human):

        frust_delta = 80
        anger_delta = 70
        constant = np.clip(self.success_constant + 1, 0, 1)

        human.emotions.frustration.change(human, frust_delta * constant, FRUSTRATION_REASON.GOT_INSULTED)
        human.emotions.anger.change(human, anger_delta * constant, (self.initiator.id_number, ANGER_REASON.GOT_INSULTED))


    """
    Return true/false to indicate whether the person would like to join the interaction.
    This is a static method therefore you cannot use self i.e. data cannot be accessed from this Interaction class
    """
    def participate(self, initiator, target):
        """
        Partcipate if we want to socialise and not currently interacting.
        Note: current_highest_need isn't updated till next tick, therefore
        technically the person's highest need will not become current interaction,
        therefore we also do one additional check on their needs.
        """
        return target.needs[NEED_TYPE.CURRENT_INTERACTION].need_level == -1 and \
               target.state == HumanState.AWAKE

    """
    Return the need level the person will have CURRENT_INTERACTION set to
    """
    def get_need_level(self, human):
        if human.current_highest_need.need_type == NEED_TYPE.FRUSTRATION:
            return human.needs[NEED_TYPE.FRUSTRATION].need_level + human.needs[NEED_TYPE.FRUSTRATION].minimum_level_for_switch()
        elif human.current_highest_need.need_type == NEED_TYPE.ANGER:
            return human.needs[NEED_TYPE.ANGER].need_level + human.needs[NEED_TYPE.ANGER].minimum_level_for_switch()
        # else if you're getting insulted just flick to 10000
        return 10000

    """
    Returns the interaction type
    """
    def get_interaction_type(self):
        return INTERACTION_TYPE.INSULT



    def tick(self, person):
        """
        Gets new information in convo
        """
        if len(self.active_participants) <= 1:
            return False

        self.get_initator_tick_delta_emotions(self.initiator)
        self.get_participant_tick_delta_emotions(self.participant)

        return False

