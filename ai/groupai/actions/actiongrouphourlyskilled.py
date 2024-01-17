from ai.groupai.actions.actiongroup import ActionGroup
from ai.humanai.task.taskbringresourcetogroup import TaskBringResourceToGroup
import global_params
from collections import OrderedDict
from abc import ABC, abstractmethod
from ai.groupai.bufferfactor.bufferfactorskill import BufferFactorSkillStats
from ai.need import NEED_TYPE
from ai.humanai.task.taskassignedtimedtask import TaskAssignedTimedTask


"""
Needs to be called at least once a day.
Allocates people such that they collect and deposit cell at the stockpile.
Allocates hourly using buffer factors.

A wrapper for performing an action, including a cost function, prerequisite conditions and worker logic.
"""

class ActionGroupHourlySkilled(ActionGroup):

    # """
    # DO NOT DELETE THIS. PASTE THIS IN FOR EVERY NEW OBJECT THAT WILL BE STORED IN A SET/DICTIONARY.
    # THIS IS ESSENTIAL FOR MAKING SURE THE PROGRAM PERFORMS EXACTLY THE SAME EVERY TIME!
    #
    # assert(false) WILL CRASH THE PROGRAM IF YOU ATTEMPT TO PUT THIS OBJECT INTO A SET/DICT WITHOUT FIRST MODIFYING THE FUNCTION.
    # THIS IS DONE ON PURPOSE TO PREVENT YOU FROM ACCIDENTALLY LEAKING NON-DETERMINISM INTO THE PROGRAM.
    # SPEAK TO ME (TOM) AND I WILL EXPLAIN WHAT TO DO.
    # """
    # def __hash__(self):
    #     assert(False)


    def __init__(self, parent_task, skill, total_amount_required):
        super().__init__(parent_task) # ALWAYS CALL PARENT CONSTRUCTOR
        self.buffer_factor_skill_stat = BufferFactorSkillStats(skill)
        self.total_amount_left = total_amount_required
        self.original_amount = total_amount_required
        self.hours_allocated = 0
        self.current_workers = set()
        self.hours_taken = 0
        self.ticks_taken = 0

    def begin_work_on_task(self, human):
        self.current_workers.add(human)

    def end_work_on_task(self, human):
        if human in self.current_workers:
            self.current_workers.remove(human)


    """
    Called every tick while the action has begun and not completed yet.
    Returns True/False to indicate if an error occurs.
    """
    def tick(self, human):
        # record amount of hours people have been working for
        self.ticks_taken += (1 * len(self.current_workers))
        self.hours_taken = self.ticks_taken / global_params.hourly_ticks
        return True



    """
    Called when the person has made progress in the task.
    Opportunity for you to update buffer factors as well as general progress of the action.
    """
    @abstractmethod
    def register_progress(self, human, amount, group):
        ...


    """
    Returns true/false if we should include this action in the typical task allocation.
    If false, will be removed from the task calculations.

    Called when task actions are recalculated.
    """
    def requires_hourly_task_allocation_algo(self):
        return True

    """
    IF requires_hourly_task_allocation_algo is true,
    will take into account the estimated hours below.
    """
    def estimated_hours(self, group):
        """
        YES - we should be using the default harvest tick rate in this calculation.
        It acts as a constant for normalising the buffer factors.
        Having a variable "more accurate" number will actually be WORST for normalising buffer factors,
        because its variable.

        i.e. default tick rate adjusted for average group skills, will cause the buffer factors
            to get trained on that average - which may change over time, causing more
            volatility for the buffer factor system. Using a constant is NECESSARY here.
            The buffer factors will reflect the skills over time.
        """
        return self.buffer_factor_skill_stat.skill.get_estimated_hours(self.total_amount_left) *\
               group.buffer_factors[self.buffer_factor_skill_stat.skill].value


    """
    Optional, gives tickly debug information.
    """
    def get_stats(self, group):
        if self.hours_allocated == 0:
            return str(self.buffer_factor_skill_stat)

        return "stat %s \nhours %s/%s | %s%%\ncurrent workers %s\namunt left: %s/%s" % \
                                      (str(self.buffer_factor_skill_stat),
                                      round(self.hours_taken, 2),
                                      round(self.hours_allocated, 2),
                                      int((self.hours_taken / self.hours_allocated) * 100),
                                      len(self.current_workers),
                                      self.total_amount_left,
                                       self.original_amount)


    """
    The task to be allocated to each person.
    """
    @abstractmethod
    def get_allocated_task(self):
        ...


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
        self.hours_allocated = hours_left
        self.allocate_via_hours(hours_left, available_people, group)

    """
    Get buffer factor data
    """
    @abstractmethod
    def get_allocated_task(self):
        ...

    """
    Returns the data used to train this skills buffer factor.
    Triggered at activation of action.
    Should be returned as a tuple like so:
    (amount_achieved, amount_required)
    """
    @abstractmethod
    def get_achieved_vs_required_bf_data(self, group):
        ...

    """
    This is called when the action is deactivated.
    """
    def deactivate(self, group):

        (amount_achieved, amount_required) = self.get_achieved_vs_required_bf_data(group)

        group.modify_buffer_factor(self.buffer_factor_skill_stat.skill, amount_achieved, amount_required)
        self.buffer_factor_skill_stat.reset()


    """
    Allocate tasks to the humans via hours
    """
    def allocate_via_hours(self, hours_left, available_people, group):
        sorted_human_ratios = OrderedDict(
            sorted(available_people.items(), key=lambda x: x[1][str(self.buffer_factor_skill_stat.skill.associated_human_skill) + "_ratio"],
                   reverse=True))

        amount_people = set()

        while True:
            if hours_left == 0:
                break
            anyone_available = False
            for human in sorted_human_ratios:
                # check if human still has free hours
                if sorted_human_ratios[human]['free_hours'] == 0:
                    continue
                else:
                    # find the minimum between human's free hours and hours remaining for task
                    # add and subtract accordingly
                    amount_hours = min(hours_left,sorted_human_ratios[human]['free_hours'])
                    if amount_hours == 0:
                        continue
                    sorted_human_ratios[human]['free_hours'] -= amount_hours
                    human.force_finish_task()
                    hours_left -= amount_hours
                    amount_people.add(human)
                    human.needs[NEED_TYPE.GROUP_TASK].add_scheduled_task(human, TaskAssignedTimedTask(self.get_allocated_task(),
                                                                                           global_params.hourly_ticks *
                                                                                           amount_hours))
                    anyone_available = True
            if not anyone_available:
                break

    """
    The estimated cost of this action.
    This occurs during the decision making process of a action tree.
    For extra accuracy, use data from prerequisites.
    """

    def get_costs(self, group):
        return 0



    """
    Returns true/false to indicate whether the action is complete or not.
    Called every tick before tick() is executed.    
    """
    def is_complete(self, group):
        return self.total_amount_left <= 0
