
from ai.groupai.task.caravan.army.armycampaign import ArmyCampaign, CAMPAIGN_TYPE
from ai import pathfinding
import guiwindow
from ai.groupai.task.caravan.taskgroupcaravanmove import TaskGroupCaravanMove
from ai.groupai.task.caravan.taskgroupcaravancampaignoccupy import TaskGroupCaravanCampaignOccupy
from ai.groupai.interaction.interactiongroupbattle import InteractionGroupBattle
from ai.groupai.interaction.interactionparticipantgroup import BATTLE_RESULT
import logging
from ai.groupai.task.caravan.army.armytypes.armyterritoryannexdefence import ArmyTerritoryAnnexDefence

class ArmyTerritoryAnnexCampaign(ArmyCampaign):

    def __init__(self, original_group, territory_location):
        self.territory_location = territory_location
        self.enemy_territory_id = guiwindow.WORLD_INSTANCE.world[self.territory_location[0]][self.territory_location[1]].territory
        self.army_rally_point = None
        self.enemy_camp_rally_point = None
        self.calculate_locations(original_group)

        super().__init__(original_group)


    """
    Get the appropriate type of defence army that might be used to defend against this assault
    """
    def get_defence_type(self):
        return ArmyTerritoryAnnexDefence

    """
    Calculate estimated days the army will take.
    (used to calculate food and water requirements)
    """
    def get_estimated_days(self):
        return 1

    """
    The location where the army is initally formed
    """
    def get_army_rally_point(self, original_group):
        """
        Should return closest location within border of our territory
        """
        return self.army_rally_point

    """
    Get the type of army this is
    """
    def get_campaign_type(self):
        return CAMPAIGN_TYPE.TERRITORY_ANNEX

    """
    Returns the group that will be offended by this army
    """
    def get_enemy_group_id(self):
        return self.enemy_territory_id

    """
    Must return set of people we will use for the army.
    """
    def choose_army(self):
        return set(list(self.original_group.members)[:len(self.original_group.members)//2])


    """
    Return true if the participant wants to surrender
    Called every tick during a battle
    """
    def should_surrender(self, interaction_participant):
        # if all dead
        if len(self.caravan_group.members) == 0:
            return True
        # if all left battle
        if len(interaction_participant.active_soldiers) == 0:
            return True
        # 3 people have died
        if self.original_soldier_amount - len(self.caravan_group.members) > 3:
            return True
        return False


    """
    /// ==========================================================================================
    /// CAMPAIGN LOGIC
    /// ==========================================================================================
    """


    """
    Called when the inital army has formed
    """
    def army_formed(self):
        logging.info("%s has formed their army of %s" % (self.original_group.id_number, len(self.chosen_army)))
        """
        Border of our territory
        """
        self.march_and_move_army_camp(self.enemy_camp_rally_point, self.arrived_at_territory)


    def arrived_at_territory(self):
        logging.info("%s's army has arrived at the border of %s and is moving in to occupy" % (self.original_group.id_number, self.enemy_territory_id))

        """
        Border of their territory
        """
        self.caravan_group.add_task(TaskGroupCaravanCampaignOccupy(self.caravan_group, self.territory_location, self, callback = self.occupation_response))



    def occupation_response(self):

        # they noticed territory was being taken
        if self.interaction_group_battle is not None:
            self.interaction_group_battle.start_interaction()
        # they didn't notice territory was being taken
        else:
            logging.info("%s did not respond to %s's territorial occupation" % (self.enemy_territory_id, self.original_group.id_number))
            self.end_succeded()


    def battle_over(self, result):
        if result == BATTLE_RESULT.WON:
            self.end_succeded()
        else:
            self.end_failed()


    def end_succeded(self):
        logging.info("%s has succeded in taking over the territory" % (self.original_group.id_number))
        self.original_group.take_over_territory(self.territory_location, list(guiwindow.WORLD_INSTANCE.groups.keys()))
        self.march_to_army_camp(self.end)

    def end_failed(self):
        logging.info("%s has failed in taking over the territory" % (self.original_group.id_number))
        self.end()


    def calculate_locations(self, original_group):

        """
        Find army meetup spot at border of our territory
        """
        self.army_rally_point = pathfinding.get_first_location_given(original_group.stockpile_location, self.territory_location,
                                                                     lambda worldcell : worldcell.territory != original_group.id_number)

        """
        Find army camp spot at border of enemy territory
        """
        self.enemy_camp_rally_point = pathfinding.get_first_location_given(self.army_rally_point, self.territory_location,
                                                                     lambda worldcell : worldcell.territory == self.enemy_territory_id)












