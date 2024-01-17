from ai.groupai.needs.needgroup import NeedGroup, GROUP_NEED_TYPE
from ai.groupai.task.taskgroupgetitemmaterials import TaskGroupCraftGetItemMaterials
import logging

class NeedGroupRequestItems(NeedGroup):

    """
    DO NOT DELETE THIS. PASTE THIS IN FOR EVERY NEW OBJECT THAT WILL BE STORED IN A SET/DICTIONARY.
    THIS IS ESSENTIAL FOR MAKING SURE THE PROGRAM PERFORMS EXACTLY THE SAME EVERY TIME!

    assert(false) WILL CRASH THE PROGRAM IF YOU ATTEMPT TO PUT THIS OBJECT INTO A SET/DICT WITHOUT FIRST MODIFYING THE FUNCTION.
    THIS IS DONE ON PURPOSE TO PREVENT YOU FROM ACCIDENTALLY LEAKING NON-DETERMINISM INTO THE PROGRAM.
    SPEAK TO ME (TOM) AND I WILL EXPLAIN WHAT TO DO.
    """
    def __hash__(self):
        assert(False)


    def __init__(self):
        super().__init__(GROUP_NEED_TYPE.RESOURCE_REQUESTING) # ALWAYS CALL PARENT CONSTRUCTOR
        self.items_request_crafting = []

    def request_item_crafted(self, item, demand):
        logging.info("%s has requested %s to be crafted" % (item.crafted_for_id, item))
        self.items_request_crafting.append(TaskGroupCraftGetItemMaterials(item, demand, GROUP_NEED_TYPE.RESOURCE_REQUESTING))
        self.need_level += demand

    """
    Called once a day.
    """
    def get_task(self, group, adjusted_need_level):
        """
        DECREMENT NEED LEVELS AFTER TASK COMPLETE!
        """

        if adjusted_need_level > 0:
            new_tasks = list(self.items_request_crafting)
            self.items_request_crafting.clear()
            return new_tasks
        return []

