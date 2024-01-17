from sortedcollections import ValueSortedDict
from ai.humanai.relationships.opinions import Opinions
from statistics import mean
import logging
from entities.group import GroupType
from ai.need import NEED_TYPE
import guiwindow
import global_params

class KnowledgeGroupOpinions(Opinions):

    def __init__(self, human):
        self.human = human

        """
        Food Buffer Factor
            -dependent on how hungry this person currently is? i.e. switch group if hungry | won't necessarily be case because dist is pretty good
        Water Buffer Factor
            -dependent on how thirsty this person currently is? i.e. switch group if thirsty | won't necessarily be case because dist is pretty good
        Fight score
            -dependent on how strong this person is i.e. a strong person knows he can fend for himself
            -dependent on how large other group is? I.e. a strong 3 man group in a climate of superpowers is not desirable
        Social Score
            -dependent on how social this person is i.e. some might not care about this
        Calculate Overall Score From This.
        """
        self.water_bf_score_sorted = ValueSortedDict()
        self.food_bf_score_sorted = ValueSortedDict()
        self.social_score_sorted = ValueSortedDict()
        self.fight_score_sorted = ValueSortedDict()
        self.overall_score_sorted = ValueSortedDict()

        # temp variable holding group knowledge that can have opinion for
        self.possible_groups = []



    def calculate_group_scores(self):

        # clear old stats
        self.water_bf_score_sorted.clear()
        self.food_bf_score_sorted.clear()
        self.social_score_sorted.clear()
        self.fight_score_sorted.clear()
        self.overall_score_sorted.clear()

        self.possible_groups = []

        # figure out groups that we can have opinion for
        for group_id in self.human.knowledge_groups.known_groups.keys():
            knowledge_group = self.human.knowledge_groups.get_knowledge_of_group(group_id)


            if self.can_have_opinion_for(knowledge_group):


                self.possible_groups.append(knowledge_group)


        # if there are group opinions continue
        if self.possible_groups:
            for knowledge_group in self.possible_groups:
                self.calculate_group_score(knowledge_group)


    """
    Returns true if a known group is allegable to have a opinion for
    """
    def can_have_opinion_for(self, knowledge_group):
        # if knowledge_group.id_number == self.human.own_group.id_number:
        #     print((knowledge_group.member_ids or knowledge_group.id_number == self.human.own_group.id_number))
        #     print(knowledge_group.group_type == GroupType.SETTLEMENT)
        #     print(knowledge_group.id_number in guiwindow.WORLD_INSTANCE.groups.keys())
        #     print(knowledge_group.believed_food_buffer_factor)
        #     print(knowledge_group.believed_water_buffer_factor)


        if knowledge_group.id_number == self.human.own_group.id_number:
            return True

        return (knowledge_group.member_ids) and\
                knowledge_group.group_type == GroupType.SETTLEMENT and\
                knowledge_group.id_number in guiwindow.WORLD_INSTANCE.groups.keys()




    """
    Calculate score for a group
    """
    def calculate_group_score(self, knowledge_group):

        # various verification
        # (group_id one is hacky)

        food_score, water_score = self.calculate_bf_score(knowledge_group)
        fight_score = self.get_fight_score(knowledge_group) # how to determine fight score?
        social_scores = self.get_social_score(knowledge_group)

        self.water_bf_score_sorted[knowledge_group.id_number] = water_score
        self.food_bf_score_sorted[knowledge_group.id_number] = food_score
        self.social_score_sorted[knowledge_group.id_number] = social_scores
        self.fight_score_sorted[knowledge_group.id_number] = fight_score
        self.overall_score_sorted[knowledge_group.id_number] = (social_scores + water_score + food_score + fight_score) / 4


    """
    Calculate weighted social score for group
    """
    def get_social_score(self, knowledge_group):

        """
        Own group case
        """
        if knowledge_group.id_number == self.human.own_group.id_number:
            return 1 - self.human.personality.social.as_percentage()

        social_scores = mean([(self.human.knowledge_of_people.human_opinions.most_love_sorted[person_id] +
                       self.human.knowledge_of_people.human_opinions.most_respect_sorted[person_id]) / 2
                       for person_id in knowledge_group.member_ids])

        # i.e. the more social the more weighting
        social_weighting_person = self.human.personality.social.as_percentage()

        return social_weighting_person * social_scores


    """
    Calculates buffer factor score for a group
    """
    def calculate_bf_score(self, knowledge_group):

        food_bf = 1 - (knowledge_group.believed_food_buffer_factor / global_params.DEFAULT_SURVIVAL_BUFFER_FACTOR)
        water_bf = 1 - (knowledge_group.believed_water_buffer_factor / global_params.DEFAULT_SURVIVAL_BUFFER_FACTOR)

        food_bf *= 2
        food_bf -= 1

        water_bf *= 2
        water_bf -= 1

        food_score = food_bf
        water_score = water_bf

        return food_score, water_score


    """
    Calculate weighted fight score for a certain group
    """
    def get_fight_score(self, knowledge_group):
        # sum all members kit scores
        total_member_score = 0
        human_strength_weighting = 1 - (self.human.needs[NEED_TYPE.TRAIN].current_kit_rating * self.human.body.strength)

        for member_id in knowledge_group.member_ids:
            human_knowledge = self.human.knowledge_of_people.get_knowledge_of_person(member_id)
            total_member_score += human_knowledge.current_kit_rating * human_knowledge.strength

        return total_member_score * human_strength_weighting



    def to_string(self, amount):
        output = ""
        output += "%s food | most %s | least %s\n" % (amount, self.get_n_most(self.food_bf_score_sorted, amount), self.get_n_least(self.food_bf_score_sorted, amount))
        output += "%s water | most %s | least %s\n" % (amount, self.get_n_most(self.water_bf_score_sorted, amount), self.get_n_least(self.water_bf_score_sorted, amount))
        output += "%s fight | most %s | least %s\n" % (amount, self.get_n_most(self.fight_score_sorted, amount), self.get_n_least(self.fight_score_sorted, amount))
        output += "%s social | most %s | least %s\n" % (amount, self.get_n_most(self.social_score_sorted, amount), self.get_n_least(self.social_score_sorted, amount))
        output += "%s best | most %s | least %s\n" % (amount, self.get_n_most(self.overall_score_sorted, amount), self.get_n_least(self.overall_score_sorted, amount))
        return output