from ai.groupai.task.taskgroup import TaskGroup
from gameworld.timestamp import TimeStamp


class TaskGroupDaily(TaskGroup):

    def __init__(self, need_level, need_type):
        super(). __init__(need_level, need_type)

        """
        Intermediate storage of actions complete in the day,
        that require deactivating.
        """
        self.prev_days_completed_actions = set()




    """
    Must return True/False
    A condition that when true, will activate this task.
    Default True
    """
    def activate_when(self, group):
        time = TimeStamp()
        return time.tick == group.start_time_in_ticks

    """
    Must return True/False
    A condition that when true, will call the tick function.
    Default True
    """
    def tick_when(self, group):
        return TimeStamp().hour >= group.start_hour_work_day and\
               TimeStamp().hour <= (group.start_hour_work_day + group.amount_hours_work_day)


    """
    Called when task finished/paused
    """
    def deactivate(self, group):
        self.is_activated = False
        self.deposit_excess_resources_to_stockpile(group)
        self.deactivate_actions(group, self.current_actions)
        self.deactivate_actions(group, list(self.prev_days_completed_actions))
        self.prev_days_completed_actions = set()

    """
    Called when task is activated    
    """
    def activate(self, group):
        self.deactivate(group)
        # print("HERE")
        # print(self.prev_days_completed_actions)
        # self.deactivate_actions(group, list(self.prev_days_completed_actions))
        # self.prev_days_completed_actions = set()
        super().activate(group)

    """
    Returns true/false if the current action is complete
    """
    def tick(self, group):

        for action in self.current_actions:
            action.tick(group)

        """
        Check if action is complete.
        Remove and deactivate if it has.
        """

        actions_complete = False


        def check_if_action_complete(action):
            nonlocal actions_complete

            if action.is_complete(group):
                # print("YES ACHIEVED!")
                self.prev_days_completed_actions.add(action)
                actions_complete = True
                action.terminated = True
                return True
            return False

        self.current_actions[:] = [action for action in self.current_actions if not check_if_action_complete(action)]

        if actions_complete:
            if self.current_actions == [] and self.action_queue != []:
                self.set_next_actions()
                return self.current_actions

        return []

    """
    Returns true/false if this entire task is complete
    """
    def is_task_complete(self, group):
        """
        Task should only be checked for completion at start of day.
        """
        return self.action_queue == [] and self.current_actions == [] and self.has_started and self.activate_when(group)
