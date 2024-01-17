from ai import task
from abc import ABC, abstractmethod
from items.itemresources.itemresource import ResourceType

"""
contents : expected amount
Should be checked at start and end of day

Start of day - deposit cell into stockpile
End of day - deposit cell back into stockpile

Buffer factors are updated 

RECORD TIME OF WHEN JOB STARTED TOO ELSE THE BUFFER FACTORS WILL BE UNDERESTIMATED!

"""

class ResourceStorage():

    def __init__(self, resource):
        self.resource = resource
        self.storage = 0

        # useful statistic in some scenarios
        self.amount_collected = 0
        self.amount_goal = 0
        self.max_amount = 0

    def reset(self):
        self.amount_collected = 0
        self.amount_goal = 0

    def deposit(self, amount):
        self.storage += amount
        self.amount_collected += amount

    def withdraw(self, amount):
        if self.storage < amount:
            amount_withdrawn = self.storage
            self.storage = 0
            return amount_withdrawn
        self.storage -= amount
        return amount

    def __repr__(self):
        if self.amount_goal == 0:
            return "%s | NA" % int(self.storage)

        return "%s | %s/%s (%s%%)" % (int(self.storage),
                                    int(self.amount_collected),
                                    int(self.amount_goal),
                                    int((self.amount_collected / self.amount_goal) * 100)
                                    )


"""
A wrapper for performing an group task
"""
class TaskGroup(task.Task, ABC):

    def __init__(self, need_level, need_type):
        self.need_level = need_level
        self.need_type = need_type
        self.contents = { resource_type:ResourceStorage(resource_type) for resource_type in list(ResourceType)}
        self.action_queue = []
        self.current_actions = []
        self.has_started = False
        self.is_activated = False


    """
    Must return true/false.
    In some cases (especially for caravan tasks) it is necessary that when the task is registered
    it becomes the sole task of the group i.e. clears all other tasks.
    This will also prevent other non only tasks but will be replaced by a only task another being registered.
    """
    def should_be_only_group_task(self):
        return False


    """
    Must return true/false.
    Will deplete a need given the level and need passed to this task on creation if true.
    Certain need types don't need this.
    """
    def should_deplete_need_on_task_completion(self):
        return False


    def reset_storage_statistics(self):
        for content in self.contents.values():
            content.reset()


    """
    Must return True/False
    A condition that when true, will activate this task.
    Default True
    """
    def activate_when(self, group):
        return not self.is_activated

    """
    Must return True/False
    A condition that when true, will call the tick function.
    Default True
    """
    def tick_when(self, group):
        return True

    """
    Deposits extra cell over max amount into group stockpile
    """
    def deposit_excess_resources_to_stockpile(self, group):
        for resource_storage in self.contents.values():
            if resource_storage.storage > resource_storage.max_amount:
                delta = resource_storage.storage - resource_storage.max_amount
                resource_storage.storage -= delta
                group.stockpile_contents[resource_storage.resource] += delta

    """
    Must return True/False
    If true, resets the progress of all actions and the action queue
    every time this task is activated i.e. activate() function is called 
    Action queue will be assigned to possible_actions().
    """
    @abstractmethod
    def reset_action_tree_on_activation(self):
        ...

    """
    Called when the task is activated for the first time.
    """
    def _activate_first_time(self):
        self.action_queue = []
        for item in self.possible_actions():
            self.action_queue.append(item)
        self.current_actions = []
        self.set_next_actions()


    """
    Called at start of pre-activation 
    i.e. activatable_when just became True
    """
    def trigger(self, group):
        pass


    """
    Called when task is activated.
    """
    def activate(self, group):
        self.is_activated = True
        self.trigger(None)
        if self.reset_action_tree_on_activation() or not self.has_started:
            self._activate_first_time()
            self.has_started = True

    def deactivate_actions(self, group, actions):
        # print("DEACVTING %s" % actions)
        for action in actions:
            action.is_activated = False
            action.deactivate(group)

    """
    Called when task finished/paused
    """
    def deactivate(self, group):
        self.is_activated = False
        self.deposit_excess_resources_to_stockpile(group)
        self.deactivate_actions(group, self.current_actions)

    """
    Returns true/false if this entire task is complete
    """
    def is_task_complete(self, group):
        return self.action_queue == [] and self.current_actions == [] and self.has_started


    """
    Called when the a action in a task has failed.
    Must Return a action tree.
    Default: returns best action tree
    """
    def action_failed_response(self, group):
        return [[]]


    """
    Returns true/false if the current action is complete
    """
    def tick(self, group):

        for action in self.current_actions:
            action.tick(group)
            # if not action.tick(group):
            #     new_actions = self.action_failed_response(group)
            #     self.action_queue = []
            #     for item in new_actions:
            #         self.action_queue.append(item)
            #     self.current_actions = []
            #     return True

        """
        Check if action is complete.
        Remove and deactivate if it has.
        """
        for action in self.current_actions:
            if action.is_complete(group):
                action.deactivate(group)
                action.terminated = True



        amount_actions = len(self.current_actions)
        self.current_actions[:] = [action for action in self.current_actions if not action.is_complete(group)]
        actions_completed = len(self.current_actions) != amount_actions
        # i.e. a action has been completed

        if actions_completed:
            if self.current_actions == [] and self.action_queue != []:
                self.set_next_actions()
                return self.current_actions
        return []


    """
    Set next action
    """
    def set_next_actions(self):
        # print("set next acts")
        self.current_actions = self.action_queue.pop(0)



    def get_current_actions(self):
        return len(self.action_queue)





