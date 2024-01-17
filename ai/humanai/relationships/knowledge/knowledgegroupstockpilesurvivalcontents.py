from ai.humanai.relationships.knowledge.knowledge import Knowledge
from items.itemresources.itemresource import ResourceType

"""
The knowledge of all people
"""
class KnowledgeGroupStockpileSurvivalContents(Knowledge):

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

    def register_from_information(self, human, informationgroupstockpilecontent):
        group_knowledge = self.knowledge_groups.get_knowledge_of_group(informationgroupstockpilecontent.group_id)
        group_knowledge.believed_amount_food = informationgroupstockpilecontent.task_survival_food_contents[ResourceType.FOOD].storage
        group_knowledge.believed_amount_water = informationgroupstockpilecontent.task_survival_water_contents[ResourceType.WATER].storage


    def get_stockpile_resource_contents(self, group_id, resource):
        group_knowledge = self.knowledge_groups.get_knowledge_of_group(group_id)

        return group_knowledge.believed_amount_food if resource == ResourceType.FOOD else group_knowledge.believed_amount_water


    """
    Use this method to return a random piece of information
    that you can create from the knowledge. 
    This is for use in interactions, get_random_information may be called
    to simulate random conversation being passed.
    """
    def get_random_information(self):
        return KnowledgeGroupStockpileSurvivalContents(stockpile_contents)