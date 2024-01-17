from ai.humanai.relationships.information.information import Information


class InformationPersonGroup(Information):

    """
    DO NOT DELETE THIS. PASTE THIS IN FOR EVERY NEW OBJECT THAT WILL BE STORED IN A SET/DICTIONARY.
    THIS IS ESSENTIAL FOR MAKING SURE THE PROGRAM PERFORMS EXACTLY THE SAME EVERY TIME!

    assert(false) WILL CRASH THE PROGRAM IF YOU ATTEMPT TO PUT THIS OBJECT INTO A SET/DICT WITHOUT FIRST MODIFYING THE FUNCTION.
    THIS IS DONE ON PURPOSE TO PREVENT YOU FROM ACCIDENTALLY LEAKING NON-DETERMINISM INTO THE PROGRAM.
    SPEAK TO ME (TOM) AND I WILL EXPLAIN WHAT TO DO.
    """
    def __hash__(self):
        assert(False)

    def __init__(self, person_id, group_id):
        self.person_id = person_id
        self.group_id = group_id


    """
    Given a human object, register the information in this class to that person.
    """
    def register_to_knowledge(self, human):
        human.knowledge_people_groups.register_from_information(human, self)


    """
    The value of this item if it was to be given to a person.
    """
    def get_value_score(self, person_id):
        return 0

    def __str__(self):
        return "Person %s is in group %s " % (self.person_id, self.group_id)
