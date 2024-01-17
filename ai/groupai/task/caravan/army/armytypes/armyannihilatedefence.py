from ai.groupai.task.caravan.army.armydefence import ArmyDefence
from ai.groupai.interaction.interactiongroupbattle import InteractionGroupBattle
from ai.groupai.interaction.interactionparticipantgroup import BATTLE_RESULT
import logging

class ArmyAnnihilateDefence(ArmyDefence):


    def __init__(self, original_group, enemy_territory_campaign):
        self.enemy_territory_campaign = enemy_territory_campaign
        super().__init__(original_group)


    """
    Called when battle is over
    """
    @staticmethod
    def get_campaign_threat_score(group, enemy_territory_campaign):
        return 1000

    """
    Decide response
    """
    @staticmethod
    def get_campaign_response(group, enemy_territory_campaign):

        fight = True

        if fight:
            defensive_strategy = ArmyAnnihilateDefence(group, enemy_territory_campaign)

            defensive_strategy.begin()


    """
    Must return set of people we will use for the army.
    """
    def choose_army(self):
        return set(list(self.original_group.members)[:len(self.original_group.members)//7])

    """
    The location where the army is initally formed
    """
    def get_army_rally_point(self, original_group):
        return original_group.stockpile_location

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
    /// DEFENCE LOGIC
    /// ==========================================================================================
    """

    """
    Start point
    """
    def begin(self):
        logging.info("%s has started a defence army against %s's %s!" % (self.original_group.id_number,
                                                                         self.enemy_territory_campaign.original_group.id_number,
                                                                         self.enemy_territory_campaign.get_campaign_type()))

        self.interaction_group_battle = InteractionGroupBattle(self, self.enemy_territory_campaign,
                                                               self.battle_over, self.enemy_territory_campaign.battle_over)
        # by setting this, this also signals the campaign army of the defence decision
        self.enemy_territory_campaign.interaction_group_battle = self.interaction_group_battle
        self.form_army()

    """
    Called when the inital army has formed
    """
    def army_formed(self):
        logging.info("%s has formed their army of %s" % (self.original_group.id_number, len(self.chosen_army)))



    def battle_over(self, result):
        if result == BATTLE_RESULT.WON:
            logging.info("%s won the battle against %s avoiding annihilation!" % (self.original_group.id_number, self.enemy_territory_campaign.original_group.id_number))
        else:
            logging.info("%s lost was annihilated by %s after losing in battle" % (self.original_group.id_number, self.enemy_territory_campaign.original_group.id_number))

        self.end()


    """
    Should be called on end.
    """
    def end(self):
        logging.info("%s defence army is going home." % self.original_group.id_number)
        self.send_army_home()





