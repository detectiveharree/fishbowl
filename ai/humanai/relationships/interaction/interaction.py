from abc import ABC, abstractmethod
from gameworld.timestamp import TimeStamp
from ai.need import NEED_TYPE
from ai.humanai.relationships.interaction.interactionparticipant import InteractionParticipantInitator, InteractionParticipantParticipant
import random
import guiwindow
from enum import Enum
import logging
import bisect
from ai import pathfinding

class INTERACTION_TYPE(Enum):
    ROMANCE = 2
    CHAT = 3
    INSULT = 4
    BANTER = 5
    FIGHT_BATTLE = 6
    FIGHT_BRAWL = 7
    FIGHT_TRAINING = 8

    def __str__(self):
        return self.name

    def __repr__(self):
        return str(self)

class ANGER_REASON(Enum):
    FRUSTRATION = 0
    GOT_INSULTED = 1
    GOT_COUNTER_INSULTED = 2
    FOUGHT_FRIEND = 3
    JEALOUS_ROMANCE = 5

    def __str__(self):
        return "ANGRY %s" % self.name

    def __repr__(self):
        return str(self)

class FRUSTRATION_REASON(Enum):
    BAD_CHAT = 0
    BAD_BANTER = 1
    BAD_ROMANCE = 2
    GOT_INSULTED = 3
    GOT_COUNTER_INSULTED = 4
    TOOK_HIT_FIGHT = 5


    def __str__(self):
        return "FRUSTRATED %s" % self.name

    def __repr__(self):
        return str(self)



"""
A wrapper for the information to prevent it from being registered multiple times
"""
class PublicInformation():

    """
    DO NOT DELETE THIS. PASTE THIS IN FOR EVERY NEW OBJECT THAT WILL BE STORED IN A SET/DICTIONARY.
    THIS IS ESSENTIAL FOR MAKING SURE THE PROGRAM PERFORMS EXACTLY THE SAME EVERY TIME!

    assert(false) WILL CRASH THE PROGRAM IF YOU ATTEMPT TO PUT THIS OBJECT INTO A SET/DICT WITHOUT FIRST MODIFYING THE FUNCTION.
    THIS IS DONE ON PURPOSE TO PREVENT YOU FROM ACCIDENTALLY LEAKING NON-DETERMINISM INTO THE PROGRAM.
    SPEAK TO ME (TOM) AND I WILL EXPLAIN WHAT TO DO.
    """
    def __hash__(self):
        return hash(self.hash_id)

    def __eq__(self, other):
        return self.__class__ == other.__class__ and self.hash_id == other.hash_id

    def __init__(self, info):
        self.hash_id = guiwindow.WORLD_INSTANCE.public_info_id_counter
        guiwindow.WORLD_INSTANCE.public_info_id_counter += 1
        self.seen_by = set()
        self.info = info
        pass

    def register_to_human(self, human):
        if human.id_number not in self.seen_by:
            self.info.register_to_knowledge(human)
            self.seen_by.add(human.id_number)


