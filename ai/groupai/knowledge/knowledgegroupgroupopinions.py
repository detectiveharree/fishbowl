from ai.humanai.relationships.opinions import Opinions
from sortedcollections import ValueSortedDict
from collections import Counter

class KnowledgeGroupGroupOpinions(Opinions):

    def __init__(self, group):
        self.group = group
        """
        Hate/Love for other group (dependent on human's average love/hate for them)
        """


        pass
        self.social_score_sorted = ValueSortedDict() # social score is combo of love + respect
        self.overall_score_sorted = ValueSortedDict()


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
        self.social_score_sorted.clear()
        self.overall_score_sorted.clear()

        known_group_counter = Counter()

        sum_social_score_counter = Counter()

        for person in self.group.members:
            # doesn't matter which we use (love, fear etc.) because if a person is known a score is maintained for
            # all of them
            known_group_counter.update(person.knowledge_groups.group_opinions.overall_score_sorted.keys())

            # count scores
            sum_social_score_counter.update(person.knowledge_groups.group_opinions.social_score_sorted)

        # calculate most known person. We use this as a weight for voting.
        if not known_group_counter:
            return

        most_known_person_count = max(known_group_counter.values())

        for group_id in known_group_counter.keys():

            if group_id == self.group.id_number:
                continue

            # if this person is most known will have score of 1 etc.
            amount_known_by_factor = known_group_counter[group_id] / most_known_person_count

            average_social_score = (sum_social_score_counter[group_id] / known_group_counter[group_id]) * amount_known_by_factor
            average_overall_score = average_social_score

            self.social_score_sorted[group_id] = round(average_social_score, 2)
            self.overall_score_sorted[group_id] = round(average_overall_score, 2)


    def to_string(self, amount):
        output = ""
        output += "%s social | most %s | least %s\n" % (amount, self.get_n_most(self.social_score_sorted, amount), self.get_n_least(self.social_score_sorted, amount))
        output += "%s best | most %s | least %s\n" % (amount, self.get_n_most(self.overall_score_sorted, amount), self.get_n_least(self.overall_score_sorted, amount))
        return output