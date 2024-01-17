

import guiwindow
import global_params


def get_proportion_progress_of_day():
    return guiwindow.WORLD_INSTANCE.time_day / global_params.daily_ticks

class TimeStamp():

    """
    DO NOT DELETE THIS. PASTE THIS IN FOR EVERY NEW OBJECT THAT WILL BE STORED IN A SET/DICTIONARY.
    THIS IS ESSENTIAL FOR MAKING SURE THE PROGRAM PERFORMS EXACTLY THE SAME EVERY TIME!

    assert(false) WILL CRASH THE PROGRAM IF YOU ATTEMPT TO PUT THIS OBJECT INTO A SET/DICT WITHOUT FIRST MODIFYING THE FUNCTION.
    THIS IS DONE ON PURPOSE TO PREVENT YOU FROM ACCIDENTALLY LEAKING NON-DETERMINISM INTO THE PROGRAM.
    SPEAK TO ME (TOM) AND I WILL EXPLAIN WHAT TO DO.
    """
    def __hash__(self):
        assert(False)

    def __init__(self):
        self.day = guiwindow.WORLD_INSTANCE.time_day
        self.hour = guiwindow.WORLD_INSTANCE.time_hour
        self.tick = guiwindow.WORLD_INSTANCE.time_ticks

    def convert_to_hours(self):
        return (self.day * 24) + self.hour

    def convert_to_ticks(self):
        amount = 0
        amount += global_params.daily_ticks * self.day
        amount += self.tick
        return amount

    def __str__(self):
        return "Day: %s | Hour %s" % (self.day, self.hour)

    def __repr__(self):
        return str(self)