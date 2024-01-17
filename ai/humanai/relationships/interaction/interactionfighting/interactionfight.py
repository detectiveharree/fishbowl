from enum import Enum
from ai.humanai.relationships.interaction.interactionfighting.attack.attack import ATTACK_TYPES, FIGHT_STATE

from ai.humanai.relationships.interaction.interaction import Interaction, INTERACTION_TYPE
from ai.humanai.relationships.interaction.interactionparticipant import InteractionParticipantInitator, InteractionParticipantParticipant
from ai.humanai.relationships.interaction.interaction import Interaction, PublicInformation
from ai.humanai.relationships.interaction.interactionfighting.fighthelper import *
from items.iteminnovation import calculate_fight_ratio
import random
from ai.need import NEED_TYPE
import logging
import numpy as np
import guiwindow
from enum import Enum
from humanbase import HumanState, HEALTH_CHANGE_TYPE
from abc import ABC, abstractmethod
from gameworld.timestamp import TimeStamp

class InteractionFight(Interaction, ABC):

    """
    DO NOT DELETE THIS. PASTE THIS IN FOR EVERY NEW OBJECT THAT WILL BE STORED IN A SET/DICTIONARY.
    THIS IS ESSENTIAL FOR MAKING SURE THE PROGRAM PERFORMS EXACTLY THE SAME EVERY TIME!

    assert(false) WILL CRASH THE PROGRAM IF YOU ATTEMPT TO PUT THIS OBJECT INTO A SET/DICT WITHOUT FIRST MODIFYING THE FUNCTION.
    THIS IS DONE ON PURPOSE TO PREVENT YOU FROM ACCIDENTALLY LEAKING NON-DETERMINISM INTO THE PROGRAM.
    SPEAK TO ME (TOM) AND I WILL EXPLAIN WHAT TO DO.
    """
    def __hash__(self):
        assert(False)



    def __init__(self, initiator, unarmed,damage_requirement):
        super().__init__(initiator)
        self.fight_state = FIGHT_STATE.FEET
        self.participant1_submission_status = False
        self.participant2_submission_status = False

        # fight state
        self.unarmed = unarmed
        self.damage_requirement = damage_requirement

        # stats for relationships
        self.starting_health_initator = 0
        self.starting_health_participant = 0

        self.starting_stamina_initator = 0
        self.starting_stamina_participant = 0

        self.ending_health_initator = 0
        self.ending_health_participant = 0

        self.damage_taken_initator = 0
        self.damage_taken_participant = 0

        self.initator_weapon = None
        self.participant_weapon = None
        self.winner = None

        self.initiator_fight_score = None
        self.participant_fight_score = None


    """
    For cases when we are looking for person outside of a building.
    Returns a factor to multiply target score on based by their distance.
    Return -1 to indicate too far and skip this person.
    """
    def target_distance_score_factor(self, distance):
        MAX_DISTANCE = 3

        if distance > MAX_DISTANCE:
            return -1

        score = distance / MAX_DISTANCE
        score += 0.1 # just do it's not 0
        return score


    """
    Returns a preference score (0 is most preferred, 1 is least)
    where if a person has a >0 agreeable score, they start to prefer an unfair fight (>0.5 advantage) less.
    The opposite is true for <0 agreeable score, they start to prefer an unfair fight (>0.5 advantage) more.
    Based off of the person's knowledge of the target.
    """
    def get_agreeable_advantage_preference(self, initiator, target_id):

        initator_strength = initiator.body.strength
        initator_health = initiator.body.health.get()
        initator_agreeableness = initiator.personality.agreeable.value


        person_knowledge = initiator.knowledge_of_people.get_knowledge_of_person(target_id)
        participant_health = person_knowledge.health
        participant_strength = person_knowledge.strength

        health_weight = 3

        initator_total_fitness = initator_strength + (initator_health * health_weight)
        participant_total_fitness = participant_strength + (participant_health * health_weight)

        # advantage initator has in a fight
        initator_advantage = initator_total_fitness / (initator_total_fitness + participant_total_fitness)

        # agreeableness: 1 favour initator 0.5 advantage
        # agreeableness: -1 favour initator 1 advantage
        # when their advantage is <0.5, they have the same preference to it


        # the smaller the advantage is, the less they wanna do it
        preference = initator_advantage

        if initator_advantage > 0.5:
            # less favourable the higher advantage given a more agreeable person
            if initator_agreeableness > 0:
                decrement_by = (initator_agreeableness * (initator_advantage - 0.5))
                preference = 1 - (decrement_by * 2)
            # more favourable the higher advantage given a more disagreeble person
            else:
                preference = 0.5 + (initator_agreeableness * (initator_advantage - 0.5) * -1)

        # flip the preference since we were working with opposite scales
        preference *= -1
        preference += 1
        return preference


    """
    Return true/false to indicate whether the person would like to join the interaction.
    This is a static method therefore you cannot use self i.e. data cannot be accessed from this Interaction class
    """
    def participate(self, initiator, target):
        """
        Partcipate if we want to socialise and not currently interacting.
        Note: current_highest_need isn't updated till next tick, therefore
        technically the person's highest need will not become current interaction,
        therefore we also do one additional check on their needs.
        """
        return target.needs[NEED_TYPE.CURRENT_INTERACTION].need_level == -1 and target.body.health.get() > self.damage_requirement


    """
    Gets delta change in initator emotions per tick
    """
    def get_initator_tick_delta_emotions(self, human):
        pass

    """
    Gets delta change in participant emotions per tick
    """
    def get_participant_tick_delta_emotions(self, human):
        pass

    """
    Used when a interaction is starting
    """
    def start_interaction(self, participant):
        self.beginning_time = TimeStamp()

        self.participant = participant

        interaction_participant_1 = InteractionParticipantInitator(self.initiator)
        interaction_participant_2 = InteractionParticipantParticipant(participant)

        interaction_participant_1.other_participant = interaction_participant_2
        interaction_participant_2.other_participant = interaction_participant_1

        self.active_participants[self.initiator.id_number] = interaction_participant_1
        self.active_participants[participant.id_number] = interaction_participant_2


        self.starting_health_initator = self.initiator.body.health.get()
        self.starting_health_participant = self.participant.body.health.get()

        self.starting_stamina_initator = self.initiator.body.stamina.get()
        self.starting_stamina_participant = self.participant.body.stamina.get()

        self.ending_health_initator = self.initiator.body.health.get()
        self.ending_health_participant = self.participant.body.health.get()

        logging.info(self.to_string())

        self.information_interaction = PublicInformation(self.information_interaction_on_begin())
        self.initiator.needs[NEED_TYPE.CURRENT_INTERACTION].start_interaction(self, self.get_need_level(self.initiator))
        self.participant.needs[NEED_TYPE.CURRENT_INTERACTION].start_interaction(self,
                                                                                self.get_need_level(self.participant))


    """
    Return true/false to indicate whether the person would like to join the interaction.
    This is a static method therefore you cannot use self i.e. data cannot be accessed from this Interaction class
    """
    def to_string(self):
        if len(self.active_participants) <= 1:
            return "%s looking for participant (%s) in building %s" % (self.initiator.id_number, self.get_interaction_type(), self.initiator.current_building)
        return "%s (%s) interacting with %s (%s) (%s) in building %s" % (self.initiator.id_number, self.initiator.body.gender,
                                                               self.participant.id_number, self.participant.body.gender,
                                                                self.get_interaction_type(),
                                                               self.initiator.current_building)


    def tick(self, person):
        """
        Fight loop
        """
        if len(self.active_participants) <= 1:
            return False


        # begin actual fight move
        moves = choose_attacker(person.human, person.other_participant.human, self.unarmed)
        if moves is not None:
            attacker, defender = moves
            available_attacks = {}
            for attack in fight_state_available_attacks_cache[self.fight_state]:
                if attack.prerequisites(attacker, self.unarmed):
                    available_attacks[attack] = attack.get_damage(attacker, defender, self.fight_state)

            #print(available_attacks)
            chosen_attack = choose_attack(attacker, available_attacks)

            # print(person.human.body.health , person.other_participant.human.body.health)
            #print(attacker.id_number, attacker.body.health, defender.id_number, defender.body.health,)
            (self.fight_state, damage) = chosen_attack.make_attack(attacker, defender, available_attacks[chosen_attack], self.fight_state)


            # logging.info("%s -> %s | %s (%s%%) %s (%s%%) %s (%s%%)" % (old_fight_state, self.fight_state, attacker.id_number,
            #                                 round(attacker.body.health.get(), 2),
            #                                 chosen_attack, round(damage, 2),
            #                                 defender.id_number,
            #                                 round(defender.body.health.get(), 2)))

            # decrement health of defender
            decrement_damage(attacker, defender, damage, self.unarmed, self.get_interaction_type(), self.damage_requirement)
            attacker.change_stamina(-attacker.body.stamina_cost_per_attack)


        else:
            # print("Both %s and %s don't have enough stamina to attack!" % (person.human.id_number, person.other_participant.human.id_number))
            pass

        self.participant1_submission_status, self.participant2_submission_status = check_submission_status(person.human, person.other_participant.human, self.damage_requirement)

        if self.participant1_submission_status or self.participant2_submission_status:

            winner, loser = (person.human, person.other_participant.human) if self.participant2_submission_status else (person.other_participant.human, person.human)
            logging.info("%s (%s%%) submitted to %s (%s%%)" % (loser.id_number, round(loser.body.health.get(), 2), winner.id_number, round(winner.body.health.get(), 2)))

            self.winner = winner
            self.ending_health_initator = self.initiator.body.health.get()
            self.ending_health_participant = self.participant.body.health.get()
            self.damage_taken_initator = self.starting_health_initator - self.ending_health_initator
            self.damage_taken_participant = self.starting_health_participant - self.ending_health_participant

            """
            Only if these conditions are correct we create theoretical participants from the fight
            """
            if not self.unarmed:
                if not (self.damage_taken_initator == 0 and self.damage_taken_participant == 0):
                    self.initiator_fight_score = calculate_fight_ratio(self.damage_taken_participant, self.damage_taken_initator)
                    self.participant_fight_score = calculate_fight_ratio(self.damage_taken_initator, self.damage_taken_participant)

            return False

        return True


"""
This function checks whether the humans have submitted
"""
def check_submission_status(human1, human2, damage_requirement):
    return ((human1.body.health.get() <= damage_requirement) or human1.state == HumanState.INCAPACITATED or human1.state == HumanState.DEAD,
            (human2.body.health.get() <= damage_requirement) or human2.state == HumanState.INCAPACITATED or human2.state == HumanState.DEAD)
