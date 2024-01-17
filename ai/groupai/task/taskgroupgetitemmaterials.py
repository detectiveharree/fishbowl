from ai.groupai.task.taskgroupdaily import TaskGroupDaily
from ai.groupai.actions.actiongrouphourlyskilledgetresource import ActionGroupHourlySkilledGetResource
import guiwindow
from ai.need import NEED_TYPE

class TaskGroupCraftGetItemMaterials(TaskGroupDaily):

    """
    DO NOT DELETE THIS. PASTE THIS IN FOR EVERY NEW OBJECT THAT WILL BE STORED IN A SET/DICTIONARY.
    THIS IS ESSENTIAL FOR MAKING SURE THE PROGRAM PERFORMS EXACTLY THE SAME EVERY TIME!

    assert(false) WILL CRASH THE PROGRAM IF YOU ATTEMPT TO PUT THIS OBJECT INTO A SET/DICT WITHOUT FIRST MODIFYING THE FUNCTION.
    THIS IS DONE ON PURPOSE TO PREVENT YOU FROM ACCIDENTALLY LEAKING NON-DETERMINISM INTO THE PROGRAM.
    SPEAK TO ME (TOM) AND I WILL EXPLAIN WHAT TO DO.
    """
    def __hash__(self):
        return hash(self.hash_id)

    def __eq__(self, other):
        return self.__class__ == other.__class__ and self.hash_id == other.hash_id


    def __init__(self, item, need_level, need_type):
        super(). __init__(need_level, need_type)
        self.hash_id = guiwindow.WORLD_INSTANCE.task_craft_item_id_counter
        guiwindow.WORLD_INSTANCE.task_craft_item_id_counter += 1
        self.item = item


    def terminate_task_early(self, group):
        """
        If we have to cancel the task early for any reason,
        inform the person that it cannot be achieved which will let him
        reinnovate again.
        """
        if self.item.crafted_for_id in group.member_ids:
            human = guiwindow.WORLD_INSTANCE.humanDict[self.item.crafted_for_id]
            human.needs[NEED_TYPE.TRAIN].reset_kit_change_request(human)

    """
    Must return true/false.
    Will deplete a need given the level and need passed to this task on creation if true.
    Certain need types don't need this.
    """
    def should_deplete_need_on_task_completion(self):
        return True

    """
    Must return True/False
    If true, resets the progress of all actions and the action queue
    every time this task is activated i.e. activate() function is called 
    Action queue will be assigned to possible_actions().
    """
    def reset_action_tree_on_activation(self):
        return False

    """
    Called when the task is finished.
    This can occur naturally (i.e. action tree finishing) or if a task is force quited. 
    """
    def finish_task(self, group):
        group.need_crafting.register_item_to_be_crafted(self.item, self.need_level)

    """
    Possible actions that the user can do to satisfy this pre requisite.
    Note the action with the cheapest action tree will be picked.
    """
    def possible_actions(self):

        def create_resource_action(resource, amount):
            self.contents[resource].max_amount = amount
            return ActionGroupHourlySkilledGetResource(resource, amount, self)

        return [[create_resource_action(resource, amount) for (resource, amount) in self.item.get_craft_resources().items()]]


    def __repr__(self):
        return str("Get resources to craft item %s" % self.item)