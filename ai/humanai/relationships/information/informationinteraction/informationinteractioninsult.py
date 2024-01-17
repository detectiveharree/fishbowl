from ai.humanai.relationships.information.informationinteraction.informationinteraction import InformationInteraction
from ai.humanai.relationships.interaction.interaction import INTERACTION_TYPE




class InformationInteractionInsult(InformationInteraction):

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
        return INTERACTION_TYPE.INSULT

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

        # human_witness_id is the initator
        if human_witness_id == self.initiator_id:

            """
            If insult lands decrease fear and respect for person.
            If insult doesn't land increase fear and respect for person and decrease love for them. 
            """
            fear = -5 * self.success_constant
            respect = -10 * self.success_constant
            love = 0

            if self.success_constant < 0:
                love = 30 * self.success_constant

            return [(self.participant_id, love, fear, respect)]
        # human_witness_id is the participant
        elif human_witness_id == self.participant_id:

            """
            If insult lands, increase fear (a bit), respect of insulter, and decrease love for them by alot
            if insult doesn't land, decrease fear and respect of insulter by alot, and decrease love by a bit
            """
            fear = 0
            respect = 0
            love = 0

            if self.success_constant > 0:
                fear = 5 * self.success_constant
                respect = 10 * self.success_constant
                love = -30 * self.success_constant
            else:
                fear = 10 * self.success_constant
                respect = 20 * self.success_constant
                love = 5 * self.success_constant

            return [(self.initiator_id, love, fear, respect)]
        # human_witness_id is a witness
        else:  

            new_love_init, new_fear_init, new_respect_init = 0, 0, 0
            new_love_part, new_fear_part, new_respect_part = 0, 0, 0
            iniator_love_score = witness.knowledge_of_people.human_opinions.most_love_sorted[self.initiator_id]
            participant_love_score = witness.knowledge_of_people.human_opinions.most_love_sorted[self.participant_id]


            # if witnesses likes or dislikes both participants he doesn't care about interaction
            if (iniator_love_score > 0 and participant_love_score > 0) or\
                    (iniator_love_score < 0 and participant_love_score < 0) or\
                    (iniator_love_score == 0 and participant_love_score == 0):
                return []

            love_success_const = 20
            respect_success_const = 5
            fear_success_const = 5

            """
            If person insults someone he doesn't like and he likes the person
            If successful | respect + love goes up proportional to success, fear and respect drops for other
            If not successful | respect goes down proportional to success, respect goes up for other
            """
            if iniator_love_score > 0 and participant_love_score <= 0:
                if self.success_constant > 0:
                    new_love_init = self.success_constant * love_success_const
                    new_respect_init = self.success_constant * respect_success_const

                    new_respect_part = self.success_constant * -respect_success_const
                    new_fear_part = self.success_constant * -fear_success_const
                else:
                    new_respect_init = self.success_constant * respect_success_const

                    new_respect_part = self.success_constant * -respect_success_const


            """
            If person insults someone he likes and he doesn't like the person
                If successful | respect goes up love goes down proportional to success, fear and respect drops for other
                If not successful | respect + love goes down proportional to success, respect goes up for other
            """
            if iniator_love_score <= 0 and participant_love_score > 0:
                if self.success_constant > 0:
                    new_love_init = self.success_constant * -love_success_const
                    new_respect_init = self.success_constant * respect_success_const

                    new_respect_part = self.success_constant * -respect_success_const
                    new_fear_part = self.success_constant * -respect_success_const
                else:
                    new_love_init = self.success_constant * love_success_const
                    new_respect_init = self.success_constant * respect_success_const

                    new_respect_part = self.success_constant * -respect_success_const


            return [(self.participant_id, new_love_part, new_fear_part, new_respect_part),
                    (self.initiator_id, new_love_init, new_fear_init, new_respect_init)]


    """
    The value of this item if it was to be given to a person.
    """
    def get_value_score(self, person_id):
        return 0



