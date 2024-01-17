from ai.humanai.relationships.interaction.interaction import Interaction, INTERACTION_TYPE
from ai.need import NEED_TYPE
from ai.humanai.relationships.interaction.interactionparticipant import InteractionParticipant
from ai.humanai.relationships.information.informationinteraction.informationinteractionbanter import InformationInteractionBanter

import human
from ai.humanai.relationships.interaction.interactionsocialise.interactionsocialise import InteractionSocialise
import numpy as np
from humanbase import HumanState
from ai.humanai.relationships.interaction.interaction import FRUSTRATION_REASON



class InteractionBanter(InteractionSocialise):

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
        MAX_DISTANCE = 10

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
        Charisma is main multiplier
        Love and respect are main multipliers, love has double weight of respect.
        If love below -0.5, this is unacceptable
        Distance taken into account too.
        Better if same gender = 0.7
        """

        person_knowledge = initiator.knowledge_of_people.get_knowledge_of_person(target_id)
        love =  initiator.knowledge_of_people.human_opinions.most_love_sorted[target_id]
        respect = initiator.knowledge_of_people.human_opinions.most_respect_sorted[target_id]
        charisma = person_knowledge.personality_attributes.charisma.value
        gender = person_knowledge.gender


        # THIS WAS CAUSING MAJOR HATE ISSUES
        # SINCE PEOPLE WERE NEVER MENDING THEIR RELATIONSHIPS
        # PROBABLY BEST TO KEEP THIS OUT
        # if love < 0:
        #     return -1

        charisma += 1
        charisma /= 2


        score = charisma * (((love * 2) + respect) / 3)

        # flip score at this point so best is 0 worst is 1
        score *= -1
        score += 1

        # higher chance to pick someone if they are same gender
        if gender == initiator.body.gender:
            score *= 0.85


        return score



    """
    Calculate a pre-determined constant indicating how successful a interaction will be at start.
    Must return a number between -1 and 1
    """
    def calculate_success_constant(self):

        """
        Higher average charisma and socialness will yield a better score
        Higher neuroticism the better.
        """
        charisma1, charisma2 = self.initiator.personality.charisma.value, self.participant.personality.charisma.value
        social1, social2 = self.initiator.personality.social.value, self.participant.personality.social.value
        neuroticism1, neuroticism2 = self.initiator.personality.neuroticism.value, self.participant.personality.neuroticism.value
        carelessness1, carelessness2 = self.initiator.personality.carelessness.value, self.participant.personality.carelessness.value
        carelessnessaverage = (carelessness1 + carelessness2) / 2

        socialcharisma = (charisma1 +  charisma2 + social1 + social2) / 4
        socialcharisma += (carelessnessaverage / 4)  # slight carelessness effect i.e. avg carelessness of -1 = -0.25 difference in succ

        # the variance i.e. the more neurotic the pair are the less predictable it will be
        average_neuroticism = (neuroticism1 + neuroticism2) / 2
        average_neuroticism += 1
        average_neuroticism /= 2
        average_neuroticism *= 0.2


        # self.social = SocialAttribute(social) # higher socialness (>0) the better
        # self.carelessness = CarelessnessAttribute(carelessness) # higher carelessness the better
        # self.charisma = CharismaAttribute(charisma) # higher charisma the better
        return round(np.clip(np.random.normal(socialcharisma, average_neuroticism), -1, 1), 2)


    """
    The public interaction information object that will be viewable to all
    as soon as the interaction begins.
    Created once when the interaction starts.
    Must return a InformationInteraction object.
    """
    def information_interaction_on_begin(self):
        return InformationInteractionBanter(self.interaction_id, self.initiator.id_number, self.participant.id_number, self.success_constant)

    """
    The public interaction information object that will be viewable to all
    when the interaction ends.
    Created when the interaction ends.
    Must return a InformationInteraction object.
    """
    def information_interaction_on_end(self):
        return InformationInteractionBanter(self.interaction_id, self.initiator.id_number, self.participant.id_number, self.success_constant)

    """
    Gets delta change in emotions for participants
    For socialise boredom, the emotion change is symmetric
    """
    def get_participants_tick_delta_emotions(self, human):
        # always decrease loneliness and fear no matter how bad interaction is
        human.emotions.loneliness.change(human, -3)
        human.emotions.fear.change(human, -5)

        happy_delta = 5 * self.success_constant
        frustration_delta = -4 * self.success_constant # blow off steam

        human.emotions.happiness.change(human, happy_delta)
        human.emotions.frustration.change(human, frustration_delta, FRUSTRATION_REASON.BAD_BANTER)


    """
    Return true/false to indicate whether the person would like to join the interaction.
    This is a static method therefore you cannot use self i.e. data cannot be accessed from this Interaction class
    """
    def participate(self, initiator, target):

        if not super().participate(initiator, target):
            return False

        return True
        # return target.knowledge_of_people.human_opinions.most_love_sorted[initiator.id_number] >= 0

    """
    Returns the interaction type
    """
    def get_interaction_type(self):
        return INTERACTION_TYPE.BANTER



    def tick(self, interaction_participant):
        super().tick(interaction_participant)
        """
        Gets new information in convo
        """
        if len(self.active_participants) <= 1:
            return False
        # interaction_participant.human.needs[NEED_TYPE.CURRENT_INTERACTION].need_level = interaction_participant.human.needs[NEED_TYPE.BOREDOM].need_level

        interaction_participant.tick_emotions(self)

        return True

