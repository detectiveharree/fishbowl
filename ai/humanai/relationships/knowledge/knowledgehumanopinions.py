from sortedcollections import ValueSortedDict
from collections import Counter
from ai.humanai.relationships.interaction.interaction import INTERACTION_TYPE
from ai.humanai.relationships.humanopinions import HumanOpinions
from ai.humanai.relationships.knowledge.knowledge import Knowledge

"""
Class that providers rankings and helper functions for humans given a score.
"""


min_lover_score = 0.7
min_romance_row = 10

class KnowledgeHumanOpinions(HumanOpinions):


    def __init__(self, human):
        super().__init__()
        self.human = human
        self.potential_lovers_sorted = ValueSortedDict() # mix of love + respect only if they're opposite gender
        self.interaction_counts = { interaction_type:ValueSortedDict() for interaction_type in list(INTERACTION_TYPE)}
        self.lover_id = None
        self.last_romanced_id = None
        self.last_romanced_row = 0


    def decay(self, decay_rate):
        self.decay_dict(self.most_love_sorted, decay_rate)
        self.decay_dict(self.most_respect_sorted, decay_rate)
        self.decay_dict(self.most_fear_sorted, decay_rate)
        self.decay_dict(self.overall_score_sorted, decay_rate)
        self.decay_dict(self.potential_lovers_sorted, decay_rate)

    """
    Registers opinion
    """
    def register_new_score(self, human_id, love, fear, respect):
        super().register_new_score(human_id, love, fear, respect)
        self.register_potential_lover_score(human_id, love, respect)

    """
    Removes all knowledge of opinion
    """
    def remove_person(self, human_id):
        super().remove_person(human_id)
        if human_id in self.potential_lovers_sorted.keys():
            del self.potential_lovers_sorted[human_id]


    def register_potential_lover_score(self, human_id, love, respect):

        knowledge_of_other_person = self.human.knowledge_of_people.get_knowledge_of_person(human_id)

        if self.human.body.gender == knowledge_of_other_person.gender:
            return
        score = round((love + respect) / 2, 2)
        if score < 0:
            if knowledge_of_other_person.id_number in self.potential_lovers_sorted.keys():
                del self.potential_lovers_sorted[knowledge_of_other_person.id_number]
        else:
            self.potential_lovers_sorted[knowledge_of_other_person.id_number] = score


    def register_romance(self, other_person_id):
        if self.last_romanced_id != other_person_id:
            self.last_romanced_row = 0

        self.last_romanced_id = other_person_id

        # if still a potential lover
        if self.last_romanced_id in self.potential_lovers_sorted.keys():
            self.last_romanced_row += 1
            print("Dating %s | Dates %s/%s | Lover score %s/%s \n" % (self.last_romanced_id, self.last_romanced_row, min_romance_row,
                                                                           self.potential_lovers_sorted[self.last_romanced_id], min_lover_score,))
            self.calculate_lover()

    def calculate_lover(self):

        if self.last_romanced_row < min_romance_row:
            return

        love_score = self.most_love_sorted[self.last_romanced_id]
        respect_score = self.most_love_sorted[self.last_romanced_id]
        score = round((love_score + respect_score) / 2, 2)


        if score < min_lover_score:
            return
        self.lover_id = self.last_romanced_id


    def get_best_potential_lover(self):
        return self.get_best(self.potential_lovers_sorted)


    def to_string(self, amount):
        output = ""
        output += "%s loved | most %s | least %s\n" % (amount, self.get_n_most(self.most_love_sorted, amount), self.get_n_least(self.most_love_sorted, amount))
        output += "%s feared | most %s | least %s\n" % (amount, self.get_n_most(self.most_fear_sorted, amount), self.get_n_least(self.most_fear_sorted, amount))
        output += "%s respected | most %s | least %s\n" % (amount, self.get_n_most(self.most_respect_sorted, amount), self.get_n_least(self.most_respect_sorted, amount))
        output += "%s pot lovers | most %s | least %s\n" % (amount, self.get_n_most(self.potential_lovers_sorted, amount), self.get_n_least(self.potential_lovers_sorted, amount))
        output += "%s overall | most %s | least %s\n" % (amount, self.get_n_most(self.overall_score_sorted, amount), self.get_n_least(self.overall_score_sorted, amount))

        output += "%s chatted | most %s | least %s\n" % (amount, self.get_n_most(self.interaction_counts[INTERACTION_TYPE.CHAT], amount), self.get_n_least(self.interaction_counts[INTERACTION_TYPE.CHAT], amount))
        output += "%s bantered | most %s | least %s\n" % (amount, self.get_n_most(self.interaction_counts[INTERACTION_TYPE.BANTER], amount), self.get_n_least(self.interaction_counts[INTERACTION_TYPE.BANTER], amount))
        output += "%s romanced | most %s | least %s\n" % (amount, self.get_n_most(self.interaction_counts[INTERACTION_TYPE.ROMANCE], amount), self.get_n_least(self.interaction_counts[INTERACTION_TYPE.ROMANCE], amount))
        output += "%s fought (battle) | most %s | least %s\n" % (amount, self.get_n_most(self.interaction_counts[INTERACTION_TYPE.FIGHT_BATTLE], amount), self.get_n_least(self.interaction_counts[INTERACTION_TYPE.FIGHT_BATTLE], amount))
        output += "%s fought (brawl) | most %s | least %s\n" % (amount, self.get_n_most(self.interaction_counts[INTERACTION_TYPE.FIGHT_BRAWL], amount), self.get_n_least(self.interaction_counts[INTERACTION_TYPE.FIGHT_BRAWL], amount))
        output += "%s fought (training) | most %s | least %s\n" % (amount, self.get_n_most(self.interaction_counts[INTERACTION_TYPE.FIGHT_TRAINING], amount), self.get_n_least(self.interaction_counts[INTERACTION_TYPE.FIGHT_TRAINING], amount))
        output += "%s insulted | most %s | least %s\n" % (amount, self.get_n_most(self.interaction_counts[INTERACTION_TYPE.INSULT], amount), self.get_n_least(self.interaction_counts[INTERACTION_TYPE.INSULT], amount))
        output += "Dating %s | Dates %s/%s | Lover score %s/%s \n" % (self.last_romanced_id, self.last_romanced_row, min_romance_row,
                                                                           self.potential_lovers_sorted[self.last_romanced_id] if self.last_romanced_id in self.potential_lovers_sorted.keys() else None, min_lover_score,)
        output += "Lover %s \n" % (self.lover_id)
        return output