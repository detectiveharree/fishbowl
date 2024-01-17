from ai.humanai.relationships.interaction.interaction import Interaction, INTERACTION_TYPE
from ai.humanai.relationships.information.informationinteraction.informationinteractionchat import InformationInteractionChat
from ai.humanai.relationships.interaction.interactionsocialise.interactionsocialise import InteractionSocialise
import numpy as np
from ai.humanai.relationships.interaction.interaction import FRUSTRATION_REASON
import logging

class InteractionChat(InteractionSocialise):

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
        MAX_DISTANCE = 20

        if distance > MAX_DISTANCE:
            return -1

        score = distance / MAX_DISTANCE
        score += 0.1 # just do it's not 0
        return 1

    """
    Return a number to indicate how bias they have to interact with a certain available person.
    Note: Should return number between 0 and 1.
    Note: returning -1 will prevent you from interaction with them whatsoever.
    Note: distance arg will be 0 if its a building interaction.
    Default: distance to the person.
    """
    def calculate_target_score(self, initiator, target_id):

        """
        Charisma has small multiplier
        Love and respect are highest multipliers, love has double weight of respect.
        If love below -0.2, this is unacceptable
        Distance taken into account too.
        """

        person_knowledge = initiator.knowledge_of_people.get_knowledge_of_person(target_id)
        love = initiator.knowledge_of_people.human_opinions.most_love_sorted[target_id]
        respect = initiator.knowledge_of_people.human_opinions.most_respect_sorted[target_id]
        agreeableness = person_knowledge.personality_attributes.agreeable.value
        gender = person_knowledge.gender


        # THIS WAS CAUSING MAJOR HATE ISSUES
        # SINCE PEOPLE WERE NEVER MENDING THEIR RELATIONSHIPS
        # PROBABLY BEST TO KEEP THIS OUT
        # if respect < 0:
        #     return -1

        agreeableness += 1
        agreeableness /= 2


        score = agreeableness * ((love + (respect * 2)) / 3)




        # flip score at this point so best is 0 worst is 1
        score *= -1
        score += 1

        # slightly higher chance to pick someone if they are same gender
        # over time this will get matter less and less
        if gender == initiator.body.gender:
            score *= 0.95


        return score


    """
    Calculate a pre-determined constant indicating how successful a interaction will be at start.
    Must return a number between -1 and 1
    """
    def calculate_success_constant(self):

        """
        Closer in carelessness and neurotism the better
        The higher average agreeableness the better

        The average neurotism increases randomness in conversation via normal std of above.
        Charisma has small weighting, will make chat a bit worst if avg charisma is bad.
        """

        careless1, careless2 = self.initiator.personality.carelessness.value, self.participant.personality.carelessness.value
        neuroticism1, neuroticism2 = self.initiator.personality.neuroticism.value, self.participant.personality.neuroticism.value
        agreeable1, agreeable2 = self.initiator.personality.agreeable.value, self.participant.personality.agreeable.value
        charisma1, charisma2 = self.initiator.personality.charisma.value, self.participant.personality.charisma.value


        # averaging social and carelessness of both people (individually)
        carelessneuroticism1 = (careless1 + neuroticism1) / 2
        carelessneuroticism2 = (careless2 + neuroticism2) / 2

        # finding our multiplier as the difference between above variables

        # https://stackoverflow.com/questions/16057627/re-scaling-the-values-between-given-maximum-and-minimum-where-max-is-positive-a
        # rescales value
        # we want personality attributes to have much smaller impact on success of convo
        def rescale(val, in_min, in_max, out_min, out_max):
            return out_min + (val - in_min) * ((out_max - out_min) / (in_max - in_min))

        carelessneuroticism_multiplier = 1 / (1 + abs(carelessneuroticism1 - carelessneuroticism2))
        carelessneuroticism_multiplier = rescale(carelessneuroticism_multiplier, 0.34, 1, 0.8, 1)

        avg_score = (agreeable1 + agreeable2 + charisma1 + charisma2) / 4 # average of agreeables
        avg_score += 1
        avg_score *= carelessneuroticism_multiplier
        avg_score -= 1



        # the variance i.e. the more neurotic the pair are the less predictable it will be
        average_neuroticism = (neuroticism1 + neuroticism2) / 2
        average_neuroticism += 1
        average_neuroticism /= 2
        average_neuroticism *= 0.3

        return round(np.clip(np.random.normal(avg_score, average_neuroticism), -1, 1), 2)

    """
    The public interaction information object that will be viewable to all
    as soon as the interaction begins.
    Created once when the interaction starts.
    Must return a InformationInteraction object.
    """
    def information_interaction_on_begin(self):
        return InformationInteractionChat(self.interaction_id, self.initiator.id_number, self.participant.id_number, self.success_constant)

    """
    The public interaction information object that will be viewable to all
    when the interaction ends.
    Created when the interaction ends.
    Must return a InformationInteraction object.
    """
    def information_interaction_on_end(self):
        return InformationInteractionChat(self.interaction_id, self.initiator.id_number, self.participant.id_number, self.success_constant)

    """
    Gets delta change in emotions for participants
    For socialise boredom, the emotion change is symmetric
    """
    def get_participants_tick_delta_emotions(self, human):
        # always decrease loneliness and fear no matter how bad interaction is
        human.emotions.loneliness.change(human, -5)
        human.emotions.fear.change(human, -5)

        happy_delta = 3 * self.success_constant
        frustration_delta = -5 * self.success_constant # blow off steam

        human.emotions.happiness.change(human, happy_delta)
        human.emotions.frustration.change(human, frustration_delta, FRUSTRATION_REASON.BAD_CHAT)


    """
    Return true/false to indicate whether the person would like to join the interaction.
    This is a static method therefore you cannot use self i.e. data cannot be accessed from this Interaction class
    """
    def participate(self, initiator, target):

        if not super().participate(initiator, target):
            return False

        # return target.knowledge_of_people.human_opinions.most_respect_sorted[initiator.id_number] >= 0
        return True

    """
    Returns the interaction type
    """
    def get_interaction_type(self):
        return INTERACTION_TYPE.CHAT



    def tick(self, interaction_participant):
        super().tick(interaction_participant)
        """
        Gets new information in convo
        """
        if len(self.active_participants) <= 1:
            return False

        interaction_participant.tick_emotions(self)

        return True

