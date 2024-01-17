from ai.humanai.relationships.interaction.interactionfighting.interactionfight import InteractionFight
from ai import pathfinding
import bisect
from ai.humanai.relationships.interaction.interaction import INTERACTION_TYPE
from ai.humanai.relationships.information.informationinteraction.informationinteractionfightbattle import InformationInteractionFightBattle
import numpy as np

class InteractionFightBattle(InteractionFight):

    """
    DO NOT DELETE THIS. PASTE THIS IN FOR EVERY NEW OBJECT THAT WILL BE STORED IN A SET/DICTIONARY.
    THIS IS ESSENTIAL FOR MAKING SURE THE PROGRAM PERFORMS EXACTLY THE SAME EVERY TIME!

    assert(false) WILL CRASH THE PROGRAM IF YOU ATTEMPT TO PUT THIS OBJECT INTO A SET/DICT WITHOUT FIRST MODIFYING THE FUNCTION.
    THIS IS DONE ON PURPOSE TO PREVENT YOU FROM ACCIDENTALLY LEAKING NON-DETERMINISM INTO THE PROGRAM.
    SPEAK TO ME (TOM) AND I WILL EXPLAIN WHAT TO DO.
    """
    def __hash__(self):
        assert(False)

    """
    The public interaction information object that will be viewable to all
    as soon as the interaction begins.
    Created once when the interaction starts.
    Must return a InformationInteraction object.
    """
    def information_interaction_on_begin(self):
        return InformationInteractionFightBattle(self.interaction_id, self.initiator.id_number, self.participant.id_number,
                                           self)

    """
    The public interaction information object that will be viewable to all
    when the interaction ends.
    Created when the interaction ends.
    Must return a InformationInteraction object.
    """
    def information_interaction_on_end(self):
        return InformationInteractionFightBattle(self.interaction_id, self.initiator.id_number, self.participant.id_number,
                                           self)


    def __init__(self, initiator, damage_requirement, enemy_group):
        super().__init__(initiator, False, damage_requirement)
        self.enemy_group = enemy_group



    """
    Returns the interaction type
    """
    def get_interaction_type(self):
        return INTERACTION_TYPE.FIGHT_BATTLE


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

        preference = self.get_agreeable_advantage_preference(initiator, target_id)

        # the less love, the more preference
        love += 1
        love /= 2
        preference *= love

        # used as noise
        initator_carelessness += 1
        initator_carelessness /= 2

        return np.clip(np.random.normal(preference, initator_carelessness), 0, 1)


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
        Equivalent to normal calculation except makes sure it's
        only for participants in the battle.
        """

        favorable_people = []  # [(score, person)]

        for person in self.enemy_group.members:
            person_id = person.id_number
            believed_location = initiator.knowledge_of_people.get_knowledge_of_person(person_id).location
            if believed_location is None:
                continue
            # do distance calculations in bulk as a optimisation
            distance = pathfinding.get_euclidean_distance(initiator.location, believed_location)
            # add in inserted order, into the list of people with their id
            distance_factor = self.target_distance_score_factor(distance)

            if distance_factor == -1:
                continue

            bias_score = self.calculate_target_score(initiator, person_id) * distance_factor
            if bias_score > -1:
                bisect.insort(favorable_people, (bias_score, person_id))

        return [person_id for bias_score, person_id in reversed(favorable_people)]

