import random
import numpy as np
from ai.humanai.relationships.interaction.interactionfighting.attack.attack import ATTACK_TYPES, FIGHT_STATE
from ai.humanai.relationships.interaction.interactionfighting.attack.attacksunarmed.attackchoke import AttackChoke
from ai.humanai.relationships.interaction.interactionfighting.attack.attacksunarmed.attackelbow import AttackElbow
from ai.humanai.relationships.interaction.interactionfighting.attack.attacksstatechange.attackenterclinch import AttackEnterClinch
from ai.humanai.relationships.interaction.interactionfighting.attack.attacksstatechange.attackenterfeet import AttackEnterFeet
from ai.humanai.relationships.interaction.interactionfighting.attack.attacksstatechange.attackenterground import AttackEnterGround
from ai.humanai.relationships.interaction.interactionfighting.attack.attacksunarmed.attackeyegouge import AttackEyeGouge
from ai.humanai.relationships.interaction.interactionfighting.attack.attacksunarmed.attackheadbut import AttackHeadBut
from ai.humanai.relationships.interaction.interactionfighting.attack.attacksunarmed.attackkick import AttackKick
from ai.humanai.relationships.interaction.interactionfighting.attack.attacksunarmed.attackknee import AttackKnee
from ai.humanai.relationships.interaction.interactionfighting.attack.attacksunarmed.attackpunch import AttackPunch
from ai.humanai.relationships.interaction.interactionfighting.attack.attackweapon import AttackWeapon
from ai.humanai.relationships.interaction.interaction import ANGER_REASON
from humanbase import HEALTH_CHANGE_TYPE
from ai.humanai.relationships.interaction.interaction import INTERACTION_TYPE
from ai.humanai.relationships.interaction.interaction import FRUSTRATION_REASON


all_attack_types = {ATTACK_TYPES.PUNCH:AttackPunch(), ATTACK_TYPES.KICK:AttackKick(), ATTACK_TYPES.ELBOW:AttackElbow(),
                    ATTACK_TYPES.KNEE:AttackKnee(), ATTACK_TYPES.WEAPON:AttackWeapon(),
                    ATTACK_TYPES.HEADBUTT:AttackHeadBut(), ATTACK_TYPES.EYE_GOUGE:AttackEyeGouge(),
                    ATTACK_TYPES.CHOKE:AttackChoke(), ATTACK_TYPES.ENTER_GROUND:AttackEnterGround(),
                    ATTACK_TYPES.ENTER_CLINCH:AttackEnterClinch(), ATTACK_TYPES.ENTER_FEET:AttackEnterFeet()}

fight_state_available_attacks_cache = {FIGHT_STATE.FEET : set([attack for attack in all_attack_types.values() if FIGHT_STATE.FEET in attack.acceptable_states()]),
                                       FIGHT_STATE.CLINCH : set([attack for attack in all_attack_types.values() if FIGHT_STATE.CLINCH in attack.acceptable_states()]),
                                       FIGHT_STATE.GROUND : set([attack for attack in all_attack_types.values() if FIGHT_STATE.GROUND in attack.acceptable_states()])}


