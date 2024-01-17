from ai.groupai.task.taskgroupdaily import TaskGroupDaily
from ai.groupai.actions.actiongrouphourlyskilledgetresource import ActionGroupHourlySkilledGetResource
import global_params
from items.itemresources.itemresource import ResourceType
from ai.groupai.needs.needgroup import GROUP_NEED_TYPE
from gameworld.timestamp import TimeStamp, get_proportion_progress_of_day
import guiwindow


"""
Task for consuming a resource
"""
class TaskGroupGetDaySurvivalWater(TaskGroupDaily):

    """
    DO NOT DELETE THIS. PASTE THIS IN FOR EVERY NEW OBJECT THAT WILL BE STORED IN A SET/DICTIONARY.
    THIS IS ESSENTIAL FOR MAKING SURE THE PROGRAM PERFORMS EXACTLY THE SAME EVERY TIME!

    assert(false) WILL CRASH THE PROGRAM IF YOU ATTEMPT TO PUT THIS OBJECT INTO A SET/DICT WITHOUT FIRST MODIFYING THE FUNCTION.
    THIS IS DONE ON PURPOSE TO PREVENT YOU FROM ACCIDENTALLY LEAKING NON-DETERMINISM INTO THE PROGRAM.
    SPEAK TO ME (TOM) AND I WILL EXPLAIN WHAT TO DO.
    """
    def __hash__(self):
        return hash(self.hash_id)

    def __eq__(self, other):
        return self.__class__ == other.__class__ and self.hash_id == other.hash_id

    def __init__(self, group, need_type, need_level):
        super(). __init__(need_level, need_type)
        self.hash_id = guiwindow.WORLD_INSTANCE.task_get_survival_resources_id_counter
        guiwindow.WORLD_INSTANCE.task_get_survival_resources_id_counter += 1
        self.group = group
        self.last_day_triggered = None

        # total amount of cell left required to complete days cell
        self.amount_water_to_collect = 0

        # total amount of cell to collect for whole day
        self.amount_water_collect_today = 0

        # total amount of cell to collected so far this day
        self.amount_water_collected_today = 0

        self.water_storage = self.contents[ResourceType.WATER]


    """
    Called at start of pre-activation 
    i.e. activatable_when just became True
    """
    def trigger(self, group):

        """
        Every day, amount collected stats must be reset.
        Figure out collection targets for the day, taking into account
        any leftover cell from yesterday
        """
        if self.last_day_triggered != TimeStamp().day:

            self.amount_water_collected_today = 0

            # Max amount of water we need today
            self.water_storage.max_amount = global_params.thirst_tick * \
                                        global_params.daily_ticks * \
                                        len(self.group.members) * \
                                        global_params.supply_days

            # net amount of water to collect given start of dat storage
            self.amount_water_to_collect = max(0, self.water_storage.max_amount - self.water_storage.storage)

            # stats
            self.amount_water_collect_today = self.amount_water_to_collect

            # record when last triggered
            self.last_day_triggered = TimeStamp().day

            # reset storage stats
            self.reset_storage_statistics()

        # record what has been previously collected today
        self.amount_water_collected_today += self.water_storage.amount_collected

        # set amount to collect to account for previous collection
        self.amount_water_to_collect = max(0, self.amount_water_to_collect - self.water_storage.amount_collected)

        # reset storage stats
        self.reset_storage_statistics()

        # set goal for current session
        self.water_storage.amount_goal = self.amount_water_to_collect

        pass


    """
    Called when the action is activated
    """
    def begin(self, group):
        pass


    """
    Must return True/False
    If true, resets the progress of all actions and the action queue
    every time this task is activated i.e. activate() function is called 
    Action queue will be assigned to possible_actions().
    """
    def reset_action_tree_on_activation(self):
        return True


    """
    Returns true/false if this entire task is complete
    """
    def is_task_complete(self, group):
        """
        This task is never complete.
        """
        return False

    """
    Possible actions that the user can do to satisfy this pre requisite.
    Note the action with the cheapest action tree will be picked.
    """
    def possible_actions(self):

        actions = []

        if self.amount_water_to_collect > 0:
            actions.append(ActionGroupHourlySkilledGetResource(ResourceType.WATER, self.amount_water_to_collect, self))

        return [actions]

    def __repr__(self):
        start = str("Survival water supply %s days (w: %s/%s)" % (global_params.supply_days,
                                                                      int(self.water_storage.storage),
                                                                      int(self.water_storage.max_amount),))
        if self.amount_water_collect_today == 0:
            return start
        return start + " | \n    water %s/%s (%s%%)" % (int(self.amount_water_collected_today + self.water_storage.amount_collected),
                                                                          int(self.amount_water_collect_today),
                                                    int(((self.amount_water_collected_today + self.water_storage.amount_collected)
                                                         / self.amount_water_collect_today) * 100))