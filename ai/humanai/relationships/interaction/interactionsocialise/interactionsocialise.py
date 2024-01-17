from ai.humanai.relationships.interaction.interaction import Interaction, PublicInformation
from abc import ABC, abstractmethod
from ai.humanai.relationships.interaction.interactionparticipant import InteractionParticipantInitator, InteractionParticipantParticipant
from ai.humanai.actions.actioninteractcellsocialisingtavern import ActionInteractCellSocialisingTavern
from ai.need import NEED_TYPE
import logging
from humanbase import HumanState
from gameworld.timestamp import TimeStamp

class InteractionSocialise(Interaction):

    """
    DO NOT DELETE THIS. PASTE THIS IN FOR EVERY NEW OBJECT THAT WILL BE STORED IN A SET/DICTIONARY.
    THIS IS ESSENTIAL FOR MAKING SURE THE PROGRAM PERFORMS EXACTLY THE SAME EVERY TIME!

    assert(false) WILL CRASH THE PROGRAM IF YOU ATTEMPT TO PUT THIS OBJECT INTO A SET/DICT WITHOUT FIRST MODIFYING THE FUNCTION.
    THIS IS DONE ON PURPOSE TO PREVENT YOU FROM ACCIDENTALLY LEAKING NON-DETERMINISM INTO THE PROGRAM.
    SPEAK TO ME (TOM) AND I WILL EXPLAIN WHAT TO DO.
    """
    def __hash__(self):
        assert(False)

    def __init__(self, initiator):
        super().__init__(initiator)
        self.success_constant = 0
        self.begin_time = None

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


        self.success_constant = self.calculate_success_constant()
        logging.info(self.to_string())

        self.information_interaction = PublicInformation(self.information_interaction_on_begin())
        self.initiator.needs[NEED_TYPE.CURRENT_INTERACTION].start_interaction(self, self.get_need_level(self.initiator))
        self.participant.needs[NEED_TYPE.CURRENT_INTERACTION].start_interaction(self, self.get_need_level(self.participant))
        self.begin_time = TimeStamp()


    """
    Return true/false to indicate whether the person would like to join the interaction.
    This is a static method therefore you cannot use self i.e. data cannot be accessed from this Interaction class
    """
    def to_string(self):
        if len(self.active_participants) <= 1:
            return "%s looking for participant (%s) in building %s" % (self.initiator.id_number, self.get_interaction_type(), self.initiator.current_building)
        return "%s (%s | %s) is socialising (%s) with %s (%s | %s) (%s) in building: %s" % (self.initiator.id_number, self.initiator.body.gender,
                                                                  self.initiator.body.age,
                                                                  self.get_interaction_type(),
                                                                  self.participant.id_number,
                                                                  self.participant.body.gender,
                                                                  self.participant.body.age,
                                                                  self.success_constant,
                                                                  self.initiator.current_building)



    """
    Gets delta change in emotions for participants
    For socialise boredom, the emotion change is symmetric
    """
    def get_participants_tick_delta_emotions(self, human):
        pass

    """
    Gets delta change in initator emotions per tick
    """
    def get_initator_tick_delta_emotions(self, human):
        self.get_participants_tick_delta_emotions(human)

    """
    Gets delta change in participant emotions per tick
    """
    def get_participant_tick_delta_emotions(self, human):
        self.get_participants_tick_delta_emotions(human)


    """
    If the person couldn't find anyone to interact with, execute this action to 
    go to a ActionInteractCellBuildingInteract variant that will cause the person to go interact
    there.
    Return None if you don't want the interaction to be done in a building
    """
    def interact_in_building_action(self):
        return ActionInteractCellSocialisingTavern(self)


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
        return target.needs[NEED_TYPE.CURRENT_INTERACTION].need_level == -1 and \
               target.state == HumanState.AWAKE and target.current_highest_need.need_type == NEED_TYPE.BOREDOM

    """
    Calculate a pre-determined constant indicating how successful a interaction will be at start.
    Must return a number between -1 and 1 
    """
    @abstractmethod
    def calculate_success_constant(self):
        ...


    def tick(self, interaction_participant):
        """
        Updates current interaction need level.
        """
        interaction_participant.human.needs[NEED_TYPE.CURRENT_INTERACTION].need_level = self.get_need_level(interaction_participant.human)
        return True

    """
    Return the need level the person will have CURRENT_INTERACTION set to
    """
    def get_need_level(self, human):
        return human.needs[NEED_TYPE.BOREDOM].need_level + human.needs[NEED_TYPE.BOREDOM].minimum_level_for_switch()