from ai.humanai.relationships.interaction.interactionfighting.attack.attack import Attack, ATTACK_TYPES, FIGHT_STATE
import numpy as np

class AttackUnarmed(Attack):

    def make_attack(self, attacker, defender, mean_damage, fight_state):
        return (fight_state, 5 * attacker.body.strength)

