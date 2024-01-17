from ai.prerequisite import Prerequisite
import math

"""
Is the human knows of a resource location that is currently empty.

A Prerequisite is a predicate that must be true to complete a action.
It is a prediction/estimation based on information that a human has, 
that is used when a human undergoes decision making. Therefore, 
DO NOT leak information that the human does not know i.e. world data.
"""
class PrerequisiteKnowsPersonLocation(Prerequisite):


    """
    DO NOT DELETE THIS. PASTE THIS IN FOR EVERY NEW OBJECT THAT WILL BE STORED IN A SET/DICTIONARY.
    THIS IS ESSENTIAL FOR MAKING SURE THE PROGRAM PERFORMS EXACTLY THE SAME EVERY TIME!

    assert(false) WILL CRASH THE PROGRAM IF YOU ATTEMPT TO PUT THIS OBJECT INTO A SET/DICT WITHOUT FIRST MODIFYING THE FUNCTION.
    THIS IS DONE ON PURPOSE TO PREVENT YOU FROM ACCIDENTALLY LEAKING NON-DETERMINISM INTO THE PROGRAM.
    SPEAK TO ME (TOM) AND I WILL EXPLAIN WHAT TO DO.
    """
    def __hash__(self):
        assert(False)


    def __init__(self, target_person_id):
        self.target_person_id = target_person_id


    """
    Returns a list of possible actions that may satisfy this prerequisite.
    """
    def possible_actions(self, human):
        return []

    """
    Return known locations of resource
    """
    def get_data(self, human):
        return human.knowledge_of_people.get_knowledge_of_person(self.target_person_id).location

    """
    Returns true/false if the current prerequisite is satisfied.
    """
    def is_satisfied(self, human):
        return human.knowledge_of_people.get_knowledge_of_person(self.target_person_id).location is not None



