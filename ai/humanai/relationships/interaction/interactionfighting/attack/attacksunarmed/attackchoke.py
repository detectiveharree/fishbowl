from ai.humanai.relationships.interaction.interactionfighting.attack.attack import Attack, ATTACK_TYPES, FIGHT_STATE
import numpy as np
from ai.humanai.relationships.interaction.interactionfighting.attack.attackunarmed import AttackUnarmed

class AttackChoke(AttackUnarmed):

    """
    Get the type of attack this class does
    """
    @staticmethod
    def get_attack_type():
        return ATTACK_TYPES.CHOKE

    def acceptable_states(self):
        return [FIGHT_STATE.GROUND]

    def prerequisites(self, attacker, unarmed):
        return attacker.body.leftarm.is_intact or attacker.body.rightarm.is_intact

    def get_damage(self, attacker, defender, fight_state):
        return 5
