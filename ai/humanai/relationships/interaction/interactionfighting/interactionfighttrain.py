from ai.humanai.relationships.interaction.interactionfighting.interactionfight import InteractionFight
from ai.humanai.actions.actioninteractcellfightingarenatrain import ActionInteractCellFightingArenaTrain
from ai.humanai.relationships.interaction.interaction import INTERACTION_TYPE
import numpy as np
from ai.humanai.relationships.information.informationinteraction.informationinteractionfighttrain import InformationInteractionFightTrain




class InteractionFightTrain(InteractionFight):

    """
    DO NOT DELETE THIS. PASTE THIS IN FOR EVERY NEW OBJECT THAT WILL BE STORED IN A SET/DICTIONARY.
    THIS IS ESSENTIAL FOR MAKING SURE THE PROGRAM PERFORMS EXACTLY THE SAME EVERY TIME!

    assert(false) WILL CRASH THE PROGRAM IF YOU ATTEMPT TO PUT THIS OBJECT INTO A SET/DICT WITHOUT FIRST MODIFYING THE FUNCTION.
    THIS IS DONE ON PURPOSE TO PREVENT YOU FROM ACCIDENTALLY LEAKING NON-DETERMINISM INTO THE PROGRAM.
    SPEAK TO ME (TOM) AND I WILL EXPLAIN WHAT TO DO.
    """
    def __hash__(self):
        assert(False)



    def __init__(self, initiator, damage_requirement):
        super().__init__(initiator, False, damage_requirement)


    """
    If the person couldn't find anyone to interact with, execute this action to 
    go to a ActionInteractCellBuildingInteract variant that will cause the person to go interact
    there.
    Return None if you don't want the interaction to be done in a building
    """
    def interact_in_building_action(self):
        return ActionInteractCellFightingArenaTrain(self)

    """
    Returns the interaction type
    """
    def get_interaction_type(self):
        return INTERACTION_TYPE.FIGHT_TRAINING

    """
    The public interaction information object that will be viewable to all
    as soon as the interaction begins.
    Created once when the interaction starts.
    Must return a InformationInteraction object.
    """
    def information_interaction_on_begin(self):
        return InformationInteractionFightTrain(self.interaction_id, self.initiator.id_number, self.participant.id_number,
                                           self)

    """
    The public interaction information object that will be viewable to all
    when the interaction ends.
    Created when the interaction ends.
    Must return a InformationInteraction object.
    """
    def information_interaction_on_end(self):
        return InformationInteractionFightTrain(self.interaction_id, self.initiator.id_number, self.participant.id_number,
                                           self)


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
        More love the better
        Noise by a bit of carelessness.
        """

        initator_carelessness = initiator.personality.carelessness.value

        person_knowledge = initiator.knowledge_of_people.get_knowledge_of_person(target_id)
        participant_health = person_knowledge.health
        love =  initiator.knowledge_of_people.human_opinions.most_love_sorted[target_id]
        gender =  person_knowledge.gender

        if participant_health <= self.damage_requirement:
            return -1

        preference = self.get_agreeable_advantage_preference(initiator, target_id)

        # the more love, the more preference
        love += 1
        love /= 2
        love *= -1 # flip it
        love += 1
        preference *= love

        # used as noise
        initator_carelessness += 1
        initator_carelessness /= 2

        # higher chance to pick someone if they are same gender
        if gender == initiator.body.gender:
            preference *= 0.85

        return np.clip(np.random.normal(preference, initator_carelessness / 3), 0, 1)

    """
    For cases when we are looking for person outside of a building.
    Returns a factor to multiply target score on based by their distance.
    Return -1 to indicate too far and skip this person.
    """
    def target_distance_score_factor(self, distance):
        MAX_DISTANCE = 50

        if distance > MAX_DISTANCE:
            return -1

        score = distance / MAX_DISTANCE
        score += 0.1 # just do it's not 0
        return score


