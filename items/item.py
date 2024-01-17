from abc import ABC, abstractmethod
import guiwindow

class Item(ABC):

    def __init__(self):
        self.id_number = guiwindow.WORLD_INSTANCE.item_id_counter
        guiwindow.WORLD_INSTANCE.item_id_counter += 1

    """
    Get weight of item
    """
    @abstractmethod
    def weight(self):
         ...