"""
Interacton class is primilarly concerned with the transfer of:
Information e.g.
Physical contact
"""
class Interaction(ABC):

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
        self.interaction_id = guiwindow.WORLD_INSTANCE.interaction_id_counter
        guiwindow.WORLD_INSTANCE.interaction_id_counter += 1

        self.initiator = initiator
        self.participant = None

        self.active_participants = {}
        self.public_information = set()
        """
        Piece of public information viewable at all at all times:
        Will be assigned when interaction starts.
        Will be reassigned when interaction finishes.
        """
        self.information_interaction = None
        self.beginning_time = None

    """
    Returns the interaction type
    """
    @abstractmethod
    def get_interaction_type(self):
        ...

    """
    Information exchanged only between participants
    """
    def create_private_information(self, info, to_participant):
        to_participant.private_info.add(info)

    """
    Information available to everyone who witnesses the interaction
    """
    def create_public_information(self, info):
        self.public_information.add(PublicInformation(info))


    """
    Registers all public information associated with this interaction
    POTENTIALLY optimise this function by adding lru cache with size of public information as parameter
    """
    def witness_interaction_public_information(self, human):
        for publicinfo in self.public_information:
            publicinfo.register_to_human(human)
        self.information_interaction.register_to_human(human)


    """
    The public interaction information object that will be viewable to all
    as soon as the interaction begins.
    Created once when the interaction starts.
    Must return a InformationInteraction object.
    """
    @abstractmethod
    def information_interaction_on_begin(self):
        ...

    """
    The public interaction information object that will be viewable to all
    when the interaction ends.
    Created when the interaction ends.
    Must return a InformationInteraction object.
    """
    @abstractmethod
    def information_interaction_on_end(self):
        ...


    """
    Gets delta change in initator emotions per tick
    """
    @abstractmethod
    def get_initator_tick_delta_emotions(self, human):
        ...

    """
    Gets delta change in participant emotions per tick
    """
    @abstractmethod
    def get_participant_tick_delta_emotions(self, human):
        ...

    """
    Return the need level the person will have CURRENT_INTERACTION set to
    """
    def get_need_level(self, human):
        return 10000

    """
    If the person couldn't find anyone to interact with, execute this action to 
    go to a ActionInteractCellBuildingInteract variant that will cause the person to go interact
    there.
    Return None if you don't want the interaction to be done in a building
    """
    def interact_in_building_action(self):
        return None


    """
    Used when a interaction is starting
    """
    def start_interaction(self, participant):

        self.participant = participant

        interaction_participant_1 = InteractionParticipantInitator(self.initiator)
        interaction_participant_2 = InteractionParticipantParticipant(participant)

        interaction_participant_1.other_participant = interaction_participant_2
        interaction_participant_2.other_participant = interaction_participant_1

        self.active_participants[self.initiator.id_number] = interaction_participant_1
        self.active_participants[participant.id_number] = interaction_participant_2

        self.information_interaction = PublicInformation(self.information_interaction_on_begin())
        self.initiator.needs[NEED_TYPE.CURRENT_INTERACTION].start_interaction(self, self.get_need_level(self.initiator))
        self.participant.needs[NEED_TYPE.CURRENT_INTERACTION].start_interaction(self, self.get_need_level(self.participant))

    """
    We don't deal with humans in the tick function,
    instead we deal with InteractionParticipant objects.
    It contains the human, but also extra helper information
    that might be relevant for the current interaction. 
    """
    def get_interaction_participant(self, human):
        return self.active_participants[human.id_number]

    """
    Returns true if a human is involved in this current interaction
    """
    def human_in_interaction(self, human):
        return human.id_number in self.active_participants.keys()

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

        favorable_people = [] # [(score, person)]

        for location in initiator.knowledge_people_locations.last_known_people_locations.keys():
            # do distance calculations in bulk as a optimisation
            distance = pathfinding.get_euclidean_distance(initiator.location, location)
            people_ids = initiator.knowledge_people_locations.get_people_at_location(location)
            # add in inserted order, into the list of people with their id
            distance_factor =  self.target_distance_score_factor(distance)

            if distance_factor == -1:
                continue

            for person_id in people_ids:
                bias_score = self.calculate_target_score(initiator, person_id) * distance_factor
                if bias_score > -1:
                    bisect.insort(favorable_people, (bias_score, person_id))

        return [person_id for bias_score, person_id in favorable_people]

    """
    Returns a id of a person to look for in the same building, for this current interaction.
    This method will be called multiple times as the person moves towards their target.
    Default: Returns random person in same building
    RETURN A LIST NOT A SET
    """
    def calculate_interaction_targets_in_building(self, initiator):
        if len(initiator.current_building.current_occupants) == 1:
            return []

        favorable_people = [] # [(score, person)]
        # logging.info("LOL %s" % initiator.current_building.current_occupants)
        for person_id in initiator.current_building.current_occupants:
            # dont try interact with yourself
            if person_id == initiator.id_number:
                continue
            # add in inserted order, into the list of people with their id
            bias_score = self.calculate_target_score(initiator, person_id)
            # logging.info("%s" % bias_score)
            if bias_score > -1:
                bisect.insort(favorable_people, (bias_score, person_id))

        # logging.info("initator %s %s" % (initiator.id_number, [person_id for bias_score, person_id in reversed(favorable_people)]))
        return [person_id for bias_score, person_id in favorable_people]

    """
    Return a number to indicate how bias they have to interact with a certain available person.
    Note: Should return number between 0 and 1.
    Note: returning <= -1 will prevent them from interaction with the person whatsoever.
    Note: distance arg will be 0 if its a building interaction.
    Default: distance to the person.
    """
    def calculate_target_score(self, initiator, target_id):
        return -1


    """
    For cases when we are looking for person outside of a building.
    Returns a factor to multiply target score on based by their distance.
    """
    @abstractmethod
    def target_distance_score_factor(self, distance):
        ...


    def valid_interaction_target_in_building(self, initator, target_id):
        return target_id in initator.current_building.current_occupants

    """
    Return true/false to indicate whether the person would like to join the interaction.
    This is a static method therefore you cannot use self i.e. data cannot be accessed from this Interaction class
    """
    @abstractmethod
    def participate(self, initiator, target):
        ...

    """
    Each person will tick 
    """
    @abstractmethod
    def tick(self, person):
        ...



    """
    Return true/false to indicate whether the person would like to join the interaction.
    This is a static method therefore you cannot use self i.e. data cannot be accessed from this Interaction class
    """
    def to_string(self):
        if len(self.active_participants) <= 1:
            return "%s looking for participant (%s) in building %s" % (self.initiator.id_number, self.get_interaction_type(), self.initiator.current_building)
        return "%s interacting with %s (%s) in building %s" % (self.initiator.id_number,
                                                               self.participant.id_number,
                                                               self.get_interaction_type(),
                                                               self.initiator.current_building)



    def leave_interaction(self, participant):

        """
        The first person to leave will create the information interaction object
        """
        if len(self.active_participants) == 2:
            self.information_interaction = PublicInformation(self.information_interaction_on_end())
            # logging.info("%s finished socialising (%s) with %s (%s ticks)" % (participant.human.id_number,
            #                                               self.get_interaction_type(),
            #                                               participant.other_participant.human.id_number,
            #                                               TimeStamp().convert_to_ticks() - self.beginning_time.convert_to_ticks()))

        """
        Register the public information e.g. interaction information
        """
        self.witness_interaction_public_information(participant.human)

        """
        Register all private information passed on in interaction e.g. conversation
        """
        for info in participant.private_info:
            info.register_to_knowledge(participant.human)
            # print("%s told %s %s" % (participant.other_participant.human.id_number, participant.human.id_number, info))

        del self.active_participants[participant.human.id_number]
        participant.human.needs[NEED_TYPE.CURRENT_INTERACTION].finish_interaction(participant.human)










