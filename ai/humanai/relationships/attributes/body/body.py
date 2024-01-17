from ai.humanai.relationships.attributes.body.limb import Head, Eye, Torso, Leg, Arm
from enum import Enum
from ai.humanai.relationships.attributes.attributes import BoundedNumber

class GENDER_TYPE(Enum):
    MALE = 1
    FEMALE = 2

    def __str__(self):
        return self.name

    def __repr__(self):
        return str(self)

BASE_WEAPON_DAMAGE = 10

"""
Body class to store all limbs
"""
class Body():

    """
    DO NOT DELETE THIS. PASTE THIS IN FOR EVERY NEW OBJECT THAT WILL BE STORED IN A SET/DICTIONARY.
    THIS IS ESSENTIAL FOR MAKING SURE THE PROGRAM PERFORMS EXACTLY THE SAME EVERY TIME!

    assert(false) WILL CRASH THE PROGRAM IF YOU ATTEMPT TO PUT THIS OBJECT INTO A SET/DICT WITHOUT FIRST MODIFYING THE FUNCTION.
    THIS IS DONE ON PURPOSE TO PREVENT YOU FROM ACCIDENTALLY LEAKING NON-DETERMINISM INTO THE PROGRAM.
    SPEAK TO ME (TOM) AND I WILL EXPLAIN WHAT TO DO.
    """
    def __hash__(self):
        assert(False)


    def __init__(self, gender, genetic_weight=0.5, genetic_strength=0.5, genetic_fatness=True, genetic_height=1.8, age = 18):
        # limbs
        self.gender = gender
        self.head = Head()
        self.lefteye = Eye()
        self.righteye = Eye()
        self.torso = Torso()
        self.leftleg = Leg()
        self.rightleg = Leg()
        self.leftarm = Arm()
        self.rightarm = Arm()
        self.age = age

        self.genetic_weight = genetic_weight # DO NOT MODIFY | FOR GENETICS ONLY
        self.genetic_strength = genetic_strength # DO NOT MODIFY | FOR GENETICS ONLY
        self.genetic_fatness = genetic_fatness # DO NOT MODIFY | FOR GENETICS ONLY
        self.genetic_height = genetic_height # DO NOT MODIFY | FOR GENETICS ONLY


        # performance attributes
        self.height = genetic_height
        self.strength = self.genetic_strength


        # fight variables
        self.health = BoundedNumber(100, 0, 100)
        self.stamina = BoundedNumber(100, 0, 100)

        self.stamina_cost_per_attack = 10


        # cosmetic (colours)
        self.skincolour = [(233,171,150,255), (194,129,111,255), (148,102,86,255), (107,75,64,255), (82,53,45,255)]
        self.eyecolour = [(106,190,48,255), (106,190,48,255)]
        self.haircolour = [(112,78,66,255), (89,61,51,255), (76,52,43,255)]

        # cosmetic (head, hair, beard, and nose id's)
        self.beard_id = False
        self.hairback_id = 1 # False for no hair
        self.hairfront_id = 1 # False for no hair
        self.headbottom_id = 1
        self.headtop_id = 1
        self.eye_id = 1
        self.nose_id = 1
        self.bodytype_id = 'strong'

        # extra genetic attributes
        self.geneticeyecolours = [self.eyecolour] # to prevent eyes averaging out to grey, children pull a random eye colour from their ancestors


    def get_eye_count(self):
        count = 0
        if self.lefteye.is_intact:
            count += 1
        if self.righteye.is_intact:
            count += 1
        return count

    def get_arm_count(self):
        count = 0
        if self.leftarm.is_intact:
            count += 1
        if self.rightarm.is_intact:
            count += 1
        return count


    def get_leg_count(self):
        count = 0
        if self.leftleg.is_intact:
            count += 1
        if self.rightleg.is_intact:
            count += 1
        return count

    def to_string(self):
        output = ""
        output += "health %s%% | stamina %s%%\n" % (round(self.health.get(), 2), round(self.stamina.get(), 2))
        output += "gender %s | age %s | strength %s | genetic_weight %s\n" % (self.gender, self.age, self.strength, self.genetic_weight)
        output += "limbs | eyes %s | arms %s | legs %s \n" % (self.get_eye_count(), self.get_arm_count(), self.get_leg_count())
        return output

