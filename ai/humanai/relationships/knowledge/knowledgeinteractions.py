from ai.humanai.relationships.knowledge.knowledge import Knowledge
from ai.humanai.relationships.interaction.interaction import INTERACTION_TYPE
from ai.need import NEED_TYPE


"""
Knowledge interactions is used to register 
"""
class KnowledgeInteractions(Knowledge):

    """
    DO NOT DELETE THIS. PASTE THIS IN FOR EVERY NEW OBJECT THAT WILL BE STORED IN A SET/DICTIONARY.
    THIS IS ESSENTIAL FOR MAKING SURE THE PROGRAM PERFORMS EXACTLY THE SAME EVERY TIME!

    assert(false) WILL CRASH THE PROGRAM IF YOU ATTEMPT TO PUT THIS OBJECT INTO A SET/DICT WITHOUT FIRST MODIFYING THE FUNCTION.
    THIS IS DONE ON PURPOSE TO PREVENT YOU FROM ACCIDENTALLY LEAKING NON-DETERMINISM INTO THE PROGRAM.
    SPEAK TO ME (TOM) AND I WILL EXPLAIN WHAT TO DO.
    """
    def __hash__(self):
        assert(False)

    def __init__(self, knowledge_people, human):
        self.knowledge_people = knowledge_people
        self.human = human





    def predict_better_weapon(self):
        pass




    def register_from_information(self, human, informationinteraction):
        """
        For each person in the interaction, calculate a score for each participant
        from the perspective of the person who is hearing it.
        Register these scores along with the interaction itself in their interaction knowledge of the person.
        """

        # just in case never seen these people before
        if informationinteraction.initiator_id != human.id_number:
            self.human.knowledge_of_people.register_knowledge_of_person(informationinteraction.initiator_id)

        # just in case never seen these people before
        if informationinteraction.participant_id != human.id_number:
            self.human.knowledge_of_people.register_knowledge_of_person(informationinteraction.participant_id)


        for (person_id, love, fear, respect) in informationinteraction.get_memory_cache_values(human):
            knowledge_person = self.knowledge_people.get_knowledge_of_person(person_id)
            knowledge_person.interaction_memory_cache.register_interaction(love, fear, respect, informationinteraction)
            new_love, new_fear, new_respect = knowledge_person.interaction_memory_cache.get_scaled_relationship_scores()
            self.knowledge_people.human_opinions.register_new_score(person_id, new_love, new_fear, new_respect)


        if human.id_number == informationinteraction.initiator_id or human.id_number == informationinteraction.participant_id:

            """
            This might record duplicates interactions if we're told about a interaction we were in
            ... MAKE sure you can't be told about interactions you were already in
            """

            other_id = informationinteraction.participant_id \
                if human.id_number == informationinteraction.initiator_id else informationinteraction.initiator_id

            self.knowledge_people.get_knowledge_of_person(other_id).total_interactions += 1

            if informationinteraction.get_interaction_type() == INTERACTION_TYPE.ROMANCE:
                self.knowledge_people.human_opinions.register_romance(other_id)

            if other_id in self.knowledge_people.human_opinions.interaction_counts[informationinteraction.get_interaction_type()].keys():
                self.knowledge_people.human_opinions.interaction_counts[informationinteraction.get_interaction_type()][other_id] += 1
            else:
                self.knowledge_people.human_opinions.interaction_counts[informationinteraction.get_interaction_type()][other_id] = 1

            """
            Record fight for training purposes
            """
            if informationinteraction.get_interaction_type() == INTERACTION_TYPE.FIGHT_BRAWL or\
                informationinteraction.get_interaction_type() == INTERACTION_TYPE.FIGHT_TRAINING or\
                    informationinteraction.get_interaction_type() == INTERACTION_TYPE.FIGHT_BATTLE:
                # if these are not none then it is a valid fight to record
                if informationinteraction.initiator_fight_score is not None and informationinteraction.participant_fight_score is not None:
                    human.needs[NEED_TYPE.TRAIN].register_theoretical_fight(human, informationinteraction)

    """
    Use this method to return a random piece of information
    that you can create from the knowledge. 
    This is for use in interactions, get_random_information may be called
    to simulate random conversation being passed.
    """
    def get_random_information(self):
        return KnowledgeGroupStockpileSurvivalContents(stockpile_contents)