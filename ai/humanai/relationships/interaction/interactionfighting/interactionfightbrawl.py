from ai.humanai.relationships.interaction.interactionfighting.interactionfight import InteractionFight
from ai.humanai.relationships.information.informationinteraction.informationinteractionfightbrawl import InformationInteractionFightBrawl
from ai.humanai.relationships.interaction.interaction import INTERACTION_TYPE
import numpy as np
from enum import Enum



class InteractionFightBrawl(InteractionFight):

    """
    DO NOT DELETE THIS. PASTE THIS IN FOR EVERY NEW OBJECT THAT WILL BE STORED IN A SET/DICTIONARY.
    THIS IS ESSENTIAL FOR MAKING SURE THE PROGRAM PERFORMS EXACTLY THE SAME EVERY TIME!

    assert(false) WILL CRASH THE PROGRAM IF YOU ATTEMPT TO PUT THIS OBJECT INTO A SET/DICT WITHOUT FIRST MODIFYING THE FUNCTION.
    THIS IS DONE ON PURPOSE TO PREVENT YOU FROM ACCIDENTALLY LEAKING NON-DETERMINISM INTO THE PROGRAM.
    SPEAK TO ME (TOM) AND I WILL EXPLAIN WHAT TO DO.
    """
    def __hash__(self):
        assert(False)



    def __init__(self, initiator, unarmed, damage_requirement, brawl_reason):
        super().__init__(initiator, unarmed, damage_requirement)
        self.brawl_reason = brawl_reason


    """
    Returns the interaction type
    """
    def get_interaction_type(self):
        return INTERACTION_TYPE.FIGHT_BRAWL


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
    The public interaction information object that will be viewable to all
    as soon as the interaction begins.
    Created once when the interaction starts.
    Must return a InformationInteraction object.
    """
    def information_interaction_on_begin(self):
        return InformationInteractionFightBrawl(self.interaction_id, self.initiator.id_number, self.participant.id_number,
                                           self)

    """
    The public interaction information object that will be viewable to all
    when the interaction ends.
    Created when the interaction ends.
    Must return a InformationInteraction object.
    """
    def information_interaction_on_end(self):
        return InformationInteractionFightBrawl(self.interaction_id, self.initiator.id_number, self.participant.id_number,
                                           self)


    """
    Return true/false to indicate whether the person would like to join the interaction.
    This is a static method therefore you cannot use self i.e. data cannot be accessed from this Interaction class
    """
    def to_string(self):
        if len(self.active_participants) <= 1:
            return "%s looking for participant (%s) in building %s because %s" % (self.initiator.id_number, self.get_interaction_type(), self.initiator.current_building, self.brawl_reason)
        return "%s (%s) interacting with %s (%s) (%s) in building %s because %s" % (self.initiator.id_number, self.initiator.body.gender,
                                                               self.participant.id_number, self.participant.body.gender,
                                                                self.get_interaction_type(),
                                                               self.initiator.current_building, self.brawl_reason)



    """
    Return a number to indicate how bias they have to interact with a certain available person.
    Note: Should return number between 0 and 1.
    Note: returning -1 will prevent you from interaction with them whatsoever.
    Note: distance arg will be 0 if its a building interaction.
    Default: distance to the person.
    """
    def calculate_target_score(self, initiator, target_id):

        """
        Agreeable advantage preference
        Less love the better
        Noise by carelessness.
        """

        initator_carelessness = initiator.personality.carelessness.value

        person_knowledge = initiator.knowledge_of_people.get_knowledge_of_person(target_id)
        participant_health = person_knowledge.health
        love = initiator.knowledge_of_people.human_opinions.most_love_sorted[target_id]

        if participant_health <= self.damage_requirement:
            return -1

        preference = 1

        # the less love, the more preference
        love += 1
        love /= 2
        preference *= love

        # used as noise
        initator_carelessness += 1
        initator_carelessness /= 2

        return np.clip(np.random.normal(preference, initator_carelessness), 0, 1)

