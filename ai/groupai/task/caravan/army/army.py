from abc import abstractmethod, ABC
from entities.group import Group
from entities.groupbase import GroupType
from enum import Enum
from ai.groupai.task.taskgroupcreatecaravan import TaskGroupCreateCaravan
from ai.groupai.task.caravan.taskgroupcaravangohome import TaskGroupCaravanGoHome
from ai.groupai.task.caravan.taskgroupcaravanmove import TaskGroupCaravanMove

class CAMPAIGN_TYPE(Enum):

    TERRITORY_ANNEX = 1

    def __repr__(self):
        return self.name

class Army(ABC):

    def __init__(self, original_group):
        self.original_group = original_group
        self.chosen_army = self.choose_army()
        self.original_soldier_amount = len(self.chosen_army)
        self.caravan_group = Group(self.get_army_rally_point(original_group), GroupType.RALLY_POINT, original_group)
        self.interaction_group_battle = None # if a battle results from this army, reference it here

    """
    Start point
    """
    @abstractmethod
    def begin(self):
        ...

    """
    Should be called on end.
    """
    @abstractmethod
    def end(self):
        ...

    """
    Must return set of people we will use for the army.
    """
    @abstractmethod
    def choose_army(self):
        ...

    """
    The location where the army is initally formed
    """
    @abstractmethod
    def get_army_rally_point(self, original_group):
        ...

    """
    Called when the inital army has formed via form_army
    """
    @abstractmethod
    def army_formed(self):
        ...

    """
    Called when battle is over
    """
    @abstractmethod
    def battle_over(self, outcome):
        ...

    """
    Return true if the participant wants to surrender
    Called every tick during a battle
    """
    @abstractmethod
    def should_surrender(self, interaction_participant):
        ...

    """
    Forms the army group, assigning it to caravan_group
    """
    def form_army(self):
        task = TaskGroupCreateCaravan(self.original_group, self.caravan_group, self.chosen_army, self.army_formed)
        self.original_group.add_task(task)


    """
    Helper function that sends the army home
    """
    def send_army_home(self):
        self.caravan_group.add_task(TaskGroupCaravanGoHome(self.caravan_group))

    """
    Helper function that sends the army back to their army camp
    """
    def march_to_army_camp(self, callback):
        self.caravan_group.add_task(TaskGroupCaravanMove(self.caravan_group, self.enemy_camp_rally_point,
                                                         starting_location = self.caravan_group.stockpile_location,
                                                         move_stockpile=False,
                                                         callback = callback))


    """
    Helper function that sends the army back to their army camp
    """
    def march_and_move_army_camp(self, destination, callback):
        self.caravan_group.add_task(TaskGroupCaravanMove(self.caravan_group, destination,
                                                         starting_location = self.caravan_group.stockpile_location,
                                                         move_stockpile=True,
                                                         callback = callback))


