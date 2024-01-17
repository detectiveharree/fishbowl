from ai import task
import ai.humanai.actions.actionexploregroup


class TaskExploreGroup(task.Task):



    """
    Possible actions that the user can do to satisfy this pre requisite.
    Note the action with the cheapest action tree will be picked.
    """
    def possible_actions(self):
        return [ai.humanai.actions.actionexploregroup.ActionExploreGroup()]


    def action_failed_response(self, human):
        return []

    def __repr__(self):
        return str("Explore group")