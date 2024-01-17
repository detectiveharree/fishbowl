from ai.groupai.needs.needgroup import NeedGroup, GROUP_NEED_TYPE
from ai.groupai.task.taskgroupblacksmithcraftitems import TaskGroupBlacksmithCraftItems


class NeedGroupCraftItems(NeedGroup):

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
        super().__init__(GROUP_NEED_TYPE.CRAFTING) # ALWAYS CALL PARENT CONSTRUCTOR
        # backlog of items to be crafted
        self.craft_list = []

        # current item being crafted by all blacksmiths
        self.current_item = None

        # really lazy way of keeping track of needs of each item so can subtract it at end (i don't want that info to go the full circuit)
        self.need_level_map = {}

    """
    Informs us a item should be crafted.
    WARNING the process of "crafting" doesn't actually use resources up.
    This is done in needgrouprequestitem's request_item_crafted method, use that instead.
    """
    def register_item_to_be_crafted(self, item, demand):
        self.need_level_map[item] = demand
        if self.current_item is None:
            self.current_item = item
        else:
            self.craft_list.append(item)
        self.need_level += demand

    """
    Returns true if there are items still not crafted
    """
    def is_items_left(self):
        return self.current_item is not None

    """
    Sets next item to be crafted
    """
    def set_next_craft_item(self):
        if self.craft_list:
            self.current_item = self.craft_list.pop(0)
        else:
            self.current_item = None

    """
    Called when we complete crafting the current item
    """
    def complete_crafting(self, group):

        if self.current_item in self.need_level_map:
            # subtract demand of this item
            demand = self.need_level_map[self.current_item]
            del self.need_level_map[self.current_item]
            self.need_level -= demand
            group.knowledge_group_item_inventory.move_to_collect(self.current_item, self.current_item.crafted_for_id)
            self.set_next_craft_item()


    """
    Called once a day.
    """
    def get_task(self, group, adjusted_need_level):
        if adjusted_need_level > 0:
            return [TaskGroupBlacksmithCraftItems(5000)]
        return []
