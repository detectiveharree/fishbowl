
from ai.humanai.relationships.attributes.attributes import ScaleAttribute, BinaryAttribute
from enum import Enum


class PERSONALITY_PRESET(Enum):
    DEFAULT = 1
    ARABIAN = 2
    AFRICAN = 3

    def __repr__(self):
        return self.name


class AgreeablenessAttribute(ScaleAttribute):

    """
    DO NOT DELETE THIS. PASTE THIS IN FOR EVERY NEW OBJECT THAT WILL BE STORED IN A SET/DICTIONARY.
    THIS IS ESSENTIAL FOR MAKING SURE THE PROGRAM PERFORMS EXACTLY THE SAME EVERY TIME!

    assert(false) WILL CRASH THE PROGRAM IF YOU ATTEMPT TO PUT THIS OBJECT INTO A SET/DICT WITHOUT FIRST MODIFYING THE FUNCTION.
    THIS IS DONE ON PURPOSE TO PREVENT YOU FROM ACCIDENTALLY LEAKING NON-DETERMINISM INTO THE PROGRAM.
    SPEAK TO ME (TOM) AND I WILL EXPLAIN WHAT TO DO.
    """
    def __hash__(self):
        assert(False)

    def __init__(self, value):
        super().__init__("Disagreeable", "Agreeable", value)


class SocialAttribute(ScaleAttribute):

    """
    DO NOT DELETE THIS. PASTE THIS IN FOR EVERY NEW OBJECT THAT WILL BE STORED IN A SET/DICTIONARY.
    THIS IS ESSENTIAL FOR MAKING SURE THE PROGRAM PERFORMS EXACTLY THE SAME EVERY TIME!

    assert(false) WILL CRASH THE PROGRAM IF YOU ATTEMPT TO PUT THIS OBJECT INTO A SET/DICT WITHOUT FIRST MODIFYING THE FUNCTION.
    THIS IS DONE ON PURPOSE TO PREVENT YOU FROM ACCIDENTALLY LEAKING NON-DETERMINISM INTO THE PROGRAM.
    SPEAK TO ME (TOM) AND I WILL EXPLAIN WHAT TO DO.
    """
    def __hash__(self):
        assert(False)

    def __init__(self, value):
        super().__init__("Introvert", "Extrovert", value)

class CarelessnessAttribute(ScaleAttribute):

    """
    DO NOT DELETE THIS. PASTE THIS IN FOR EVERY NEW OBJECT THAT WILL BE STORED IN A SET/DICTIONARY.
    THIS IS ESSENTIAL FOR MAKING SURE THE PROGRAM PERFORMS EXACTLY THE SAME EVERY TIME!

    assert(false) WILL CRASH THE PROGRAM IF YOU ATTEMPT TO PUT THIS OBJECT INTO A SET/DICT WITHOUT FIRST MODIFYING THE FUNCTION.
    THIS IS DONE ON PURPOSE TO PREVENT YOU FROM ACCIDENTALLY LEAKING NON-DETERMINISM INTO THE PROGRAM.
    SPEAK TO ME (TOM) AND I WILL EXPLAIN WHAT TO DO.
    """
    def __hash__(self):
        assert(False)

    def __init__(self, value):
        super().__init__("Careless", "Organised", value)

class NeuroticismAttribute(ScaleAttribute):

    """
    DO NOT DELETE THIS. PASTE THIS IN FOR EVERY NEW OBJECT THAT WILL BE STORED IN A SET/DICTIONARY.
    THIS IS ESSENTIAL FOR MAKING SURE THE PROGRAM PERFORMS EXACTLY THE SAME EVERY TIME!

    assert(false) WILL CRASH THE PROGRAM IF YOU ATTEMPT TO PUT THIS OBJECT INTO A SET/DICT WITHOUT FIRST MODIFYING THE FUNCTION.
    THIS IS DONE ON PURPOSE TO PREVENT YOU FROM ACCIDENTALLY LEAKING NON-DETERMINISM INTO THE PROGRAM.
    SPEAK TO ME (TOM) AND I WILL EXPLAIN WHAT TO DO.
    """
    def __hash__(self):
        assert(False)

    def __init__(self, value):
        super().__init__("Nervous", "Confident", value)


class CharismaAttribute(ScaleAttribute):

    """
    DO NOT DELETE THIS. PASTE THIS IN FOR EVERY NEW OBJECT THAT WILL BE STORED IN A SET/DICTIONARY.
    THIS IS ESSENTIAL FOR MAKING SURE THE PROGRAM PERFORMS EXACTLY THE SAME EVERY TIME!

    assert(false) WILL CRASH THE PROGRAM IF YOU ATTEMPT TO PUT THIS OBJECT INTO A SET/DICT WITHOUT FIRST MODIFYING THE FUNCTION.
    THIS IS DONE ON PURPOSE TO PREVENT YOU FROM ACCIDENTALLY LEAKING NON-DETERMINISM INTO THE PROGRAM.
    SPEAK TO ME (TOM) AND I WILL EXPLAIN WHAT TO DO.
    """
    def __hash__(self):
        assert(False)

    def __init__(self, value):
        super().__init__("Dull", "Charismatic", value)


