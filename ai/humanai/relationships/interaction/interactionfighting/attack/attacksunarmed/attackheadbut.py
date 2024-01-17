from ai.humanai.relationships.interaction.interactionfighting.attack.attack import Attack, ATTACK_TYPES, FIGHT_STATE
import numpy as np
from ai.humanai.relationships.interaction.interactionfighting.attack.attackunarmed import AttackUnarmed

class AttackHeadBut(AttackUnarmed):

    """
    Get the type of attack this class does
    """
    @staticmethod
    def get_attack_type():
        return ATTACK_TYPES.HEADBUTT

    def acceptable_states(self):
        return [FIGHT_STATE.CLINCH]

    def prerequisites(self, attacker, unarmed):
        return True

    def get_damage(self, attacker, defender, fight_state):
        return 5 * abs(attacker.personality.agreeable.value + 1)
