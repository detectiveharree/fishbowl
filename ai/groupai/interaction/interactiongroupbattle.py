from ai.humanai.relationships.interaction.interaction import Interaction, INTERACTION_TYPE
from ai.humanai.relationships.information.informationinteraction.informationinteractionfightbattle import InformationInteractionFightBattle
from ai.humanai.relationships.interaction.interactionparticipant import InteractionParticipantInitator, InteractionParticipantParticipant
from ai.groupai.interaction.interactionparticipantgroup import InteractionGroupParticipant, BATTLE_RESULT
from ai.groupai.interaction.interactiongroup import InteractionGroup
from ai.groupai.task.caravan.taskgroupcaravanbattle import TaskGroupCaravanBattle, BATTLE_ACTION
from ai.need import NEED_TYPE
import logging
from enum import Enum
from ai import pathfinding
from ai.humanai.relationships.information.informationlocationpeople import InformationLocationPeople
import copy
import guiwindow




class BATTLE_DECISION(Enum):
    PROCEED = 1 # proceed with battle
    SURRENDER = 2 # surrender become subjagated

    def __repr__(self):
        return self.name




class InteractionGroupBattle(InteractionGroup):

    """
    DO NOT DELETE THIS. PASTE THIS IN FOR EVERY NEW OBJECT THAT WILL BE STORED IN A SET/DICTIONARY.
    THIS IS ESSENTIAL FOR MAKING SURE THE PROGRAM PERFORMS EXACTLY THE SAME EVERY TIME!

    assert(false) WILL CRASH THE PROGRAM IF YOU ATTEMPT TO PUT THIS OBJECT INTO A SET/DICT WITHOUT FIRST MODIFYING THE FUNCTION.
    THIS IS DONE ON PURPOSE TO PREVENT YOU FROM ACCIDENTALLY LEAKING NON-DETERMINISM INTO THE PROGRAM.
    SPEAK TO ME (TOM) AND I WILL EXPLAIN WHAT TO DO.
    """
    def __hash__(self):
        assert(False)



    def __init__(self, initiator_army, participant_army, initiator_battle_over_callback, participant_battle_over_callback):
        super().__init__(initiator_army, participant_army, initiator_battle_over_callback, participant_battle_over_callback)

        self.battlefield_location = None
        self.initator_battlefield_location = None
        self.participant_battlefield_location = None
        self.STARTING_DISTANCE = 5 # radius from battlefield center each group will wait/mark their safe zone
        self.start_timer = 0
        self.WAIT_START_TICKS = 50  # once both in position, how many ticks to wait before proceeding
        self.wait_period_over = False
        self.battle_reobserve_timer = 0
        self.battle_reobserve_timer_max = 100




    """
    Used when a interaction is starting
    """
    def start_interaction(self):

        route = list(pathfinding.get_route(self.initiator.caravan_group.stockpile_location,
                                           self.participant.caravan_group.stockpile_location))
        self.battlefield_location = route[max(round(len(route)/2), len(route)-1)]
        self.initator_battlefield_location = route[max(0, round(len(route)/2)-self.STARTING_DISTANCE)]
        self.participant_battlefield_location = route[min(round(len(route)/2)+self.STARTING_DISTANCE, len(route)-1)]

        interaction_participant_1 = InteractionGroupParticipant(self.initiator)
        interaction_participant_2 = InteractionGroupParticipant(self.participant)

        interaction_participant_1.other_group = interaction_participant_2
        interaction_participant_1.starting_position_location = self.initator_battlefield_location
        interaction_participant_2.other_group = interaction_participant_1
        interaction_participant_2.starting_position_location = self.participant_battlefield_location

        self.active_participants[self.initiator.caravan_group.id_number] = interaction_participant_1
        self.active_participants[self.participant.caravan_group.id_number] = interaction_participant_2

        logging.info("%s (%s) is battling %s (%s)" % (self.initiator.caravan_group.id_number,
                                                      self.initiator.original_group.id_number,
                                                      self.participant.caravan_group.id_number,
                                                      self.participant.original_group.id_number,
                                                      ))


        self.initiator.caravan_group.add_task(TaskGroupCaravanBattle(self.initiator.caravan_group, interaction_participant_1, self, callback=self.initiator_battle_over_callback))
        self.participant.caravan_group.add_task(TaskGroupCaravanBattle(self.participant.caravan_group, interaction_participant_2, self, callback=self.participant_battle_over_callback))



    """
    Returns true when battle is ready to begin,
    i.e. both of them at the correct starting location
    """
    def both_at_starting_position(self):
        return self.active_participants[self.initiator.caravan_group.id_number].at_battle_starting_position and\
               self.active_participants[self.participant.caravan_group.id_number].at_battle_starting_position


    """
    Have members of both armies observe each other
    so they have some information for the battle
    """
    def observe_enemy_armies(self):
        locations_initators = set([member.location for member in self.initiator.caravan_group.members])
        locations_participants = set([member.location for member in self.participant.caravan_group.members])

        for member in list(self.initiator.caravan_group.members):
            for location in locations_participants:

                cell = (guiwindow.WORLD_INSTANCE.world[location[0]][location[1]])

                current_people_on_cell_copy = copy.deepcopy(cell.people_on_cell)
                if member.id_number in current_people_on_cell_copy:
                    current_people_on_cell_copy.remove(member.id_number)

                InformationLocationPeople(location, current_people_on_cell_copy).register_to_knowledge(member)

        for member in list(self.participant.caravan_group.members):
            for location in locations_initators:

                cell = (guiwindow.WORLD_INSTANCE.world[location[0]][location[1]])

                current_people_on_cell_copy = copy.deepcopy(cell.people_on_cell)
                if member.id_number in current_people_on_cell_copy:
                    current_people_on_cell_copy.remove(member.id_number)

                InformationLocationPeople(location, current_people_on_cell_copy).register_to_knowledge(member)



    def pre_battle_tick(self):
        """
        Fight loop
        """
        if len(self.active_participants) <= 1:
            return False

        # once start timer started, keep incrementing
        if self.start_timer != 0:
            self.start_timer += 1
        # both at starting position make decision on what to do
        if self.both_at_starting_position() and self.start_timer == 0:
            self.observe_enemy_armies()
            self.start_timer += 1

        # decision made, do as you proceed
        if self.start_timer == self.WAIT_START_TICKS:
            self.wait_period_over = True
            return False
        return True



    def battle_tick(self, group_participant):
        """
        Fight loop
        """
        self.battle_reobserve_timer += 1

        if len(self.active_participants) <= 1:
            return False

        if group_participant.should_surrender():
            logging.info("%s has surrendered to %s in battle" % (group_participant.group.id_number, group_participant.other_group.group.id_number))
            group_participant.battle_outcome = BATTLE_RESULT.LOST
            group_participant.other_group.battle_outcome = BATTLE_RESULT.WON
            return False

        """
        Reobserve every x amount of time to make sure
        participants don't lose each other (common for smaller fights)
        """
        if self.battle_reobserve_timer >= self.battle_reobserve_timer_max:
            self.observe_enemy_armies()
            self.battle_reobserve_timer = 0

        return True