MAX_PERSONALITY_DIFFERENCE_CONSTANT = AgreeablenessAttribute.max_difference() +\
                                      SocialAttribute.max_difference() +\
                                      NeuroticismAttribute.max_difference() +\
                                      CarelessnessAttribute.max_difference() +\
                                      CharismaAttribute.max_difference()

"""
Neuroticism
90% of people between -1 and +0.5

rand = np.random.normal(0,1)
rand *= (0.72/1.65)
rand -= 0.25 # (for women you can minus 0.15 instead)
"""

"""
Social

30% of people introverted (<0): make it less so if female? (15% for female)


"""

"""
Carelessness

Male 35%, female 20% 
risk takers (i.e. carelessness below 0): decreases in age?

Male
35% uniform below 0
65% normal (0.5, 0.5)

Female
25% uniform below 0
75% normal (0.5, 0.5)

"""


"""
Charisma
10% of people have high leadership skills ( 0.8 < charisma < 1) (Normal 0.9, 0.1)
20% have medium to high leadership skills ( 0.4 < charisma < 0.8) (Normal 0.6, 0.2)
70% uniform (-1 < charisma < 0.4)

"""



"""
curiosity

Normal (0, 1)
(we will decrease this with age) 
"""
class PersonalityAttributes():

    """
    DO NOT DELETE THIS. PASTE THIS IN FOR EVERY NEW OBJECT THAT WILL BE STORED IN A SET/DICTIONARY.
    THIS IS ESSENTIAL FOR MAKING SURE THE PROGRAM PERFORMS EXACTLY THE SAME EVERY TIME!

    assert(false) WILL CRASH THE PROGRAM IF YOU ATTEMPT TO PUT THIS OBJECT INTO A SET/DICT WITHOUT FIRST MODIFYING THE FUNCTION.
    THIS IS DONE ON PURPOSE TO PREVENT YOU FROM ACCIDENTALLY LEAKING NON-DETERMINISM INTO THE PROGRAM.
    SPEAK TO ME (TOM) AND I WILL EXPLAIN WHAT TO DO.
    """
    def __hash__(self):
        assert(False)

    def __init__(self, agreeableness=0, social=0, neuroticism = 0, carelessness = 0, charisma = 0):
        self.agreeable = AgreeablenessAttribute(agreeableness)
        self.social = SocialAttribute(social)
        self.neuroticism = NeuroticismAttribute(neuroticism)
        self.carelessness = CarelessnessAttribute(carelessness)
        self.charisma = CharismaAttribute(charisma)


    """
    Similarity score between two different personality groups.
    The larger the number the less similar.
    """
    def similarity(self, other):
        differences = 0
        differences += self.agreeable.difference(other.agreeable)
        differences += self.social.difference(other.social)
        differences += self.neuroticism.difference(other.neuroticism)
        differences += self.carelessness.difference(other.carelessness)
        differences += self.charisma.difference(other.charisma)
        return differences

    def get_colour(self):
        r = ((self.agreeable.value + 1) / 2) * 255
        g = ((self.social.value + 1) / 2) * 255
        b = ((self.neuroticism.value + 1) / 2) * 255
        return (r, g, b)

    def to_string(self):
        output = f'agreeable: {self.agreeable.value},' \
                 f' social: {self.social.value},' \
                 f' neuroticism: {self.neuroticism.value},' \
                 f' carelessness: {self.carelessness.value},' \
                 f' charisma {self.charisma.value}'
        return output


class PersonalityAttributesPreset():

    """
    DO NOT DELETE THIS. PASTE THIS IN FOR EVERY NEW OBJECT THAT WILL BE STORED IN A SET/DICTIONARY.
    THIS IS ESSENTIAL FOR MAKING SURE THE PROGRAM PERFORMS EXACTLY THE SAME EVERY TIME!

    assert(false) WILL CRASH THE PROGRAM IF YOU ATTEMPT TO PUT THIS OBJECT INTO A SET/DICT WITHOUT FIRST MODIFYING THE FUNCTION.
    THIS IS DONE ON PURPOSE TO PREVENT YOU FROM ACCIDENTALLY LEAKING NON-DETERMINISM INTO THE PROGRAM.
    SPEAK TO ME (TOM) AND I WILL EXPLAIN WHAT TO DO.
    """
    def __hash__(self):
        assert(False)

    def __init__(self, agreeableness=0, social=0, neuroticism = 0, carelessness = 0, charisma = 0):
        self.agreeable = AgreeablenessAttribute(agreeableness)
        self.social = SocialAttribute(social)
        self.neuroticism = NeuroticismAttribute(neuroticism)
        self.carelessness = CarelessnessAttribute(carelessness)
        self.charisma = CharismaAttribute(charisma)

