from abc import ABC, abstractmethod
import numpy as np

"""
ABC is a abstract base class.
Means we can never instantiate a Prerequisite object.
Instead we have to extend it, and complete the functions to do it. 
"""
class Task(ABC):

    assigned_by_group = False


    """
    Called every tick when this is the humans current task
    """
    def tick(self, human):
        pass

    """
    Possible actions that the user can do to satisfy this pre requisite.
    Note the action with the cheapest action tree will be picked.
    """
    def possible_actions(self):
        return []

    """
    Actions that CANNOT be performed while completing this task.
    NOTE the actions are specified via its type.
    """
    def forbidden_actions(self):
        return []


    """
    Called when the task is begun for the first time.
    Must Return a action tree.
    Default: returns best action tree
    """
    def begin(self, human):
        return self._get_best_action_tree(human, self.possible_actions())


    """
    Called when the a action in a task has failed.
    Must Return a action tree.
    Default: returns best action tree
    """
    def action_failed_response(self, human):
        return self._get_best_action_tree(human, self.possible_actions())


    """
    Called when the proposed action tree returns empty,
    suggesting it was not satisfied.
    Default: removes the persons task
    """
    def action_tree_not_satisfied(self, human):
        print("No action tree for task %s, removing task" % (self))
        human.change_current_task(None)

    """
    Called when the action tree is completed.
    Returns True/False. If true, task will terminate, else the task will be restarted via begin()
    Default: returns true
    """
    def is_task_complete(self, human):
        return True


    def terminate_task_early(self, human):
        return False

    """
    Called when the task is finished.
    This can occur naturally (i.e. action tree finishing) or if a task is force quited. 
    """
    def finish_task(self, human):
        pass

    """
    Overloads less then operator which is a requirement for putting a custom object in a dictionary.
    By default compare by uniqueness of memory value.
    """
    def __lt__(self, other):
        return str(self) < str(other)



    """
    Helper function for decision making.
    Sets the current action tree to the best possible given the task.
    """
    def _get_best_action_tree(self, human, action_list):
        possible_action_trees = []
        for possible_action in action_list:
            action_tree = []
            cost = self._calculate_best_action_tree(human, action_tree, possible_action)
            if cost == -1:
                continue
            possible_action_trees.append((cost, action_tree))
        if not possible_action_trees:
            return []
        best_possible_action_index = np.argmin(([cost for cost, tree in possible_action_trees]))
        return possible_action_trees[best_possible_action_index][1]



    """
    Recursively founds best action tree (i.e. the branch with the minimum cost)
    Result is returned in output list.
    """
    def _calculate_best_action_tree(self, human, output, action):

        # indicate action is forbidden there action branch not allowed
        if type(action) in self.forbidden_actions():
            return -1

        # if no unsatisfied pre requisites just return the cost of the action
        unsatisfied_prerequisites = action.get_unsatisifed_prerequisites(human)
        if not unsatisfied_prerequisites:
            output.append(action)
            return action.get_costs(human)

        cost_of_actions = 0
        potential_tree = []
        for unsatisfied in unsatisfied_prerequisites:
            # for each pre requisite get all the possible actions
            possible_actions = unsatisfied.possible_actions(human)
            # if no possible actions to satisfy pre requisite action tree not possible
            if not possible_actions:
                output.clear()
                return -1

            # recursively consider each possible action to satisfy the pre requisite and their action tree
            action_trees_from_prerequisite = []
            for pot_action in possible_actions:
                action_list = []
                cost = self._calculate_best_action_tree(human, action_list, pot_action)
                # if action tree not possible don't consider this action tree
                if cost == -1:
                    continue
                action_trees_from_prerequisite.append((cost, action_list))

            # if no possible actions to satisfy pre requisite we can't do that tree
            if not action_trees_from_prerequisite:
                return -1

            # find minimum cost action that can satisfy the prerequsite
            best_possible_action_index = np.argmin(([cost for cost, tree in action_trees_from_prerequisite]))
            best_cost = action_trees_from_prerequisite[best_possible_action_index][0]
            best_tree = action_trees_from_prerequisite[best_possible_action_index][1]
            cost_of_actions += best_cost
            potential_tree += best_tree

        # register the action tree
        output += potential_tree
        output.append(action)
        cost_of_actions += action.get_costs(human)
        return cost_of_actions
