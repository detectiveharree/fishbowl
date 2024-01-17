from ai.humanai.relationships.information.informationlocation import InformationLocation
from ai.humanai.relationships.information.information import Information

class InformationGroupStats(Information):

    """
    DO NOT DELETE THIS. PASTE THIS IN FOR EVERY NEW OBJECT THAT WILL BE STORED IN A SET/DICTIONARY.
    THIS IS ESSENTIAL FOR MAKING SURE THE PROGRAM PERFORMS EXACTLY THE SAME EVERY TIME!

    assert(false) WILL CRASH THE PROGRAM IF YOU ATTEMPT TO PUT THIS OBJECT INTO A SET/DICT WITHOUT FIRST MODIFYING THE FUNCTION.
    THIS IS DONE ON PURPOSE TO PREVENT YOU FROM ACCIDENTALLY LEAKING NON-DETERMINISM INTO THE PROGRAM.
    SPEAK TO ME (TOM) AND I WILL EXPLAIN WHAT TO DO.
    """
    def __hash__(self):
        assert(False)

    def __init__(self, group_id, group_type, food_buffer, water_buffer):
        self.group_id = group_id
        self.group_type = group_type
        self.water_buffer = water_buffer
        self.food_buffer = food_buffer


    """
    Given a human object, register the information in this class to that person.
    """
    def register_to_knowledge(self, human):
        human.knowledge_group_stats.register_from_information(human, self)


    """
    The value of this item if it was to be given to a person.
    """
    def get_value_score(self, person_id):
        return 0

    def __str__(self):
        return "Stockpile contents for group %s" % self.group_id
