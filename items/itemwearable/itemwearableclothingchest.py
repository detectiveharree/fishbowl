from items.itemwearable.itemwearable import ItemWearable


class ClothingChest(ItemWearable):

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
        self.rng_cosmetic_attributes = [1,1,1]
        self.torso_id = 1
        self.arm_id = 1
        self.leg_id = 1

    def calibrate_performance_to_wielder(self, human):
        pass

    def __str__(self):
        return f'{self.material} chest clothing'