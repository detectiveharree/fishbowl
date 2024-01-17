from ai.humanai.relationships.knowledge.knowledge import Knowledge

"""
The knowledge of all people
"""
class KnowledgeGroupStats(Knowledge):

    """
    DO NOT DELETE THIS. PASTE THIS IN FOR EVERY NEW OBJECT THAT WILL BE STORED IN A SET/DICTIONARY.
    THIS IS ESSENTIAL FOR MAKING SURE THE PROGRAM PERFORMS EXACTLY THE SAME EVERY TIME!

    assert(false) WILL CRASH THE PROGRAM IF YOU ATTEMPT TO PUT THIS OBJECT INTO A SET/DICT WITHOUT FIRST MODIFYING THE FUNCTION.
    THIS IS DONE ON PURPOSE TO PREVENT YOU FROM ACCIDENTALLY LEAKING NON-DETERMINISM INTO THE PROGRAM.
    SPEAK TO ME (TOM) AND I WILL EXPLAIN WHAT TO DO.
    """
    def __hash__(self):
        assert(False)

    def __init__(self, knowledge_groups):
        self.knowledge_groups = knowledge_groups

    def register_from_information(self, human, informationgroupstats):
        group_knowledge = self.knowledge_groups.get_knowledge_of_group(informationgroupstats.group_id)
        group_knowledge.group_type = informationgroupstats.group_type
        group_knowledge.believed_food_buffer_factor = informationgroupstats.food_buffer
        group_knowledge.believed_water_buffer_factor = informationgroupstats.water_buffer
        # if informationgroupstats.group_id == 43 and human.group.id_number == 43:
        #     print("FUCKKKKK YES WHAT AM I DOING")
        #     print(informationgroupstats.water_buffer)
        #     print(informationgroupstats.food_buffer)


    """
    Use this method to return a random piece of information
    that you can create from the knowledge. 
    This is for use in interactions, get_random_information may be called
    to simulate random conversation being passed.
    """
    def get_random_information(self):
        return KnowledgeGroupStockpileSurvivalContents(stockpile_contents)