from abc import ABC, abstractmethod
from ai.groupai.bufferfactor.bufferfactor import BufferFactor
import global_params
from math import log
from entities.groupbase import GROUP_BUFFER_FACTOR


class BufferFactorSkillStats():

    """
    DO NOT DELETE THIS. PASTE THIS IN FOR EVERY NEW OBJECT THAT WILL BE STORED IN A SET/DICTIONARY.
    THIS IS ESSENTIAL FOR MAKING SURE THE PROGRAM PERFORMS EXACTLY THE SAME EVERY TIME!

    assert(false) WILL CRASH THE PROGRAM IF YOU ATTEMPT TO PUT THIS OBJECT INTO A SET/DICT WITHOUT FIRST MODIFYING THE FUNCTION.
    THIS IS DONE ON PURPOSE TO PREVENT YOU FROM ACCIDENTALLY LEAKING NON-DETERMINISM INTO THE PROGRAM.
    SPEAK TO ME (TOM) AND I WILL EXPLAIN WHAT TO DO.
    """
    def __hash__(self):
        assert(False)


    def __init__(self, skill):
        self.skill = skill
        # Storage statistics (used for buffer factors)
        self.amount_achieved = 0
        self.amount_required = 0

    def reset(self):
        self.amount_achieved = 0
        self.amount_required = 0

    def achieved(self, amount):
        self.amount_achieved += amount

    def __str__(self):
        if self.amount_required == 0:
            return "%s: NA" % self.skill

        return "%s: %s/%s" % (self.skill,
                                     self.amount_achieved,
                                     round(self.amount_required, 2))
    def __repr__(self):
        return str(self)

"""
A wrapper for performing an action, including a cost function, prerequisite conditions and worker logic.

ABC is a abstract base class.
Means we can never instantiate a BufferFactor object.
Instead we have to extend it, and complete the functions to do it. 
"""

"""
Resources 2 categories
Essential cell

Record all cell collected for one day : only on days they need.
"""

class BufferFactorSkill(BufferFactor):

    """
    DO NOT DELETE THIS. PASTE THIS IN FOR EVERY NEW OBJECT THAT WILL BE STORED IN A SET/DICTIONARY.
    THIS IS ESSENTIAL FOR MAKING SURE THE PROGRAM PERFORMS EXACTLY THE SAME EVERY TIME!

    assert(false) WILL CRASH THE PROGRAM IF YOU ATTEMPT TO PUT THIS OBJECT INTO A SET/DICT WITHOUT FIRST MODIFYING THE FUNCTION.
    THIS IS DONE ON PURPOSE TO PREVENT YOU FROM ACCIDENTALLY LEAKING NON-DETERMINISM INTO THE PROGRAM.
    SPEAK TO ME (TOM) AND I WILL EXPLAIN WHAT TO DO.
    """
    def __hash__(self):
        assert(False)

    def __init__(self, skill):
        super().__init__(skill) # ALWAYS CALL PARENT CONSTRUCTOR


    """
    Update the buffer factor
    """
    def daily_update(self, amount_needed, amount_collected, total_hours_float_allocation):

        if amount_collected == 0 and amount_needed == 0:
            return
        if amount_needed == 0:
            return

        print("food stats %s %s" % (amount_needed, amount_collected))

        file_object = open('bufferfactorresults.txt', 'a')
        # Append 'hello' at the end of file
        file_object.write("need: %s receive: %s\n" % (amount_needed, amount_collected))
        # Close the file
        file_object.close()


        """
        Not sure if this is a good fix, maybe the situation where this arises is a
        symptom of a larger bug, maybe not, but in a situation where they have been ordered to collect food
        yet somehow the amount_need is 0 then make it 1 such that we see a large change in buffer factor.
        """
        if amount_collected != 0 and amount_needed == 0:
            amount_needed = 1

        if amount_needed != 0 and amount_collected == 0:
            self.value *= 2

            if self.value >= global_params.DEFAULT_SURVIVAL_BUFFER_FACTOR:
                self.value = global_params.DEFAULT_SURVIVAL_BUFFER_FACTOR

            return

        # if self.skill == GROUP_BUFFER_FACTOR.FOOD_HARVESTING:


        # print("BUFFER FACTOR: %s" % self.skill)
        # print("Amount collected: %s" % amount_collected)
        # print("Amount needed: %s" % amount_needed)
        # print("Current value %s" % self.value)

        achieved = (amount_needed / amount_collected)
        # if achieved > 1 and total_hours_float_allocation >= 0.98:
        #     return
        # if achieved > 1:
            # self.value *= log(achieved, 2)
        # else:
        self.value *= achieved

        if self.value >= global_params.DEFAULT_SURVIVAL_BUFFER_FACTOR:
            self.value = global_params.DEFAULT_SURVIVAL_BUFFER_FACTOR


        return


    def __str__(self):
        return "%s" % (round(self.value, 2))

    def __repr__(self):
        return str(self)



