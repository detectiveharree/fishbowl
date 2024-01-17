from ai.humanai.relationships.information.informationinteraction.informationinteraction import InformationInteraction
from ai.humanai.relationships.interaction.interaction import INTERACTION_TYPE
from ai.humanai.relationships.interaction.interaction import ANGER_REASON




class InformationInteractionRomance(InformationInteraction):

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
        return INTERACTION_TYPE.ROMANCE

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
            If love is successful, both: lose fear for each other, increase love and respect for each other
            If unsuccessful, both: lose love and respect for each other
            """
            respect = 30 * self.success_constant
            love = 80 * self.success_constant

            other_id = self.participant_id if human_witness_id == self.initiator_id else self.initiator_id
            return [(other_id, love, 0, respect)]
        # human_witness_id is a witness
        else:

            new_love_init, new_fear_init, new_respect_init = 0, 0, 0
            new_love_part, new_fear_part, new_respect_part = 0, 0, 0

            iniator_love_score = witness.knowledge_of_people.human_opinions.most_love_sorted[self.initiator_id]
            participant_love_score = witness.knowledge_of_people.human_opinions.most_love_sorted[self.participant_id]

            hate_const = 50
            anger_const = 40

            """
            If they care about either of the participants,
            Hate the participants by how strongly they love one, and how much they hate other. Combine it and
            apply it to both for love dimension. For SO, also decrease respect by same amount.
            Anger at initiator
            """
            if self.initiator_id in witness.knowledge_of_people.human_opinions.potential_lovers_sorted.keys():
                love_init_percent = (iniator_love_score + 1) / 2 # (0-1 bigger if more love)
                hate_part_percent = 1 - ((participant_love_score + 1) / 2) # (0-1 bigger if more hate)
                total_percent = (love_init_percent + hate_part_percent) / 2 # total strength
                new_love_init = -hate_const * total_percent
                new_love_part = -hate_const * total_percent
                new_respect_init = -hate_const * total_percent
                witness.emotions.anger.change(witness, anger_const * iniator_love_score, (self.initiator_id, ANGER_REASON.JEALOUS_ROMANCE))
            elif self.participant_id in witness.knowledge_of_people.human_opinions.potential_lovers_sorted.keys():
                love_part_percent = (iniator_love_score + 1) / 2 # (0-1 bigger if more love)
                hate_init_percent = 1 - ((participant_love_score + 1) / 2) # (0-1 bigger if more hate)
                total_percent = (love_part_percent + hate_init_percent) / 2 # total strength
                new_love_init = -hate_const * total_percent
                new_love_part = -hate_const * total_percent
                new_respect_part = -hate_const * total_percent
                witness.emotions.anger.change(witness, anger_const * iniator_love_score, (self.initiator_id, ANGER_REASON.JEALOUS_ROMANCE))

            return [(self.participant_id, new_love_part, new_fear_part, new_respect_part),
                    (self.initiator_id, new_love_init, new_fear_init, new_respect_init)]


    """
    The value of this item if it was to be given to a person.
    """
    def get_value_score(self, person_id):
        return 0

