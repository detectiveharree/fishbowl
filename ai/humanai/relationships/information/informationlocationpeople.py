from ai.humanai.relationships.information.informationlocation import InformationLocation


class InformationLocationPeople(InformationLocation):

    """
    DO NOT DELETE THIS. PASTE THIS IN FOR EVERY NEW OBJECT THAT WILL BE STORED IN A SET/DICTIONARY.
    THIS IS ESSENTIAL FOR MAKING SURE THE PROGRAM PERFORMS EXACTLY THE SAME EVERY TIME!

    assert(false) WILL CRASH THE PROGRAM IF YOU ATTEMPT TO PUT THIS OBJECT INTO A SET/DICT WITHOUT FIRST MODIFYING THE FUNCTION.
    THIS IS DONE ON PURPOSE TO PREVENT YOU FROM ACCIDENTALLY LEAKING NON-DETERMINISM INTO THE PROGRAM.
    SPEAK TO ME (TOM) AND I WILL EXPLAIN WHAT TO DO.
    """
    def __hash__(self):
        assert(False)

    def __init__(self, location, people):
        super().__init__(location) # ALWAYS CALL PARENT CONSTRUCTOR
        self.people = people


    """
    Given a human object, register the information in this class to that person.
    """
    def register_to_knowledge(self, human):
        human.knowledge_people_locations.register_from_information(human, self)


    """
    The value of this item if it was to be given to a person.
    """
    def get_value_score(self, person_id):
        return 0

    def __str__(self):
        return "Location of people at " % self.location

