from abc import ABC, abstractmethod

"""
A item that can be stored in a group's KnowledgeGroupInventoryShelf 
"""
class ItemShelfable(ABC):

    """
    Returns correct storage shelf
    """
    @staticmethod
    @abstractmethod
    def lookup_storage(lookup_matrix, group):
         ...

    """
    Returns availability storage container
    """
    @staticmethod
    @abstractmethod
    def get_availability_storage(group):
         ...

    """
    Gets lookup matrix for storage cabinet
    """
    @abstractmethod
    def get_lookup_matrix(self):
         ...



    """
    Adds item to shelf.
    """
    def add_item_to_shelf(self, group):
        self.lookup_storage(self.get_lookup_matrix(), group).append(self)
        self.get_availability_storage(group).add(self.get_lookup_matrix())

    """
    Add all item to shelf.
    """
    @classmethod
    def add_all_items_to_shelf(self, lookup_matrix, group, items):
        storage = self.lookup_storage(lookup_matrix, group)
        storage += items
        self.get_availability_storage(group).add(lookup_matrix)


    """
    Removes item from shelf.
    Will return None if item not found.
    """
    @classmethod
    def remove_item_from_shelf(self, lookup_matrix, group):
        items = self.lookup_storage(lookup_matrix, group)
        if items:
            item = items.pop(0)
            # if all plates of this material removed, take it away from plates availablity set
            if not items:
                self.get_availability_storage(group).remove(lookup_matrix)
            return item
        return None

    """
    Removes all item from shelf.
    Returns a list of the items.
    """
    @classmethod
    def remove_all_items_from_shelf(self, lookup_matrix, group):
        shelf_items = self.lookup_storage(lookup_matrix, group)
        items = list(shelf_items)
        shelf_items.clear()
        availability_storage = self.get_availability_storage(group)
        if lookup_matrix in availability_storage:
            availability_storage.remove(lookup_matrix)
        return items
