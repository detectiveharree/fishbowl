import ai
from ai.need import NEED_TYPE

"""
Basically a list of tasks that will get performed in sequence till they are complete
"""
class TaskAssignedScheduleTasks(ai.task.Task):


    def __init__(self, tasks):
        self.tasks = tasks
        self.current_task = None
        self.set_next_task()


    def set_next_task(self):
        self.current_task = self.tasks.pop(0) if self.tasks else None

    """
    Called when the task is begun for the first time.
    Must Return a action tree.
    Default: returns best action tree
    """
    def begin(self, human):
        return self.current_task.begin(human)


    """
    Called every tick when this is the humans current task
    """
    def tick(self, human):
        self.current_task.tick(human)

    def terminate_task_early(self, human):

        human_highest_need = human.current_highest_need.need_type
        if human_highest_need != NEED_TYPE.GROUP_TASK:
            human.needs[NEED_TYPE.GROUP_TASK].finish_daily_task()
            return True

        if self.current_task.terminate_task_early(human):
            self.set_next_task()

            """
            I.e. no more tasks left
            """
            if self.current_task is None and not self.tasks:
                human.needs[NEED_TYPE.GROUP_TASK].finish_daily_task()
                return True

        return False

    """
    Called when the a action in a task has failed.
    Must Return a action tree.
    Default: returns best action tree
    """
    def action_failed_response(self, human):
        return self.current_task.action_failed_response(human)


    """
    Called when the action tree is completed.
    Returns True/False. If true, task will terminate, else the task will be restarted via begin()
    Default: returns true
    """
    def is_task_complete(self, human):
        """
        I.e. no more tasks left
        """
        if self.current_task.is_task_complete(human):
            self.set_next_task()

        if self.current_task is None and not self.tasks:
            human.needs[NEED_TYPE.GROUP_TASK].finish_daily_task()
            return True

        return False


    def __repr__(self):
        return str("Assigned Schedule %s (%s)" % (self.current_task, self.tasks))
