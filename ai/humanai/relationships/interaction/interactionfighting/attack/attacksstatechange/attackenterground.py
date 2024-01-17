from ai.humanai.relationships.interaction.interactionfighting.attack.attack import Attack, ATTACK_TYPES, FIGHT_STATE
import numpy as np
from ai.humanai.relationships.interaction.interactionfighting.attack.attackstatechange import AttackStateChange

class AttackEnterGround(AttackStateChange):

    """
    Get the type of attack this class does
    """
    @staticmethod
    def get_attack_type():
        return ATTACK_TYPES.ENTER_GROUND

    def acceptable_states(self):
        return [FIGHT_STATE.CLINCH]

    def prerequisites(self, attacker, unarmed):
        return attacker.body.leftarm.is_intact or attacker.body.rightarm.is_intact

    def get_damage(self, attacker, defender, fight_state):
        return 5

    """
    Get the type of state that will be changed to
    """
    @staticmethod
    def get_new_state():
        return FIGHT_STATE.GROUND