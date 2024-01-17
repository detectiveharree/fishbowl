from ai.humanai.relationships.information.informationinteraction.informationinteraction import InformationInteraction
from ai.humanai.relationships.interaction.interaction import INTERACTION_TYPE




class InformationInteractionChat(InformationInteraction):

    """
    DO NOT DELETE THIS. PASTE THIS IN FOR EVERY NEW OBJECT THAT WILL BE STORED IN A SET/DICTIONARY.
    THIS IS ESSENTIAL FOR MAKING SURE THE PROGRAM PERFORMS EXACTLY THE SAME EVERY TIME!

    assert(false) WILL CRASH THE PROGRAM IF YOU ATTEMPT TO PUT THIS OBJECT INTO A SET/DICT WITHOUT FIRST MODIFYING THE FUNCTION.
    THIS IS DONE ON PURPOSE TO PREVENT YOU FROM ACCIDENTALLY LEAKING NON-DETERMINISM INTO THE PROGRAM.
    SPEAK TO ME (TOM) AND I WILL EXPLAIN WHAT TO DO.
    """
    def __hash__(self):
        assert(False)

    def __init__(self, interaction_id, initiator_id, participant_id, success_constant):
        super().__init__(interaction_id, initiator_id, participant_id)
        self.success_constant = success_constant


    """
    Returns the interaction type
    """
    def get_interaction_type(self):
        return INTERACTION_TYPE.CHAT

    """
    Called when finally registered to a human's interaction memory cache.
    MUST return a tuple with human_id, love, fear, respect score for each participant in the interaction
    These values SHOULD be calculated from the perspective of the human
    passed in the parameter, as multiple can witness a interaction.
    Since these can be registered at any time (i.e. information spreads) make
    sure to take into account time_occured if you want to dampen the actual love/fear/respect values.
    return [(human_id, love, fear, respect)] 
    """
    def get_memory_cache_values(self, witness):
        human_witness_id = witness.id_number


        # human_witness_id is the initator or particpant
        if human_witness_id == self.initiator_id or human_witness_id == self.participant_id:


            """
            If chat is successful, both: increase love and respect for each other
            If unsuccessful, both: lose love and respect for each other
            """

            respect = 0
            love = 0

            if self.success_constant > 0:
                love = 20 * self.success_constant
                respect = 20 * self.success_constant
            else:
                love = 5 * self.success_constant
                respect = 10 * self.success_constant

            other_id = self.participant_id if human_witness_id == self.initiator_id else self.initiator_id
            return [( other_id, love, 0, respect)]
        # human_witness_id is a witness
        else:
            """
            A witness may be jealous of an interaction if he respects and disrespects other parties respectively.
            In this case he will love some respect for the person he respects proportional to how much he disrespects the other
            person.
            """

            iniator_respect_score = witness.knowledge_of_people.human_opinions.most_respect_sorted[self.initiator_id]
            participant_respect_score = witness.knowledge_of_people.human_opinions.most_respect_sorted[self.participant_id]


            # if witnesses likes or dislikes both participants he doesn't care about interaction
            if (iniator_respect_score > 0 and participant_respect_score > 0) or\
                    (iniator_respect_score < 0 and participant_respect_score < 0) or\
                    (iniator_respect_score == 0 and participant_respect_score == 0):
                return []
            jealously_constant = 5

            iniator_respect_score_as_percent = 1 - ((iniator_respect_score + 1) / 2)
            participant_respect_score_as_percent = 1 - ((participant_respect_score + 1) / 2)

            # if he likes the initator but not participant, decrement love of him by amount he hates participant * jealousy constant
            if iniator_respect_score > 0:
                return [( self.initiator_id, 0, 0, participant_respect_score_as_percent * jealously_constant)]
            elif participant_respect_score > 0:
                return [( self.participant_id, 0, 0, iniator_respect_score_as_percent * jealously_constant)]
            return []



    """
    The value of this item if it was to be given to a person.
    """
    def get_value_score(self, person_id):
        return 0

