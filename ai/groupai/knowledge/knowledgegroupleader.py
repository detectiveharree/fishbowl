import logging
from gameworld.timestamp import TimeStamp
"""
Class that providers rankings and helper functions for humans given a score.
"""

# To become the current leader you must achieve this
MIN_LEADER_CHANGE_GAP = 0.02

class KnowledgeGroupLeader():


    def __init__(self, group, knowledge_human_opinions):
        self.group = group
        self.knowledge_human_opinions = knowledge_human_opinions
        self.leader_id = None # in practice will NEVER be none
        self.leader_begin_daytime = TimeStamp()

    """
    Fix up opinions, give support for removing/adding people.
    Fill in functions for add member/lose member with leadership transfer
    """

    def member_added(self, human):
        if len(self.group.members) == 1:
            self.knowledge_human_opinions.update_opinions()
            self.get_new_leader()

    def member_removed(self, human):
        # only if still members
        if self.group.members:
            if human.id_number == self.leader_id:
                logging.info("%s who is leader of %s has left the group! Calling snap election!" % (human.id_number, self.group.id_number))
                self.leader_id = None
                self.knowledge_human_opinions.update_opinions()
                self.get_new_leader()
                pass

    def get_new_leader(self):
        best_new_leader = self.get_best_possible_leader()

        if self.leader_id is None or self.leader_id not in self.group.member_ids:
            self.choose_leader(best_new_leader)
            return

        best_new_leader_score = self.knowledge_human_opinions.leadership_score_sorted[best_new_leader]
        current_leader_score = self.knowledge_human_opinions.leadership_score_sorted[self.leader_id]

        if best_new_leader_score > (current_leader_score + MIN_LEADER_CHANGE_GAP):
            self.choose_leader(best_new_leader)

    """
    Returns the best possible leader
    """
    def get_best_possible_leader(self):
        return self.knowledge_human_opinions.get_best(self.knowledge_human_opinions.leadership_score_sorted)

    def choose_leader(self, human_id):
        if human_id != self.leader_id:
            self.leader_id = human_id
            logging.info("%s is now the leader of %s!" % (self.leader_id, self.group.id_number))
            self.leader_begin_daytime = TimeStamp()


    def to_string(self, amount):
        output = ""
        output += "potential (%s) leaders: %s\n" % (amount, self.knowledge_human_opinions.get_n_most(self.knowledge_human_opinions.leadership_score_sorted, amount))
        output += "current leader: %s\n" % (self.leader_id)
        output += "leader started: %s\n" % (self.leader_begin_daytime)
        return output

