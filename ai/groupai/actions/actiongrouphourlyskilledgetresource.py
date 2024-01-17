from ai.groupai.actions.actiongroup import ActionGroup
from ai.groupai.actions.actiongrouphourlyskilled import ActionGroupHourlySkilled
from ai.humanai.task.taskbringresourcetogroup import TaskBringResourceToGroup
import global_params
from collections import OrderedDict
import guiwindow



"""
Needs to be called at least once a day.
Allocates people such that they collect and deposit cell at the stockpile.
Allocates hourly using buffer factors.

A wrapper for performing an action, including a cost function, prerequisite conditions and worker logic.
"""
class ActionGroupHourlySkilledGetResource(ActionGroupHourlySkilled):

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


    def __init__(self, resource, total_amount_required, parent_task):
        # ROUND AMOUNT TO
        super().__init__(parent_task, resource.group_buffer_factor_association, total_amount_required) # ALWAYS CALL PARENT CONSTRUCTOR
        self.hash_id = guiwindow.WORLD_INSTANCE.skilled_get_resource_id_counter
        guiwindow.WORLD_INSTANCE.skilled_get_resource_id_counter += 1
        self.resource = resource
        self.task_resource_storage = parent_task.contents[self.resource]


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
        self.task_resource_storage.deposit(amount)
        self.buffer_factor_skill_stat.achieved(amount)
        self.total_amount_left -= amount


    """
    The task to be allocated to each person.
    """
    def get_allocated_task(self):
        return TaskBringResourceToGroup(self.resource, global_params.inventory_size, self)


    def __str__(self):
        return "Get resource %s" % self.resource
