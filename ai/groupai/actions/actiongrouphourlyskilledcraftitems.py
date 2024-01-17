from ai.groupai.actions.actiongroup import ActionGroup
from ai.groupai.actions.actiongrouphourlyskilled import ActionGroupHourlySkilled
from ai.humanai.task.taskcraftitems import TaskCraftItems
from ai.humanai.task.taskbringresourcetogroup import TaskBringResourceToGroup
from ai.humanai.task.taskbuildbuilding import TaskBuildBuilding
import global_params
from collections import OrderedDict
from ai.humanai.skill import SKILL_TYPE
from ai.need import NEED_TYPE
from ai.humanai.task.taskassignedtimedtask import TaskAssignedTimedTask
import guiwindow
from entities.groupbase import GROUP_BUFFER_FACTOR


"""
Needs to be called at least once a day.
Allocates people such that they collect and deposit cell at the stockpile.
Allocates hourly using buffer factors.

A wrapper for performing an action, including a cost function, prerequisite conditions and worker logic.
"""
class ActionGroupHourlySkilledCraftItems(ActionGroupHourlySkilled):

    """
    DO NOT DELETE THIS. PASTE THIS IN FOR EVERY NEW OBJECT THAT WILL BE STORED IN A SET/DICTIONARY.
    THIS IS ESSENTIAL FOR MAKING SURE THE PROGRAM PERFORMS EXACTLY THE SAME EVERY TIME!

    assert(false) WILL CRASH THE PROGRAM IF YOU ATTEMPT TO PUT THIS OBJECT INTO A SET/DICT WITHOUT FIRST MODIFYING THE FUNCTION.
    THIS IS DONE ON PURPOSE TO PREVENT YOU FROM ACCIDENTALLY LEAKING NON-DETERMINISM INTO THE PROGRAM.
    SPEAK TO ME (TOM) AND I WILL EXPLAIN WHAT TO DO.
    """
    # def __hash__(self):
    #     return hash(self.hash_id)
    #
    # def __eq__(self, other):
    #     return self.__class__ == other.__class__ and self.hash_id == other.hash_id


    def __init__(self, parent_task):
        super().__init__(parent_task, GROUP_BUFFER_FACTOR.CRAFTING, 0) # ALWAYS CALL PARENT CONSTRUCTOR
        self.hash_id = guiwindow.WORLD_INSTANCE.skilled_get_craft_id_counter
        guiwindow.WORLD_INSTANCE.skilled_get_craft_id_counter += 1
        self.selected_person = None


    """
    Reserves people from the task allocation algorithm.
    """
    def excluded_people_from_task_allocation_algo(self, group):
        sorted_human_ratios = OrderedDict(
            sorted(group.daily_schedule.items(), key=lambda x: x[1][str(self.buffer_factor_skill_stat.skill.associated_human_skill) + "_ratio"],
                   reverse=True))
        for human in sorted_human_ratios:
            # check if human still has free hours
            if sorted_human_ratios[human]['free_hours'] != 0:
                sorted_human_ratios[human]['free_hours'] = 0
                self.selected_person = human
                break

        return [self.selected_person]

    """
    Returns true/false if we should include this action in the typical task allocation.
    If false, will be removed from the task calculations.

    Called when task actions are recalculated.
    """
    def requires_hourly_task_allocation_algo(self):
        return False

    """
    This is called once when the action begins.
    """
    def activate(self, hours_left, available_people, group):
        """
        Note this calculation is correct because the hours are adjusted for the buffer factor
        from get_estimated_hours()
        """
        self.current_workers = set()
        self.hours_taken = 0
        self.ticks_taken = 0
        self.hours_allocated = group.amount_hours_left_work_day()
        self.selected_person.force_finish_task()
        self.selected_person.needs[NEED_TYPE.GROUP_TASK].add_scheduled_task(self.selected_person, TaskAssignedTimedTask(self.get_allocated_task(),
                                                                               self.hours_allocated * global_params.hourly_ticks))




    """
    Returns the data used to train this skills buffer factor.
    Triggered at activation of action.
    Should be returned as a tuple like so:
    (amount_achieved, amount_required)
    """
    def get_achieved_vs_required_bf_data(self, group):
        """
        Adjust original amount for actual time taken (sometimes a task can finish early)
        """
        estimated_amount_required = self.hours_taken * self.buffer_factor_skill_stat.skill.get_estimated_hourly_rate() /\
                                                        group.buffer_factors[self.buffer_factor_skill_stat.skill].value

        return self.buffer_factor_skill_stat.amount_achieved, estimated_amount_required





    """
    Called when the person has made progress in the task.
    Opportunity for you to update buffer factors as well as general progress of the action.
    """
    def register_progress(self, human, amount, group):
        group.need_crafting.current_item.increase_craft_progress(amount)
        self.buffer_factor_skill_stat.achieved(amount)
        self.total_amount_left -= amount
        if group.need_crafting.current_item.is_crafting_complete():
            group.need_crafting.complete_crafting(group)



    """
    The task to be allocated to each person.
    """
    def get_allocated_task(self):
        return TaskCraftItems(self.hours_allocated * global_params.hourly_ticks, self)


    """
    Returns true/false to indicate whether the action is complete or not.
    Called every tick before tick() is executed.    
    """
    def is_complete(self, group):
        return not group.need_crafting.is_items_left()


    """
    Optional, gives tickly debug information.
    """
    def get_stats(self, group):
        if self.hours_allocated == 0 or group.need_crafting.current_item is None:
            return str(self.buffer_factor_skill_stat)

        return "stat %s \nhours %s/%s | %s%%\ncurrent workers %s\ntask current: %s (%s%%) | queue: %s" % \
                                      (str(self.buffer_factor_skill_stat),
                                      round(self.hours_taken, 2),
                                      round(self.hours_allocated, 2),
                                      int((self.hours_taken / self.hours_allocated) * 100),
                                      len(self.current_workers),
                                      group.need_crafting.current_item,
                                       int((group.need_crafting.current_item.craft_progress_tick / group.need_crafting.current_item.get_craft_amount()) * 100),
                                       len(group.need_crafting.craft_list))


    def __str__(self):
        return "Blacksmith job"


# task current: %s (%s/%s%%) | queue: %s"