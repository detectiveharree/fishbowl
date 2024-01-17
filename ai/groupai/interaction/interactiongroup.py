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




"""
Interacton class is primilarly concerned with the transfer of:
Information e.g.
Physical contact
"""
class InteractionGroup(ABC):

    """
    DO NOT DELETE THIS. PASTE THIS IN FOR EVERY NEW OBJECT THAT WILL BE STORED IN A SET/DICTIONARY.
    THIS IS ESSENTIAL FOR MAKING SURE THE PROGRAM PERFORMS EXACTLY THE SAME EVERY TIME!

    assert(false) WILL CRASH THE PROGRAM IF YOU ATTEMPT TO PUT THIS OBJECT INTO A SET/DICT WITHOUT FIRST MODIFYING THE FUNCTION.
    THIS IS DONE ON PURPOSE TO PREVENT YOU FROM ACCIDENTALLY LEAKING NON-DETERMINISM INTO THE PROGRAM.
    SPEAK TO ME (TOM) AND I WILL EXPLAIN WHAT TO DO.
    """
    def __hash__(self):
        assert(False)

    def __init__(self, initiator_army, participant_army,initiator_battle_over_callback, participant_battle_over_callback):
        self.initiator = initiator_army
        self.participant = participant_army
        self.initiator_battle_over_callback = initiator_battle_over_callback
        self.participant_battle_over_callback = participant_battle_over_callback

        self.interaction_id = guiwindow.WORLD_INSTANCE.interaction_id_counter
        guiwindow.WORLD_INSTANCE.interaction_id_counter += 1

        self.active_participants = {}
        self.public_information = set()
        """
        Piece of public information viewable at all at all times:
        Will be assigned when interaction starts.
        Will be reassigned when interaction finishes.
        """
        self.information_interaction = None



    """
    Used when a interaction is starting
    """
    @abstractmethod
    def start_interaction(self):
        ...

    """
    We don't deal with humans in the tick function,
    instead we deal with InteractionParticipant objects.
    It contains the human, but also extra helper information
    that might be relevant for the current interaction. 
    """
    def get_interaction_participant(self, group):
        return self.active_participants[group.id_number]

    """
    Returns true if a human is involved in this current interaction
    """
    def group_in_interaction(self, group):
        return group.id_number in self.active_participants.keys()



    def leave_interaction(self, participant):
        logging.info("%s has left the battle" % participant.group.id_number)
        """
        The first person to leave will create the information interaction object
        """
        if len(self.active_participants) == 2:
            pass
            # logging.info("%s finished socialising (%s) with %s" % (participant.human.id_number,
            #                                               self.get_interaction_type(),
            #                                               participant.other_participant.human.id_number))

        """
        Register the public information e.g. interaction information
        """
        # self.witness_interaction_public_information(participant.human)

        """
        Register all private information passed on in interaction e.g. conversation
        """
        # for info in participant.private_info:
        #     info.register_to_knowledge(participant.human)
            # print("%s told %s %s" % (participant.other_participant.human.id_number, participant.human.id_number, info))

        del self.active_participants[participant.group.id_number]









