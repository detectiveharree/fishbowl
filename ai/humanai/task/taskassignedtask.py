import ai
from ai.need import NEED_TYPE

"""
Task for performing another task's action till it is complete
"""
class TaskAssignedTask(ai.task.Task):

    """
    DO NOT DELETE THIS. PASTE THIS IN FOR EVERY NEW OBJECT THAT WILL BE STORED IN A SET/DICTIONARY.
    THIS IS ESSENTIAL FOR MAKING SURE THE PROGRAM PERFORMS EXACTLY THE SAME EVERY TIME!

    assert(false) WILL CRASH THE PROGRAM IF YOU ATTEMPT TO PUT THIS OBJECT INTO A SET/DICT WITHOUT FIRST MODIFYING THE FUNCTION.
    THIS IS DONE ON PURPOSE TO PREVENT YOU FROM ACCIDENTALLY LEAKING NON-DETERMINISM INTO THE PROGRAM.
    SPEAK TO ME (TOM) AND I WILL EXPLAIN WHAT TO DO.
    """
    def __hash__(self):
        assert(False)

    def __init__(self, task):
        self.task = task


    def terminate_task_early(self, human):
        """
        Should be Okay for daily tasks because a action will not be terminated till 8am
        therefore the buffer factor window will be closed either way.
        """
        if self.task.terminate_task_early(human):
            human.needs[NEED_TYPE.GROUP_TASK].finish_daily_task()
            return True
        return False

    """
    Called when the task is begun for the first time.
    Must Return a action tree.
    Default: returns best action tree
    """
    def begin(self, human):
        return self.task.begin(human)

    """
    Called every tick when this is the humans current task
    """
    def tick(self, human):
        self.task.tick(human)


    """
    Called when the a action in a task has failed.
    Must Return a action tree.
    Default: returns best action tree
    """
    def action_failed_response(self, human):
        return self.task.action_failed_response(human)


    """
    Called when the action tree is completed.
    Returns True/False. If true, task will terminate, else the task will be restarted via begin()
    Default: returns true
    """
    def is_task_complete(self, human):

        if self.task.is_task_complete(human):
            human.needs[NEED_TYPE.GROUP_TASK].finish_daily_task()
            return True
        return False



    def __repr__(self):
        return str("Timed assigned task %s" % (str(self.task)))
