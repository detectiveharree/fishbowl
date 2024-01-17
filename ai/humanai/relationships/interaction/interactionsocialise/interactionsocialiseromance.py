from ai.humanai.relationships.interaction.interaction import Interaction, INTERACTION_TYPE
from ai.humanai.relationships.interaction.interactionsocialise.interactionsocialise import InteractionSocialise
from ai.humanai.relationships.information.informationinteraction.informationinteractionromance import InformationInteractionRomance
import numpy as np
from ai.need import NEED_TYPE
import human
from humanbase import HumanState
import logging
from ai.humanai.relationships.interaction.interaction import FRUSTRATION_REASON
import bisect

class InteractionRomance(InteractionSocialise):

    """
    DO NOT DELETE THIS. PASTE THIS IN FOR EVERY NEW OBJECT THAT WILL BE STORED IN A SET/DICTIONARY.
    THIS IS ESSENTIAL FOR MAKING SURE THE PROGRAM PERFORMS EXACTLY THE SAME EVERY TIME!

    assert(false) WILL CRASH THE PROGRAM IF YOU ATTEMPT TO PUT THIS OBJECT INTO A SET/DICT WITHOUT FIRST MODIFYING THE FUNCTION.
    THIS IS DONE ON PURPOSE TO PREVENT YOU FROM ACCIDENTALLY LEAKING NON-DETERMINISM INTO THE PROGRAM.
    SPEAK TO ME (TOM) AND I WILL EXPLAIN WHAT TO DO.
    """
    def __hash__(self):
        assert(False)


    def __init__(self, initiator):
        super().__init__(initiator)


    """
    For cases when we are looking for person outside of a building.
    Returns a factor to multiply target score on based by their distance.
    Return -1 to indicate too far and skip this person.
    """
    def target_distance_score_factor(self, distance):
        # basically says distance doesn't matter
        return 1


    """
    Returns a id of a person to look for, for this current interaction.
    This method will be called multiple times as the person moves towards their target,
    so return new people as new information is observed.
    
    I.e. pick one person to talk, as they move they see another closer person.
    Choose to interact with the other person instead.
    
    Default: finds person with closest location to initiator.
    RETURN A LIST NOT A SET
    """
    def calculate_interaction_targets(self, initiator):
        """
        If has lover just return them
        """
        if initiator.knowledge_of_people.human_opinions.lover_id is not None:
            if initiator.knowledge_people_locations.knows_person_location(initiator.knowledge_of_people.human_opinions.lover_id):
                return [initiator.knowledge_of_people.human_opinions.lover_id]
            return []

        favorable_people = []

        for lover_id, score in initiator.knowledge_of_people.human_opinions.potential_lovers_sorted.items():

            # if doesn't know location skip
            if not initiator.knowledge_people_locations.knows_person_location(lover_id):
                continue

            # flip score and squeeze it between 0 and 1
            score += 1 # between 0 and 2
            score /= 2 # between 0 and 1
            score *= -1 # between 0 and -1
            score += 1 # between 1 and 0

            bias_score = score * self.calculate_target_score(initiator, lover_id)
            if bias_score > -1:
                bisect.insort(favorable_people, (bias_score, lover_id))

        return [person_id for bias_score, person_id in favorable_people]

    """
    Returns a id of a person to look for in the same building, for this current interaction.
    This method will be called multiple times as the person moves towards their target.
    Default: Returns random person in same building
    RETURN A LIST NOT A SET
    """
    def calculate_interaction_targets_in_building(self, initiator):
        """
        If has lover just return them
        """
        if initiator.knowledge_of_people.human_opinions.lover_id is not None:
            return [initiator.knowledge_of_people.human_opinions.lover_id]
        return super().calculate_interaction_targets(initiator)


    """
    Return a number to indicate how bias they have to interact with a certain available person.
    Note: Should return number between 0 and 1.
    Note: returning <= -1 will prevent them from interaction with the person whatsoever.
    Note: distance arg will be 0 if its a building interaction.
    Default: distance to the person.
    """
    def calculate_target_score(self, initiator, target_id):

        knowledge_of_person = initiator.knowledge_of_people.get_knowledge_of_person(target_id)

        age_difference_factor = 100 / (100 + abs(initiator.body.age - knowledge_of_person.age))
        age_difference_factor *= -1
        age_difference_factor += 1

        return age_difference_factor



    """
    Calculate a pre-determined constant indicating how successful a interaction will be at start.
    Must return a number between -1 and 1
    """
    def calculate_success_constant(self):

        """
        1. More closer the people are in socialness and carelessness the better.
        2. The higher the average charisma and agreeableness the better.

        The average neurotism increases randomness in conversation via normal std of above.
        """

        agreeable1, agreeable2 = self.initiator.personality.agreeable.value, self.participant.personality.agreeable.value
        charisma1, charisma2 = self.initiator.personality.charisma.value, self.participant.personality.charisma.value
        careless1, careless2 = self.initiator.personality.carelessness.value, self.participant.personality.carelessness.value
        social1, social2 = self.initiator.personality.social.value, self.participant.personality.social.value
        neuroticism1, neuroticism2 = self.initiator.personality.neuroticism.value, self.participant.personality.neuroticism.value

        # averaging agreeableness and charisma of both characters
        average_score = (agreeable1 + agreeable2 + charisma1 + charisma2) / 4
        # averaging social and carelessness of both people (individually)
        carelesssocial1 = (careless1 + social1) / 2
        carelesssocial2 = (careless2 + social2) / 2
        # finding our multiplier as the difference between above variables
        carelesssocial_multiplier = 1 / (1 + abs(carelesssocial1 - carelesssocial2))
        # logging.info(carelesssocial1)
        # logging.info(carelesssocial2)
        #
        # logging.info(carelesssocial_multiplier)

        # logging.info(average_score)


        # at this point, we need our average score to take values between 0 and 2, so += 1
        average_score += 1

        # since average_score takes values between 0 and 2, we can multiply it
        average_score *= carelesssocial_multiplier
        # finally, we want this value to be between -1 and 1, so -= 1
        average_score -= 1

        # the variance i.e. the more neurotic the pair are the less predictable it will be
        average_neuroticism = (neuroticism1 + neuroticism2) / 2
        average_neuroticism += 1
        average_neuroticism /= 2

        average_neuroticism /= 3 # way too much swing
        return round(np.clip(np.random.normal(average_score, average_neuroticism), -1, 1), 2)


    """
    If the person couldn't find anyone to interact with, execute this action to 
    go to a ActionInteractCellBuildingInteract variant that will cause the person to go interact
    there.
    Return None if you don't want the interaction to be done in a building
    """
    def interact_in_building_action(self):
        return None


    """
    The public interaction information object that will be viewable to all
    as soon as the interaction begins.
    Created once when the interaction starts.
    Must return a InformationInteraction object.
    """
    def information_interaction_on_begin(self):
        return InformationInteractionRomance(self.interaction_id, self.initiator.id_number, self.participant.id_number, self.success_constant)

    """
    The public interaction information object that will be viewable to all
    when the interaction ends.
    Created when the interaction ends.
    Must return a InformationInteraction object.
    """
    def information_interaction_on_end(self):
        return InformationInteractionRomance(self.interaction_id, self.initiator.id_number, self.participant.id_number, self.success_constant)


    """
    Gets delta change in emotions for participants
    For socialise boredom, the emotion change is symmetric
    """
    def get_participants_tick_delta_emotions(self, human):
        # always decrease loneliness and fear no matter how bad interaction is
        human.emotions.loneliness.change(human, -2)
        human.emotions.fear.change(human, -3)

        happy_delta = 10 * self.success_constant
        frustration_delta = -4 * self.success_constant # blow off steam

        human.emotions.happiness.change(human, happy_delta)
        human.emotions.frustration.change(human, frustration_delta, FRUSTRATION_REASON.BAD_ROMANCE)

    """
    Returns the interaction type
    """
    def get_interaction_type(self):
        return INTERACTION_TYPE.ROMANCE


    """
    Called when the interaction begins
    i.e. other participant accepts
    """
    def begin_interaction(self, participant1, participant2):
        self.create_public_information(InformationInteractionRomance(participant1.id_number, participant2.id_number))


    """
    Return true/false to indicate whether the person would like to join the interaction.
    This is a static method therefore you cannot use self i.e. data cannot be accessed from this Interaction class
    """
    def participate(self, initiator, target):


        if not super().participate(initiator, target):
            return False

        """
        If has lover only accept if other person is their love
        """
        if target.knowledge_of_people.human_opinions.lover_id is not None:
            return target.knowledge_of_people.human_opinions.lover_id == initiator.id_number

        # only say yes if its their potential best lover
        return initiator.id_number in target.knowledge_of_people.human_opinions.potential_lovers_sorted


    def tick(self, interaction_participant):
        super().tick(interaction_participant)
        """
        Gets new information in convo
        """
        if len(self.active_participants) <= 1:
            return False

        interaction_participant.tick_emotions(self)

        return True

