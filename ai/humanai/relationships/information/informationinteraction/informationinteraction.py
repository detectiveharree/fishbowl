from ai.humanai.relationships.information.information import Information
from abc import ABC, abstractmethod
from gameworld.timestamp import TimeStamp


"""
Converts a interaction into a interaction summary
"""

class InformationInteraction(Information, ABC):

    """
    DO NOT DELETE THIS. PASTE THIS IN FOR EVERY NEW OBJECT THAT WILL BE STORED IN A SET/DICTIONARY.
    THIS IS ESSENTIAL FOR MAKING SURE THE PROGRAM PERFORMS EXACTLY THE SAME EVERY TIME!

    assert(false) WILL CRASH THE PROGRAM IF YOU ATTEMPT TO PUT THIS OBJECT INTO A SET/DICT WITHOUT FIRST MODIFYING THE FUNCTION.
    THIS IS DONE ON PURPOSE TO PREVENT YOU FROM ACCIDENTALLY LEAKING NON-DETERMINISM INTO THE PROGRAM.
    SPEAK TO ME (TOM) AND I WILL EXPLAIN WHAT TO DO.
    """
    def __hash__(self):
        assert(False)

    def __init__(self, interaction_id, initiator_id, participant_id):
        self.interaction_id = interaction_id
        self.initiator_id = initiator_id
        self.participant_id = participant_id
        # time of initalisation
        self.time_occured = TimeStamp()


    """
    Returns the interaction type
    """
    @abstractmethod
    def get_interaction_type(self):
        ...


    """
    Called when finally registered to a human's interaction memory cache.
    MUST return a tuple with human_id, love, fear, respect score for each participant in the interaction
    These values SHOULD be calculated from the perspective of the human
    passed in the parameter, as multiple can witness a interaction.
    Since these can be registered at any time (i.e. information spreads) make
    sure to take into account time_occured if you want to dampen the actual love/fear/respect values.
    return [(human_id, love, fear, respect)] 
    """
    @abstractmethod
    def get_memory_cache_values(self, witness):
        ...

    """
    Given a human object, register the information in this class to that person.
    """
    @abstractmethod
    def get_value_score(self, human):
        ...

    """
    Given a human object, register the information in this class to that person.
    """
    def register_to_knowledge(self, human):
        human.knowledge_interactions.register_from_information(human, self)


    def __str__(self):
        return "Info: %s %s %s" % (self.initiator_id, self.get_interaction_type(), self.participant_id)


