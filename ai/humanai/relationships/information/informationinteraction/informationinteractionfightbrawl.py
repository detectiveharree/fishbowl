from ai.humanai.relationships.information.informationinteraction.informationinteractionfight import InformationInteractionFight
from ai.humanai.relationships.interaction.interaction import INTERACTION_TYPE
import guiwindow
from ai.humanai.relationships.interaction.interaction import ANGER_REASON


class InformationInteractionFightBrawl(InformationInteractionFight):

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
    Because we'll be associating alot of information with a fight, it will not be feasible
    to make a copy of it for every witness, therefore we pass in the actual interactionfight object
    which stores much of the info.
    """
    def __init__(self, interaction_id, initiator_id, participant_id,
                 interaction_fight):
        super().__init__(interaction_id, initiator_id, participant_id, interaction_fight)


    """
    Returns tuple of theoretical particicreate_theoretical_fightpants.
    (TheoreticalHuman (perspective), TheoreticalHuman (other) )
    """
    def get_fight_score(self, human_perspective_id):
        if human_perspective_id == self.initiator_id:
            return self.initiator_fight_score
        return self.participant_fight_score


    """
    Returns the interaction type
    """
    def get_interaction_type(self):
        return INTERACTION_TYPE.FIGHT_BRAWL

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
        BASE_LOVE_DELTA = 30 # base decrease in love for init for starting the fight

        # human_witness_id is the initator or particpant
        if human_witness_id == self.initiator_id or human_witness_id == self.participant_id:
            if self.winner is None:
                return []

            new_love_init, new_fear_init, new_respect_init = 0, 0, 0
            new_love_part, new_fear_part, new_respect_part = 0, 0, 0

            (delta_love_init_ff_h, delta_fear_init_ff_h, delta_respect_init_ff_h) = self.fair_fight_from_health_memory_values(40)
            (delta_love_init_s_h, delta_fear_init_s_h, delta_respect_init_s_h) = self.fair_fight_from_strength_memory_values(80)
            (delta_respect_init_dt, delta_respect_part_dt) = self.damage_taken_respect_memory_values(100)
            (delta_love_init_dr, delta_fear_init_dr, delta_respect_init_dr, delta_love_part_dr, delta_fear_part_dr, delta_respect_part_dr) = self.damage_difference_memory_values(100)

            new_love_init += delta_love_init_ff_h + delta_love_init_s_h + delta_love_init_dr
            new_fear_init += delta_fear_init_ff_h + delta_fear_init_s_h + delta_fear_init_dr
            new_respect_init += delta_respect_init_ff_h + delta_respect_init_s_h + delta_respect_init_dt + delta_respect_init_dr

            new_love_part += delta_love_part_dr
            new_fear_part += delta_fear_part_dr
            new_respect_part += delta_respect_part_dt + delta_respect_part_dr

            new_love_init -= BASE_LOVE_DELTA

            if human_witness_id == self.initiator_id:
                return [(self.participant_id, new_love_part, new_fear_part, new_respect_part)]
            else:
                return [(self.initiator_id, new_love_init, new_fear_init, new_respect_init)]

        # human_witness_id is a witness
        else:

            """
            A witness takes into account if it was a fair fight in terms of starting health, strength and proportional damage taken.
            This is the same as the actual participants but less strong 
            """

            new_love_init, new_fear_init, new_respect_init = 0, 0, 0
            new_love_part, new_fear_part, new_respect_part = 0, 0, 0

            iniator_love_score = witness.knowledge_of_people.human_opinions.most_love_sorted[self.initiator_id]
            participant_love_score = witness.knowledge_of_people.human_opinions.most_love_sorted[self.participant_id]


            (delta_love_init_ff_h, delta_fear_init_ff_h, delta_respect_init_ff_h) = self.fair_fight_from_health_memory_values(10)
            (delta_love_init_s_h, delta_fear_init_s_h, delta_respect_init_s_h) = self.fair_fight_from_strength_memory_values(20)
            (delta_love_init_dr, delta_fear_init_dr, delta_respect_init_dr, delta_love_part_dr, delta_fear_part_dr, delta_respect_part_dr) = self.damage_difference_memory_values(20)

            new_love_init += delta_love_init_ff_h + delta_love_init_s_h + delta_love_init_dr
            new_fear_init += delta_fear_init_ff_h + delta_fear_init_s_h + delta_fear_init_dr
            new_respect_init += delta_respect_init_ff_h + delta_respect_init_s_h + delta_respect_init_dr

            new_love_part += delta_love_part_dr
            new_fear_part += delta_fear_part_dr
            new_respect_part += delta_respect_part_dr

            # if witnesses likes or dislikes both participants he doesn't care about interaction
            if (iniator_love_score > 0 and participant_love_score > 0) or\
                    (iniator_love_score < 0 and participant_love_score < 0) or\
                    (iniator_love_score == 0 and participant_love_score == 0):

                # no difference in love for either participant, only fear and respect
                return [(self.participant_id, 0, new_fear_part, new_respect_part),
                        (self.initiator_id, 0, new_fear_init, new_respect_init)]


            anger_const = 50
            """
            Make him angry at person who tried to fight friend
            """
            if iniator_love_score > 0 and participant_love_score <= 0:
                new_love_part -= BASE_LOVE_DELTA * iniator_love_score
                witness.emotions.anger.change(witness, anger_const * iniator_love_score, (self.participant_id, ANGER_REASON.FOUGHT_FRIEND))
                pass

            """
            Make him angry at person who tried to fight friend
            """
            if iniator_love_score <= 0 and participant_love_score > 0:
                # dislike initator if already disliked them and they were initator
                new_love_init -= BASE_LOVE_DELTA * participant_love_score
                witness.emotions.anger.change(witness, anger_const * participant_love_score, (self.initiator_id, ANGER_REASON.FOUGHT_FRIEND))


            return [(self.participant_id, new_love_part, new_fear_part, new_respect_part),
                    (self.initiator_id, new_love_init, new_fear_init, new_respect_init)]




    """
    The value of this item if it was to be given to a person.
    """
    def get_value_score(self, person_id):
        return 0