def decrement_damage(attacker, defender, damage, unarmed, fight_type, damage_requirement):

    prot = 1
    if not unarmed:
        if not defender.inventory.armour_chest_slot.is_empty():
            prot *= defender.inventory.armour_chest_slot.get_item().get_protection(defender.body.genetic_weight)
        if not defender.inventory.armour_plate_slot.is_empty():
            prot *= defender.inventory.armour_plate_slot.get_item().get_protection(defender.body.genetic_weight)


    # damage = max(np.random.normal(mean_damage, mean_damage / 5), 0)

    defender.change_health(-damage * prot, HEALTH_CHANGE_TYPE.FIGHT)

    if fight_type == INTERACTION_TYPE.FIGHT_TRAINING:
        """
        For every hit, the attacker gains some happiness
        and the defender gets frustrated.
        Attacker becomes less frustrated after every hit
        
        If defenders health drops below agreed damage requirement,
        he becomes scared
        """
        damage_to_frustration_defender = damage / 4
        damage_to_frustration_attacker = -damage / 3
        damage_to_happiness = damage / 2
        defender.emotions.frustration.change(defender, damage_to_frustration_defender, FRUSTRATION_REASON.TOOK_HIT_FIGHT)
        attacker.emotions.frustration.change(attacker, damage_to_frustration_attacker, None)
        attacker.emotions.happiness.change(attacker, damage_to_happiness)
        if defender.body.health.get() < damage_requirement:
            delta = damage_requirement - defender.body.health.get()
            defender.emotions.fear.change(defender, delta)
    elif fight_type == INTERACTION_TYPE.FIGHT_BRAWL:
        """
        IF defender takes a hit he becomes a bit frustrated 
        IF attacker hits he becomes a bit less frustrated 
        Anger is changed proportionally too
        """
        damage_to_frustration_defender = damage / 8
        damage_to_frustration_attacker = -damage / 6
        defender.emotions.frustration.change(defender, damage_to_frustration_defender, FRUSTRATION_REASON.TOOK_HIT_FIGHT)
        attacker.emotions.frustration.change(attacker, damage_to_frustration_attacker, None)
        attacker.emotions.anger.change(attacker, damage_to_frustration_attacker * 2, None)
        if defender.body.health.get() < damage_requirement:
            delta = damage_requirement - defender.body.health.get()
            defender.emotions.fear.change(defender, delta)
    elif fight_type == INTERACTION_TYPE.FIGHT_BATTLE:
        """
        IF defender takes a hit he becomes a bit frustrated 
        IF attacker hits he becomes a bit less frustrated 
        Anger and fear is changed proportionally too
        """
        damage_to_frustration_defender = damage / 8
        damage_to_frustration_attacker = -damage / 6
        defender.emotions.frustration.change(defender, damage_to_frustration_defender, FRUSTRATION_REASON.TOOK_HIT_FIGHT)
        attacker.emotions.frustration.change(attacker, damage_to_frustration_attacker, None)
        attacker.emotions.anger.change(attacker, damage_to_frustration_attacker * 2, None)
        defender.emotions.fear.change(defender, damage / 2, attacker.id_number)
        attacker.emotions.fear.change(attacker, damage / 2, defender.id_number)






def choose_attack(attacker, available_attacks):

    # choosing the attack (random pick, weighted according to probability)
    # print(available_attacks)
    try:
        chosen_attack = random.choices(list(available_attacks.keys()), weights=list(available_attacks.values()), k=1)[0]
    except Exception as e:
        print("WHAT THE FUCK")
        print(attacker.body)
        print(available_attacks)
        exit()
    return chosen_attack


def choose_attacker(human1, human2, unarmed):
    # the logic is to sum their speeds, and call a uniform distribution between 0 and that sum
    # if the random number is greater than human1's speed, human2 is the attacker
    # this means that the higher speed makes a person more likely to be the attacker
    # (but not exclusively)

    speed1 = 1
    speed2 = 1

    if not unarmed:
        if not human1.inventory.weapon_slot.is_empty():
            speed1 *= human1.inventory.weapon_slot.get_item().get_speed(human1.body.genetic_weight)

        if not human2.inventory.weapon_slot.is_empty():
            speed2 *= human2.inventory.weapon_slot.get_item().get_speed(human2.body.genetic_weight)

    summed_speed = speed1 + speed2
    rand = np.random.uniform(0, summed_speed)

    # ADDITION: if not enough stamina its automatically the other guy
    if rand > speed1 and human2.body.stamina.get() > human2.body.stamina_cost_per_attack:
        # human2 is the attacker
        return (human2, human1)
    elif human1.body.stamina.get() > human1.body.stamina_cost_per_attack:
        # human1 is the attacker
        return (human1, human2)
    return None
