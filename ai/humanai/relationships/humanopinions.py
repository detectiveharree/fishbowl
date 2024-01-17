from sortedcollections import ValueSortedDict
from abc import ABC, abstractmethod
from ai.humanai.relationships.opinions import Opinions

"""
Class that providers rankings and helper functions for humans given a score.
"""

class HumanOpinions(Opinions):


    def __init__(self):
        self.most_love_sorted = ValueSortedDict()
        self.most_fear_sorted = ValueSortedDict()
        self.most_respect_sorted = ValueSortedDict()
        self.overall_score_sorted = ValueSortedDict()


    """
    Registers opinion
    """
    def register_new_score(self, human_id, love, fear, respect):
        self.most_love_sorted[human_id] = love
        self.most_fear_sorted[human_id] = fear
        self.most_respect_sorted[human_id] = respect
        self.overall_score_sorted[human_id] = round((love + fear + respect) / 3, 2)

    """
    Removes all knowledge of opinion
    """
    def remove_person(self, human_id):
        if human_id in self.most_respect_sorted.keys():
            del self.most_respect_sorted[human_id]
            del self.most_love_sorted[human_id]
            del self.most_fear_sorted[human_id]
            del self.overall_score_sorted[human_id]

    def decay_dict(self, valuesorteddict, decay_rate):
        for key, value in valuesorteddict.items():
            valuesorteddict[key] *= decay_rate
