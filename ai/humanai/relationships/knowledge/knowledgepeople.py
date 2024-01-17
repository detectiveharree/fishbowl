from ai.humanai.relationships.knowledge.knowledgehuman import KnowledgeHuman
from ai.humanai.relationships.knowledge.knowledgehumanopinions import KnowledgeHumanOpinions

decay_rate = 0.99

"""
The knowledge of all people
"""
class KnowledgePeople():

    """
    DO NOT DELETE THIS. PASTE THIS IN FOR EVERY NEW OBJECT THAT WILL BE STORED IN A SET/DICTIONARY.
    THIS IS ESSENTIAL FOR MAKING SURE THE PROGRAM PERFORMS EXACTLY THE SAME EVERY TIME!

    assert(false) WILL CRASH THE PROGRAM IF YOU ATTEMPT TO PUT THIS OBJECT INTO A SET/DICT WITHOUT FIRST MODIFYING THE FUNCTION.
    THIS IS DONE ON PURPOSE TO PREVENT YOU FROM ACCIDENTALLY LEAKING NON-DETERMINISM INTO THE PROGRAM.
    SPEAK TO ME (TOM) AND I WILL EXPLAIN WHAT TO DO.
    """
    def __hash__(self):
        assert(False)

    def __init__(self, human):
        self.human = human
        self.known_people = {} # {person_id : KnowledgeHuman}
        self.human_opinions = KnowledgeHumanOpinions(human)


    def amount_known_people(self):
        return len(self.known_people.keys())

    """
    See get_knowledge_of_people
    """
    def register_from_information(self, human):
        ...

    def knows_person(self, person_id):
        return person_id in self.known_people.keys()


    """
    Register a empty version of a person if not known already
    """
    def register_knowledge_of_person(self, person_id):
        assert(person_id != -1)
        assert(isinstance(person_id, int))
        if not self.knows_person(person_id):
            know_person = KnowledgeHuman(person_id)
            self.known_people[person_id] = know_person
            # important to record thme as 0
            self.human.knowledge_of_people.human_opinions.register_new_score(person_id, 0, 0, 0)

    """
    Theres so many opportunities for a person to first hear about another person,
    that its not feasable to register a person through the register_from_information function
    (because every time we call get_knowledge_of_person we will need to check knows_person
    and call register_from_information if fails).
    Therefore we make an exception for knowledge of people and register a new person whenever
    we call get_knowledge_of_person
    """
    def get_knowledge_of_person(self, person_id):
        self.register_knowledge_of_person(person_id)
        return self.known_people[person_id]


    def decay_opinions(self):
        for person, knowledge_of in self.known_people.items():
            knowledge_of.interaction_memory_cache.decay(decay_rate)
        self.human_opinions.decay(decay_rate)


    """
    Same as above, but flicks recalculate flag for score
    I.e. use this when updating information about the group
    """
    def get_knowledge_of_person(self, person_id):
        self.register_knowledge_of_person(person_id)
        person = self.known_people[person_id]
        person.recalculate_score = True
        return person

    def amount_known_people(self):
        return len(self.known_people)





