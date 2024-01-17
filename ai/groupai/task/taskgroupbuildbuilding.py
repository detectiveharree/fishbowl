from ai.groupai.task.taskgroupdaily import TaskGroupDaily
from ai.groupai.actions.actiongrouphourlyskilledgetresource import ActionGroupHourlySkilledGetResource
from ai.groupai.actions.actiongrouphourlyskilledbuild import ActionGroupHourlySkilledBuild
import global_params
from items.itemresources.itemresource import ResourceType
from gameworld.timestamp import TimeStamp
import ai.pathfindingbuilding
import guiwindow

class TaskGroupBuildBuilding(TaskGroupDaily):

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


    def __init__(self, need_type, need_level, building, group):
        super(). __init__(need_level, need_type)
        self.hash_id = guiwindow.WORLD_INSTANCE.task_build_id_counter
        guiwindow.WORLD_INSTANCE.task_build_id_counter += 1
        self.building = building
        self.building.register_to_world()



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

        def create_resource_action(resource, amount):
            self.contents[resource].max_amount = amount
            return ActionGroupHourlySkilledGetResource(resource, amount, self)

        actions = [[create_resource_action(resource, amount) for (resource, amount) in self.building.get_required_resources().items()]]

        actions.append([ActionGroupHourlySkilledBuild(self, self.building)])
        return actions


    def __repr__(self):
        return str("Build building %s %s" % (self.building, id(self)))