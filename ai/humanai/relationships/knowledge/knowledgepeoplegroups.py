from ai.humanai.relationships.knowledge.knowledge import Knowledge
from ai.humanai.relationships.information.informationlocationpeople import InformationLocationPeople
import random

class KnowledgePeopleGroups(Knowledge):

    """
    DO NOT DELETE THIS. PASTE THIS IN FOR EVERY NEW OBJECT THAT WILL BE STORED IN A SET/DICTIONARY.
    THIS IS ESSENTIAL FOR MAKING SURE THE PROGRAM PERFORMS EXACTLY THE SAME EVERY TIME!

    assert(false) WILL CRASH THE PROGRAM IF YOU ATTEMPT TO PUT THIS OBJECT INTO A SET/DICT WITHOUT FIRST MODIFYING THE FUNCTION.
    THIS IS DONE ON PURPOSE TO PREVENT YOU FROM ACCIDENTALLY LEAKING NON-DETERMINISM INTO THE PROGRAM.
    SPEAK TO ME (TOM) AND I WILL EXPLAIN WHAT TO DO.
    """
    def __hash__(self):
        assert(False)

    def __init__(self, knowledge_groups, knowledge_people):
        self.knowledge_people = knowledge_people
        self.knowledge_groups = knowledge_groups
        # self.last_known_people_groups = {} # {group : set(person)}



    """
    Basically if we previously have seen them in other group then remove then remove them from that
    group and register to their new one
    """
    def register_from_information(self, human, informationpersongroup):

        # remove them from old group
        old_person_group = self.knowledge_people.get_knowledge_of_person(informationpersongroup.person_id).group_id


        if old_person_group is not None:
            # no new info just ignore
            if informationpersongroup.group_id == old_person_group:
                return

            # existing_people_set = self.last_known_people_groups[old_person_group]
            self.knowledge_groups.get_knowledge_of_group(old_person_group).member_ids.remove(informationpersongroup.person_id)

        # add them
        self.knowledge_groups.get_knowledge_of_group(informationpersongroup.group_id).member_ids.add(informationpersongroup.person_id)
        self.knowledge_people.get_knowledge_of_person(informationpersongroup.person_id).group_id = informationpersongroup.group_id


    """
    Returns true if we know of a person is in same group
    """
    def is_in_same_group(self, person_id, group):
        person_group_id = self.knowledge_people.get_knowledge_of_person(person_id).group_id
        return group.id_number == person_group_id


    """
    Use this method to return a random piece of information
    that you can create from the knowledge. 
    This is for use in interactions, get_random_information may be called
    to simulate random conversation being passed.
    """
    def get_random_information(self):
        loc = random.choice(list(self.last_known_people_locations.keys()))
        return InformationLocationPeople(loc, self.get_people_at_location(loc))
