from ai.humanai.relationships.knowledge.knowledgegroup import KnowledgeGroup
from ai.humanai.relationships.knowledge.knowledgehumangroupopinions import KnowledgeGroupOpinions
import logging
import guiwindow
from entities.groupbase import GroupType

MIN_GROUP_CHANGE_GAP = 0.02

"""
The knowledge of all people
"""
class KnowledgeGroups():

    """
    DO NOT DELETE THIS. PASTE THIS IN FOR EVERY NEW OBJECT THAT WILL BE STORED IN A SET/DICTIONARY.
    THIS IS ESSENTIAL FOR MAKING SURE THE PROGRAM PERFORMS EXACTLY THE SAME EVERY TIME!

    assert(false) WILL CRASH THE PROGRAM IF YOU ATTEMPT TO PUT THIS OBJECT INTO A SET/DICT WITHOUT FIRST MODIFYING THE FUNCTION.
    THIS IS DONE ON PURPOSE TO PREVENT YOU FROM ACCIDENTALLY LEAKING NON-DETERMINISM INTO THE PROGRAM.
    SPEAK TO ME (TOM) AND I WILL EXPLAIN WHAT TO DO.
    """
    def __hash__(self):
        assert(False)


    def __init__(self, human):
        self.known_groups = {} # {group_id : KnowledgeGroup}
        self.group_opinions = KnowledgeGroupOpinions(human)

    def amount_known_groups(self):
        return len(self.known_groups.keys())

    """
    See get_knowledge_of_people
    """
    def register_from_information(self, human):
        ...

    def knows_group(self, group_id):
        return group_id in self.known_groups.keys()

    """
    Register a empty version of a group if not known already
    """
    def register_knowledge_of_group(self, group_id):
        assert(group_id != -1)
        assert(isinstance(group_id, int))
        if not self.knows_group(group_id):
            know_person = KnowledgeGroup(group_id)
            self.known_groups[group_id] = know_person
            # important to record thme as 0
            # self.group_opinions.calculate_group_score(group_id)

    """
    Theres so many opportunities for a person to first hear about another person,
    that its not feasable to register a person through the register_from_information function
    (because every time we call get_knowledge_of_person we will need to check knows_person
    and call register_from_information if fails).
    Therefore we make an exception for knowledge of people and register a new person whenever
    we call get_knowledge_of_person
    """
    def get_knowledge_of_group(self, group_id):
        self.register_knowledge_of_group(group_id)
        return self.known_groups[group_id]


    """
    Returns the best possible leader
    """
    def get_best_possible_group(self):
        return self.group_opinions.get_best(self.group_opinions.overall_score_sorted)

    """
    Tries to join the best group
    """
    def join_best_group(self, human):
        # if knows of any groups
        if self.group_opinions.overall_score_sorted:

            # if in rally group proceed as fine
            # else if in settlement, and opinion of current group not done yet (if just switched might not have)

            # don't join group from rally point
            if human.group.group_type == GroupType.RALLY_POINT:
                return

            best_new_group = self.get_best_possible_group()
            best_new_group_score = self.group_opinions.overall_score_sorted[best_new_group]


            if human.group.id_number in self.group_opinions.overall_score_sorted:
                current_group_score = self.group_opinions.overall_score_sorted[human.group.id_number]
                if best_new_group_score > (current_group_score + MIN_GROUP_CHANGE_GAP):
                    logging.info("%s is attempting to switch group in night group %s -> %s" % (human.id_number, human.group.id_number, best_new_group))
                    if best_new_group == human.own_group.id_number:
                        human.group.attempt_switch_group(human, human.own_group)
                    else:
                        human.group.attempt_switch_group(human, guiwindow.WORLD_INSTANCE.groups[best_new_group])
                    #self.choose_leader(best_new_leader)
            else:
                # aka joining from rally group or something
                logging.info("%s is attempting to switch group in night group %s -> %s" % (
                human.id_number, human.group.id_number, best_new_group))
                if best_new_group == human.own_group.id_number:
                    human.group.attempt_switch_group(human, human.own_group)
                else:
                    human.group.attempt_switch_group(human, guiwindow.WORLD_INSTANCE.groups[best_new_group])

