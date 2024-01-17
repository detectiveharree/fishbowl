from ai.humanai.relationships.information.informationlocation import InformationLocation


class InformationLocationCell(InformationLocation):


    """
    DO NOT DELETE THIS. PASTE THIS IN FOR EVERY NEW OBJECT THAT WILL BE STORED IN A SET/DICTIONARY.
    THIS IS ESSENTIAL FOR MAKING SURE THE PROGRAM PERFORMS EXACTLY THE SAME EVERY TIME!

    assert(false) WILL CRASH THE PROGRAM IF YOU ATTEMPT TO PUT THIS OBJECT INTO A SET/DICT WITHOUT FIRST MODIFYING THE FUNCTION.
    THIS IS DONE ON PURPOSE TO PREVENT YOU FROM ACCIDENTALLY LEAKING NON-DETERMINISM INTO THE PROGRAM.
    SPEAK TO ME (TOM) AND I WILL EXPLAIN WHAT TO DO.
    """
    def __hash__(self):
        assert(False)


    def __init__(self, location, cellbase):
        super().__init__(location) # ALWAYS CALL PARENT CONSTRUCTOR
        self.cellbase = cellbase


    """
    Given a human object, register the information in this class to that person.
    """
    def register_to_knowledge(self, human):
        human.knowledge_cell_locations.register_from_information(human, self)

    """
    The value of this item if it was to be given to a person.
    """
    def get_value_score(self, person_id):
        return 0

    def __str__(self):
        return "Location cell for " % self.cell
