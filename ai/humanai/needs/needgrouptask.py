from ai.need import Need, NEED_TYPE
from ai.humanai.task.taskassignedscheduletasks import TaskAssignedScheduleTasks
from ai.humanai.task.taskassignedtask import TaskAssignedTask
from humanbase import HumanState
import global_params

"""
Main point of this task is to make sure the human actually does their group task.
This can be achieved by artificially setting their need level very high when they
start/finish their group task.
"""
class NeedTaskGroup(Need):

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
        super().__init__(NEED_TYPE.GROUP_TASK) # ALWAYS CALL PARENT CONSTRUCTOR
        self.group_task = None
        self.new_allocation = True

    def add_scheduled_task(self, human, scheduled_task, priority=global_params.default_group_task_loyalty_threshold):

        human.state = HumanState.AWAKE

        if self.new_allocation:
            self.group_task = None
            self.new_allocation = False

        if self.group_task is None or not isinstance(self.group_task, TaskAssignedScheduleTasks):
            self.group_task = TaskAssignedScheduleTasks([scheduled_task])
        else:
            self.group_task.tasks.append(scheduled_task)
        self.need_level = priority


    def set_daily_task(self, human, task, priority):
        human.force_finish_task()
        human.state = HumanState.AWAKE


        if self.new_allocation:
            self.group_task = None
            self.new_allocation = False

        self.group_task = TaskAssignedTask(task)
        self.need_level = priority

    def finish_daily_task(self):
        self.group_task = None # just in case set it to None
        self.need_level = 0

    """
    Each person will tick
    """
    def tick(self, human):
        pass


    """
    Called when this need is the highest out of all of needs 
    """
    def get_task(self, human):
        return self.group_task
