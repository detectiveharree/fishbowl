from ai.humanai.relationships.information.information import Information


class InformationGroupStockpileSurvivalContents(Information):

    """
    DO NOT DELETE THIS. PASTE THIS IN FOR EVERY NEW OBJECT THAT WILL BE STORED IN A SET/DICTIONARY.
    THIS IS ESSENTIAL FOR MAKING SURE THE PROGRAM PERFORMS EXACTLY THE SAME EVERY TIME!

    assert(false) WILL CRASH THE PROGRAM IF YOU ATTEMPT TO PUT THIS OBJECT INTO A SET/DICT WITHOUT FIRST MODIFYING THE FUNCTION.
    THIS IS DONE ON PURPOSE TO PREVENT YOU FROM ACCIDENTALLY LEAKING NON-DETERMINISM INTO THE PROGRAM.
    SPEAK TO ME (TOM) AND I WILL EXPLAIN WHAT TO DO.
    """
    def __hash__(self):
        assert(False)


    def __init__(self, task_survival_food, task_survival_water, group_id):

        # Deep copy is very important here otherwise we might end up using the same object i.e. leaking info
        self.task_survival_food_contents = task_survival_food
        self.task_survival_water_contents = task_survival_water
        self.group_id = group_id


    """
    Given a human object, register the information in this class to that person.
    """
    def register_to_knowledge(self, human):
        human.knowledge_group_stockpile_contents.register_from_information(human, self)


    """
    The value of this item if it was to be given to a person.
    """
    def get_value_score(self, person_id):
        return 0

    def __str__(self):
        return "Stockpile contents for group %s" % self.group_id
