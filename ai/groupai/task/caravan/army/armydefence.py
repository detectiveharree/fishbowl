from ai.groupai.task.caravan.army.army import Army
from abc import abstractmethod, ABC

class ArmyDefence(Army, ABC):


    def __init__(self, original_group):
        super().__init__(original_group)


    """
    Called when battle is over
    """
    @staticmethod
    @abstractmethod
    def get_campaign_threat_score(group, campaign):
        ...

    """
    Decide response
    """
    @staticmethod
    @abstractmethod
    def get_campaign_response(group, campaign):
        ...


    def begin_defence(self, army_members, interaction_group_battle):
        self.interaction_group_battle = interaction_group_battle
        self.form_army()

    def battle_over(self, outcome):
        self.send_army_home()

