from ai.humanai.relationships.interaction.interactionfighting.attack.attack import Attack, ATTACK_TYPES, FIGHT_STATE
from ai.humanai.relationships.interaction.interactionfighting.attack.attackunarmed import AttackUnarmed
import numpy as np
from random import randint

class AttackEyeGouge(AttackUnarmed):

    """
    Get the type of attack this class does
    """
    @staticmethod
    def get_attack_type():
        return ATTACK_TYPES.EYE_GOUGE

    def acceptable_states(self):
        return [FIGHT_STATE.GROUND]

    def prerequisites(self, attacker, unarmed):
        return attacker.body.leftarm.is_intact or attacker.body.rightarm.is_intact

    def get_damage(self, attacker, defender, fight_state):
        return 5 * abs(attacker.personality.agreeable.value + 1)

    def make_attack(self, attacker, defender, mean_damage, fight_state):

        # runs the dismemberments (if the RNG happens)
        # for limb in [defender.body.lefteye, defender.body.righteye]:
        #     if limb.is_intact:
        #         if randint(0, 100) == 0:
        #             print(attacker.id_number,'destroyed',limb.__str__(),'of',defender.id_number)
        #             limb.is_intact = False
        #             break

        return super().make_attack(attacker, defender, mean_damage, fight_state)
