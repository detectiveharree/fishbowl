from ai.humanai.relationships.information.informationinteraction.informationinteraction import InformationInteraction
from ai.humanai.relationships.interaction.interaction import INTERACTION_TYPE
import guiwindow


class InformationInteractionFight(InformationInteraction):

    """
    DO NOT DELETE THIS. PASTE THIS IN FOR EVERY delta OBJECT THAT WILL BE STORED IN A SET/DICTIONARY.
    THIS IS ESSENTIAL FOR MAKING SURE THE PROGRAM PERFORMS EXACTLY THE SAME EVERY TIME!

    assert(false) WILL CRASH THE PROGRAM IF YOU ATTEMPT TO PUT THIS OBJECT INTO A SET/DICT WITHOUT FIRST MODIFYING THE FUNCTION.
    THIS IS DONE ON PURPOSE TO PREVENT YOU FROM ACCIDENTALLY LEAKING NON-DETERMINISM INTO THE PROGRAM.
    SPEAK TO ME (TOM) AND I WILL EXPLAIN WHAT TO DO.
    """
    def __hash__(self):
        assert(False)

    """
    Because we'll be associating alot of information with a fight, it will not be feasible
    to make a copy of it for every witness, therefore we pass in the actual interactionfight object
    which stores much of the info.
    """
    def __init__(self, interaction_id, initiator_id, participant_id,
                 interaction_fight):
        super().__init__(interaction_id, initiator_id, participant_id)

        self.strength_initator = interaction_fight.initiator.body.strength
        self.strength_participant = interaction_fight.participant.body.strength
        self.starting_health_initator = interaction_fight.starting_health_initator
        self.starting_health_participant = interaction_fight.starting_health_participant
        self.starting_stamina_initator = interaction_fight.starting_stamina_initator
        self.starting_stamina_participant = interaction_fight.starting_stamina_participant
        self.ending_health_initator = interaction_fight.ending_health_initator
        self.ending_health_participant = interaction_fight.ending_health_participant
        self.damage_taken_initator = interaction_fight.starting_health_initator - interaction_fight.ending_health_initator
        self.damage_taken_participant = interaction_fight.starting_health_participant - interaction_fight.ending_health_participant
        self.winner = interaction_fight.winner
        self.unarmed = interaction_fight.unarmed
        self.damage_requirement = interaction_fight.damage_requirement
        self.initiator_fight_score = interaction_fight.initiator_fight_score
        self.participant_fight_score = interaction_fight.participant_fight_score




    """
    Returns tuple of theoretical particicreate_theoretical_fightpants.
    (TheoreticalHuman (perspective), TheoreticalHuman (other) )
    """
    def get_fight_score(self, human_perspective_id):
        if human_perspective_id == self.initiator_id:
            return self.initiator_fight_score
        return self.participant_fight_score


    """
    Meant for the initiator, since he starts the fight.
    If the fight is not fair, i.e. they have vastly different starting healths
    Calculate some delta love, fear and respect deltas.
    Returns (delta_love_init, delta_fear_init, delta_respect_init)
    """
    def fair_fight_from_health_memory_values(self, fair_fight_constant=80):
        delta_love_init, delta_fear_init, delta_respect_init = 0, 0, 0
        """
        If initator started fight with more health: decrease his respect and love
        If initator started fight with less health: increase his love and fear
        """
        delta_starting_health_multiplier = (abs(self.starting_health_initator - self.starting_health_participant) / 100)

        if self.starting_health_initator > self.starting_health_participant:
            delta_respect_init += -(fair_fight_constant * delta_starting_health_multiplier)
            delta_love_init += -(fair_fight_constant * delta_starting_health_multiplier) * 3

        else:
            delta_respect_init += (fair_fight_constant * delta_starting_health_multiplier) * 2
            delta_fear_init += (fair_fight_constant * delta_starting_health_multiplier) * 3

        return (delta_love_init, delta_fear_init, delta_respect_init)

    """
    Meant for the initiator, since he starts the fight.
    If the fight is not fair, i.e. they have vastly different strengths
    Calculate some delta love, fear and respect deltas.
    Returns (delta_love_init, delta_fear_init, delta_respect_init)
    """
    def fair_fight_from_strength_memory_values(self, fair_fight_constant=80):
        delta_love_init, delta_fear_init, delta_respect_init = 0, 0, 0
        """
        If initator started fight with more health: decrease his respect and love
        If initator started fight with less health: increase his love and fear
        """
        delta_starting_health_multiplier = (abs(self.strength_initator - self.strength_participant))

        if self.strength_initator > self.strength_participant:
            delta_respect_init += -(fair_fight_constant * delta_starting_health_multiplier)
            delta_love_init += -(fair_fight_constant * delta_starting_health_multiplier) * 3

        else:
            delta_respect_init += (fair_fight_constant * delta_starting_health_multiplier) * 2
            delta_fear_init += (fair_fight_constant * delta_starting_health_multiplier) * 3

        return (delta_love_init, delta_fear_init, delta_respect_init)

    """
    Meant for both parties.
    Increase respect for either party based on how much damage they received.
    Returns (delta_respect_init, delta_respect_part)
    """
    def damage_taken_respect_memory_values(self, damage_taken_constant=100):

        delta_respect_init = 0
        delta_respect_part = 0
        """
        Both increase respect for one another based on amount of damage they took
        """
        damage_taken_initator_multiplier = (
                    (self.starting_health_initator - self.ending_health_initator) / self.starting_health_initator)
        damage_taken_participant_multiplier = (
                    (self.starting_health_participant - self.ending_health_participant) / self.starting_health_participant)
        delta_respect_init += damage_taken_participant_multiplier * damage_taken_constant
        delta_respect_part += damage_taken_initator_multiplier * damage_taken_constant
        return (delta_respect_init, delta_respect_part)


    """
    Meant for both parties.
    Used to dictate fear, love and respect based on how much damage each party did over the other (proportionally).
    return (delta_love_init, delta_fear_init, delta_respect_init,
            delta_love_part, delta_fear_part, delta_respect_part)
    """
    def damage_difference_memory_values(self, proportional_damage_taken_constant = 100):
        delta_love_init, delta_fear_init, delta_respect_init = 0, 0, 0
        delta_love_part, delta_fear_part, delta_respect_part = 0, 0, 0
        """
        Increase fear and decrease love of other party if one party had more damage taken and do it proportional to damage taken on both sides
        i.e. if both took 30 damage, no change in fear
        """
        difference_damage_taken = 100 / (100 + abs(self.damage_taken_initator - self.damage_taken_participant))
        difference_damage_taken *= -1
        difference_damage_taken += 1

        if self.damage_taken_initator > self.damage_taken_participant:
            delta_fear_part += proportional_damage_taken_constant * difference_damage_taken
            delta_love_part -= proportional_damage_taken_constant * difference_damage_taken
            delta_fear_init -= proportional_damage_taken_constant * difference_damage_taken

        else:
            delta_fear_init += proportional_damage_taken_constant * difference_damage_taken
            delta_love_init -= proportional_damage_taken_constant * difference_damage_taken
            delta_fear_part -= proportional_damage_taken_constant * difference_damage_taken

        return (delta_love_init, delta_fear_init, delta_respect_init,
                delta_love_part, delta_fear_part, delta_respect_part)
