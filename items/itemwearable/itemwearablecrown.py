from items.itemwearable.itemwearable import ItemWearable


class Crown(ItemWearable):

    """
    DO NOT DELETE THIS. PASTE THIS IN FOR EVERY NEW OBJECT THAT WILL BE STORED IN A SET/DICTIONARY.
    THIS IS ESSENTIAL FOR MAKING SURE THE PROGRAM PERFORMS EXACTLY THE SAME EVERY TIME!

    assert(false) WILL CRASH THE PROGRAM IF YOU ATTEMPT TO PUT THIS OBJECT INTO A SET/DICT WITHOUT FIRST MODIFYING THE FUNCTION.
    THIS IS DONE ON PURPOSE TO PREVENT YOU FROM ACCIDENTALLY LEAKING NON-DETERMINISM INTO THE PROGRAM.
    SPEAK TO ME (TOM) AND I WILL EXPLAIN WHAT TO DO.
    """
    def __hash__(self):
        assert(False)


    def __init__(self, material):
        super().__init__()

        # performance
        self.material = material
        # HAVE YET TO DO CROWNS LOGIC, WILL PROBABLY JUST HAVE A HEAD ID

    def calibrate_performance_to_wielder(self, human):
        pass

    def __str__(self):
        return f'{self.material} crown'