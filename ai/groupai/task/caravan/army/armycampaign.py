from abc import abstractmethod, ABC
import global_params
from ai.groupai.task.caravan.army.army import Army
from ai.groupai.task.taskgroupgetcampaignresources import TaskGroupGetCampaignResources
from ai.groupai.task.taskgroupcreatecaravan import TaskGroupCreateCaravan
from ai import pathfinding
from ai.groupai.task.caravan.taskgroupcaravangohome import TaskGroupCaravanGoHome
from enum import Enum
import logging

class CAMPAIGN_TYPE(Enum):

    TERRITORY_ANNEX = 1
    ANNIHILATE = 2

    def __repr__(self):
        return self.name

class ArmyCampaign(Army, ABC):

    def __init__(self, original_group):
        super().__init__(original_group)
        self.food_requirement, self.water_requirement = self.calculate_food_water_requirements()


    """
    Calculate estimated days the army will take.
    (used to calculate food and water requirements)
    """
    @abstractmethod
    def get_estimated_days(self):
        ...


    """
    Get the appropriate type of defence army that might be used to defend against this assault
    """
    @abstractmethod
    def get_defence_type(self):
        ...

    """
    Returns the group that will be offended by this army
    """
    @abstractmethod
    def get_enemy_group_id(self):
        ...


    """
    Get the type of army this is
    """
    @abstractmethod
    def get_campaign_type(self):
        ...

    """
    The army will only last for how much food and water is required for the army.
    """
    def calculate_food_water_requirements(self):

        estimated_days = self.get_estimated_days()

        food_requirement = global_params.hunger_tick * \
                          global_params.daily_ticks * \
                          len(self.chosen_army) * \
                          estimated_days

        water_requirement = global_params.thirst_tick * \
                           global_params.daily_ticks * \
                           len(self.chosen_army) * \
                           estimated_days


        return (food_requirement, water_requirement)



    def begin_campaign_prep(self, group):
        logging.info("%s is preparing for a army of %s!" % (self.original_group.id_number, self.get_campaign_type()))

        group.add_task(TaskGroupGetCampaignResources(self))


    """
    Start point
    """
    def begin(self):
        logging.info("%s has begun their army of %s!" % (self.original_group.id_number, self.get_campaign_type()))
        self.caravan_group.campaign = self
        self.form_army()

    """
    Should be called on end.
    """
    def end(self):
        logging.info("%s has finished their army of %s and are going home." % (self.original_group.id_number, self.get_campaign_type()))
        self.send_army_home()
        self.caravan_group.campaign = None







