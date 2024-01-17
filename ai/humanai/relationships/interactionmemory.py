import pandas as pd
import numexpr as ne
# pd.set_option('mode.chained_assignment', None)
pd.set_option('max_columns', None)
max_size = 50


class InteractionMemoryCache():

    def __init__(self):
        self.df = pd.DataFrame(columns=["Love", "Fear", "Respect", "Significance", "Interaction", "InteractionID"], index=range(0, max_size)).fillna(0)
        # generate unique negative placeholder interaction ids
        # negative because real interaction ids are guaruanteed to be positive
        interaction_id_unique_placeholders = range(0, -max_size, -1)
        self.df["InteractionID"] = interaction_id_unique_placeholders
        # cache interaction ids to table indexes
        # start by loading it in with placeholder indexes for empty interaction ids
        self.interaction_to_index_cache = dict([(unique_id, None) for unique_id in interaction_id_unique_placeholders]) # {interaction_id : table_index}



    """
    Registers a interaction memory.
    Will kick out the least significant memory if memory is full.
    Will update a existing interaction if has same id
    
    This function is pretty optimised
    """
    def register_interaction(self, love, fear, respect, interaction_info):
        total = abs(love) + abs(fear) + abs(respect)

        # check interaction id cache to quickly retrieve table index for previously registered interaction id
        if interaction_info.interaction_id in self.interaction_to_index_cache.keys():
            old_index = self.interaction_to_index_cache[interaction_info.interaction_id]
            self.df.loc[old_index] = [love, fear, respect, total, interaction_info,
                                                interaction_info.interaction_id]
            return

        # now just replace the existing interaction with the lowest significance
        current_min_index = self.df["Significance"].idxmin()
        # if smallest value is still larger then the item, skip it
        if self.df.at[current_min_index, "Significance"] > total:
            return

        # delete old cached value for interacton_id
        del self.interaction_to_index_cache[self.df.at[current_min_index, "InteractionID"]]
        # update new cache value with new current min index
        self.interaction_to_index_cache[interaction_info.interaction_id] = current_min_index
        # replace row with minimum value
        self.df.loc[current_min_index] = [love, fear, respect, total, interaction_info, interaction_info.interaction_id]

    """
    Get scaled relationship scores of love, fear and respect
    Returned as tuple (love, fear, respect)
    
    This function could probably be optimised more.
    """
    def get_scaled_relationship_scores(self):

        def plus(val):
            return val[val > 0].sum()

        def neg(val):
            return val[val < 0].sum()


        def calculate_scaled_score(column):
            positives = self.df[column].agg(plus)
            negatives = self.df[column].agg(neg)

            if negatives == 0 and positives == 0:
                return 0
            elif negatives == 0:
                negatives = 1
            elif positives == 0:
                positives = 1

            positive_ratio = positives / (positives + abs(negatives))
            return (positive_ratio * 2) - 1


        love_score = calculate_scaled_score("Love")
        fear_score = calculate_scaled_score("Fear")
        respect_score = calculate_scaled_score("Respect")

        return (round(love_score, 2), round(fear_score, 2), round(respect_score, 2))

    """
    Decays the memory by some constant
    """

    def decay(self, decay_rate):
        pass

        a = self.df["Love"]
        b = self.df["Fear"]
        c = self.df["Respect"]
        d = self.df["Significance"]
        # numexpr is a super fast way
        # of executing series computation (way faster then pd default)
        # look it up
        ne.evaluate("a * %s" % (decay_rate))
        ne.evaluate("b * %s" % (decay_rate))
        ne.evaluate("c * %s" % (decay_rate))
        ne.evaluate("d * %s" % (decay_rate))
