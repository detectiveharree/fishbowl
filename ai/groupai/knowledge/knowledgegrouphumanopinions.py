from sortedcollections import ValueSortedDict
from collections import Counter
from ai.humanai.relationships.interaction.interaction import INTERACTION_TYPE
from ai.humanai.relationships.humanopinions import HumanOpinions

"""
Class that providers rankings and helper functions for humans given a score.
"""

class KnowledgeGroupHumanOpinions(HumanOpinions):


    def __init__(self, group):
        super().__init__()
        self.group = group
        # basically overall score, but only for people within a group
        self.leadership_score_sorted = ValueSortedDict()


    """
    Updates a order for the most loved, feared and respected people known by all members of the group.
    Note: this function is expensive and should be called max once a day.
    """
    def update_opinions(self):
        """
        What we do is average all people's relationship levels with other people,
        then adjusting them by how many people know them
        (i.e. wouldn't make sense for person to be voted most loved if only one person knows them and really loves them)
        """
        self.most_love_sorted.clear()
        self.most_fear_sorted.clear()
        self.most_respect_sorted.clear()
        self.overall_score_sorted.clear()
        self.leadership_score_sorted.clear()

        known_people_counter = Counter()

        sum_love_score_counter = Counter()
        sum_fear_score_counter = Counter()
        sum_respect_score_counter = Counter()

        for person in self.group.members:
            # doesn't matter which we use (love, fear etc.) because if a person is known a score is maintained for
            # all of them
            known_people_counter.update(person.knowledge_of_people.human_opinions.most_love_sorted.keys())

            # count scores
            sum_love_score_counter.update(person.knowledge_of_people.human_opinions.most_love_sorted)
            sum_fear_score_counter.update(person.knowledge_of_people.human_opinions.most_fear_sorted)
            sum_respect_score_counter.update(person.knowledge_of_people.human_opinions.most_respect_sorted)

        # calculate most known person. We use this as a weight for voting.
        if not known_people_counter:
            return
        most_known_person_count = max(known_people_counter.values())

        for person_id in known_people_counter.keys():
            # if this person is most known will have score of 1 etc.
            amount_known_by_factor = known_people_counter[person_id] / most_known_person_count


            average_love_score = (sum_love_score_counter[person_id] / known_people_counter[person_id]) * amount_known_by_factor
            average_fear_score = (sum_fear_score_counter[person_id] / known_people_counter[person_id]) * amount_known_by_factor
            average_respect_score = (sum_respect_score_counter[person_id] / known_people_counter[person_id]) * amount_known_by_factor
            average_overall_score = (average_love_score + average_fear_score + average_respect_score) / 3

            self.most_love_sorted[person_id] = round(average_love_score, 2)
            self.most_fear_sorted[person_id] = round(average_fear_score, 2)
            self.most_respect_sorted[person_id] = round(average_respect_score, 2)
            self.overall_score_sorted[person_id] = round(average_overall_score, 2)

            # leaders can only be people in the group
            if person_id in self.group.member_ids:
                self.leadership_score_sorted[person_id] = round(average_overall_score, 2)
        self.group.knowledge_group_leader.get_new_leader()

    def to_string(self, amount):
        output = ""
        output += "%s loved | most %s | least %s\n" % (amount, self.get_n_most(self.most_love_sorted, amount), self.get_n_least(self.most_love_sorted, amount))
        output += "%s feared | most %s | least %s\n" % (amount, self.get_n_most(self.most_fear_sorted, amount), self.get_n_least(self.most_fear_sorted, amount))
        output += "%s respected | most %s | least %s\n" % (amount, self.get_n_most(self.most_respect_sorted, amount), self.get_n_least(self.most_respect_sorted, amount))
        output += "%s overall | most %s | least %s\n" % (amount, self.get_n_most(self.overall_score_sorted, amount), self.get_n_least(self.overall_score_sorted, amount))
        output += self.group.knowledge_group_leader.to_string(amount)
        return output