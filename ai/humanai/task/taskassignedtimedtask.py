import ai
from ai.need import NEED_TYPE

"""
Task for performing another task's action till a time has been reached
"""
class TaskAssignedTimedTask(ai.task.Task):


    def __init__(self, task, amount_ticks):
        self.amount_ticks = amount_ticks
        self.task = task
        self.timer = 0

    """
    Called when the task is begun for the first time.
    Must Return a action tree.
    Default: returns best action tree
    """
    def begin(self, human):
        self.task.group_action.begin_work_on_task(human)
        return self.task._get_best_action_tree(human, self.task.possible_actions())


    def terminate_task_early(self, human):
        """
        Should be Okay for daily tasks because a action will not be terminated till 8am
        therefore the buffer factor window will be closed either way.
        """
        if self.task.group_action.terminated:
            self.task.group_action.end_work_on_task(human)
            return True
        return False

    """
    Called every tick when this is the humans current task
    """
    def tick(self, human):
        self.timer += 1
        pass


    """
    Called when the a action in a task has failed.
    Must Return a action tree.
    Default: returns best action tree
    """
    def action_failed_response(self, human):
        if self.timer >= self.amount_ticks:
            self.task.group_action.end_work_on_task(human)
            return []
        return self.task._get_best_action_tree(human, self.task.possible_actions())


    """
    Called when the action tree is completed.
    Returns True/False. If true, task will terminate, else the task will be restarted via begin()
    Default: returns true
    """
    def is_task_complete(self, human):

        """
        Perhaps should also take into account if assignee task is complete.
        E.g. stop building when building is complete
        """
        # theres less swings + they won't continue doing a action indefinetely if you have
        # self.task.group_action.is_complete(None)
        if self.timer >= self.amount_ticks:
            self.task.group_action.end_work_on_task(human)
            return True
        return False



    def __repr__(self):
        return str("Timed assigned task %s (%s/%s)" % (str(self.task), self.timer, self.amount_ticks))
