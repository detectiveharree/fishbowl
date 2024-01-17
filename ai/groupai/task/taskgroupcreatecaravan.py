from ai.groupai.task.taskgroup import TaskGroup
from ai.groupai.actions.actiongroupcreatecaravan import ActionGroupCreateCaravan
import global_params
from items.itemresources.itemresource import ResourceType
from ai.groupai.needs.needgroup import GROUP_NEED_TYPE

"""
Task for initiating the creation of a caravan with a meeting point,
also gives the group a task to do when they are successfully created
"""
class TaskGroupCreateCaravan(TaskGroup):

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


    def __init__(self, original_group, caravan_group, caravan_people, callback = lambda : None):
        super(). __init__(0, GROUP_NEED_TYPE.NONE)
        caravan_group.parent_group = original_group
        self.original_group = original_group
        self.caravan_group = caravan_group
        self.caravan_people = caravan_people
        self.caravan_formed_callback = callback


    """
    Must return True/False
    If true, resets the progress of all actions and the action queue
    every time this task is activated i.e. activate() function is called 
    Action queue will be assigned to possible_actions().
    """
    def reset_action_tree_on_activation(self):
        return False

    """
    Possible actions that the user can do to satisfy this pre requisite.
    Note the action with the cheapest action tree will be picked.
    """
    def possible_actions(self):
        return [[ActionGroupCreateCaravan(self, self.caravan_group, self.caravan_people)]]

    """
    Called when the task is finished.
    This can occur naturally (i.e. action tree finishing) or if a task is force quited.
    """
    def finish_task(self, human):
        self.caravan_formed_callback()


    def __repr__(self):
        return str("Create caravan %s from %s" % (self.caravan_group.id_number, self.original_group.id_number))