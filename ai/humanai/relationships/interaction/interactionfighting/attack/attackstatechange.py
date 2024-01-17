from ai.humanai.relationships.interaction.interactionfighting.attack.attack import Attack, ATTACK_TYPES, FIGHT_STATE
import numpy as np
from abc import ABC, abstractmethod


class AttackStateChange(Attack, ABC):

    """
    Get the type of state that will be changed to
    """
    @staticmethod
    @abstractmethod
    def get_new_state():
        ...

    def make_attack(self, attacker, defender, mean_damage, fight_state):
        return (self.get_new_state(), 0)
