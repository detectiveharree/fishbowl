from ai.humanai.relationships.knowledge.knowledge import Knowledge

"""
The knowledge of all people
"""
class KnowledgeGroupStockpileLocations(Knowledge):

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
        self.location_to_group = {} # {location : group}

    def register_from_information(self, human, informationgroupstockpilelocation):
        # if no group there

        if informationgroupstockpilelocation.group_id is None:
            # if we thought a group was there
            if informationgroupstockpilelocation.location in self.location_to_group.keys():
                # remove knowledge that we thought a group was there
                old_group_at_loc = self.location_to_group[informationgroupstockpilelocation.location]
                del self.location_to_group[informationgroupstockpilelocation.location]
                self.knowledge_groups.get_knowledge_of_group(old_group_at_loc).stockpile_location = informationgroupstockpilelocation.location
        else:
            # update group at location
            if informationgroupstockpilelocation.location in self.location_to_group.keys():
                old_group_at_loc = self.location_to_group[informationgroupstockpilelocation.location]
                self.knowledge_groups.get_knowledge_of_group(old_group_at_loc).stockpile_location = None

            self.location_to_group[informationgroupstockpilelocation.location] = informationgroupstockpilelocation.group_id


    """
    Use this method to return a random piece of information
    that you can create from the knowledge. 
    This is for use in interactions, get_random_information may be called
    to simulate random conversation being passed.
    """
    def get_random_information(self):
        return KnowledgeGroupStockpileSurvivalContents(stockpile_contents)