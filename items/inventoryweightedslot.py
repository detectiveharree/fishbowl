from items.itemresources.itemresource import ItemResource, ResourceType

class InventoryWeightedSlot():

    """
    DO NOT DELETE THIS. PASTE THIS IN FOR EVERY NEW OBJECT THAT WILL BE STORED IN A SET/DICTIONARY.
    THIS IS ESSENTIAL FOR MAKING SURE THE PROGRAM PERFORMS EXACTLY THE SAME EVERY TIME!

    assert(false) WILL CRASH THE PROGRAM IF YOU ATTEMPT TO PUT THIS OBJECT INTO A SET/DICT WITHOUT FIRST MODIFYING THE FUNCTION.
    THIS IS DONE ON PURPOSE TO PREVENT YOU FROM ACCIDENTALLY LEAKING NON-DETERMINISM INTO THE PROGRAM.
    SPEAK TO ME (TOM) AND I WILL EXPLAIN WHAT TO DO.
    """
    def __hash__(self):
        assert(False)

    def __init__(self, max_weight):
        self.max_weight = max_weight
        # creates inventory slot for every possible resource in the game of size 100
        # Initalising everyone with 0 resources is important for stabilising buffer factors early on
        self.resources = { resource_type:ItemResource(resource_type, 0) for resource_type in list(ResourceType)}


