from ai.humanai.relationships.interaction.interactionfighting.attack.attack import Attack, ATTACK_TYPES, FIGHT_STATE
from ai.humanai.relationships.attributes.body.limb import LIMB_TYPE

import numpy as np
from random import randint


class AttackWeapon(Attack):

    """
    Get the type of attack this class does
    """
    @staticmethod
    def get_attack_type():
        return ATTACK_TYPES.WEAPON


    def acceptable_states(self):
        return [FIGHT_STATE.FEET]

    def prerequisites(self, attacker, unarmed):
        if unarmed:
            return False
        return (attacker.body.leftarm.is_intact or attacker.body.rightarm.is_intact)\
               and attacker.inventory.weapon_slot.get_item() is not None

    def get_damage(self, attacker, defender, fight_state):
        damage = 40 * attacker.inventory.weapon_slot.get_item().get_damage(attacker.body.genetic_weight)
        return damage

    def make_attack(self, attacker, defender, mean_damage, fight_state):
        # compute actual damage of attack

        # runs the dismemberments (if the RNG happens)
        # This can defo be shortened lol
        """
        for (limb, chance) in attacker.inventory.weapon_slot.get_item().get_limb_dismemberment_chance():
            if np.random.uniform(0, 1) <= chance:
                if limb == LIMB_TYPE.ARM:
                    if defender.body.leftarm.is_intact and defender.body.rightarm.is_intact:
                        if randint(0, 1) == 0:
                            defender.body.leftarm.dismember(defender)
                        else:
                            defender.body.rightarm.dismember(defender)
                    elif defender.body.leftarm.is_intact:
                        defender.body.leftarm.dismember(defender)
                    else:
                        defender.body.rightarm.dismember(defender)
                elif limb == LIMB_TYPE.LEG:
                    if defender.body.leftleg.is_intact and defender.body.rightleg.is_intact:
                        if randint(0, 1) == 0:
                            defender.body.leftleg.dismember(defender)
                        else:
                            defender.body.rightleg.dismember(defender)
                    elif defender.body.leftleg.is_intact:
                        defender.body.leftleg.dismember(defender)
                    else:
                        defender.body.rightleg.dismember(defender)
                elif limb == LIMB_TYPE.EYE:
                    if defender.body.lefteye.is_intact and defender.body.righteye.is_intact:
                        if randint(0, 1) == 0:
                            defender.body.lefteye.dismember(defender)
                        else:
                            defender.body.righteye.dismember(defender)
                    elif defender.body.lefteye.is_intact:
                        defender.body.lefteye.dismember(defender)
                    else:
                        defender.body.righteye.dismember(defender)
                break
        """
        return (FIGHT_STATE.FEET, mean_damage * attacker.body.strength)
