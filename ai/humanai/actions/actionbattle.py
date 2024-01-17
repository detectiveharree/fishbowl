from ai.humanai.actions.actioninteractcell import ActionInteractCell
from gameworld.cell.cell import CELL_CATEGORY
from ai.humanai.actions.actioninteractpersoninitiate import ActionInteractPersonInitiate
from ai.need import NEED_TYPE
import guiwindow
from ai.humanai.prerequisites.prerequisiteknowspersonlocation import PrerequisiteKnowsPersonLocation
from ai.humanai.actions.actiongotoperson import ActionGoToPerson
from ai.humanai.relationships.interaction.interactionfighting.interactionfightbattle import InteractionFightBattle
from ai.action import Action
from humanbase import HumanState
import logging

"""
Harvests a resource that player is currently on

A wrapper for performing an action, including a cost function, prerequisite conditions and worker logic.
"""


class ActionBattle(Action):

    """
    DO NOT DELETE THIS. PASTE THIS IN FOR EVERY NEW OBJECT THAT WILL BE STORED IN A SET/DICTIONARY.
    THIS IS ESSENTIAL FOR MAKING SURE THE PROGRAM PERFORMS EXACTLY THE SAME EVERY TIME!

    assert(false) WILL CRASH THE PROGRAM IF YOU ATTEMPT TO PUT THIS OBJECT INTO A SET/DICT WITHOUT FIRST MODIFYING THE FUNCTION.
    THIS IS DONE ON PURPOSE TO PREVENT YOU FROM ACCIDENTALLY LEAKING NON-DETERMINISM INTO THE PROGRAM.
    SPEAK TO ME (TOM) AND I WILL EXPLAIN WHAT TO DO.
    """
    def __hash__(self):
        assert(False)


    def __init__(self, human, group_action, personal_safe_zone_location):
        """
        If someone else starts interaction with this person, they will give this person their interaction type.
        So make sure we have storage of old interaction type so we can swap it back after interaction is complete.
        E.g. someone may be looking to banter, but then someone romances. In that case perform romance but swap 
        back round to banter after.
        """
        self.interact_type = InteractionFightBattle(human,
                                                    group_action.damage_requirement,
                                                    group_action.interaction_group_participant.other_group.group)


        self.inital_interact_type = self.interact_type
        self.group_action = group_action

        self.interaction_targets = []
        self.current_interaction_target = None
        self.looking_for_person = False
        self.believed_target_location = None
        self.personal_safe_zone_location = personal_safe_zone_location



    """
    This is called once when the action begins.
    """
    def begin(self, human):
        self.group_action.interaction_group_participant.soldier_join_battle(human)
        pass

    """
    The estimated cost of this action.
    This occurs during the decision making process of a action tree.
    For extra accuracy, use data from prerequisites.
    """
    def get_costs(self, human):
        return 0


    """
    Cycles through interaction targets in building
    """
    def get_next_interaction_target(self, human):
        if len(self.interaction_targets) == 0:
            self.interaction_targets = self.interact_type.calculate_interaction_targets(human)
            if len(self.interaction_targets) == 0:
                return -1
        return self.interaction_targets.pop(0)


    def tick(self, human):


        # currently fighting
        if human.needs[NEED_TYPE.CURRENT_INTERACTION].currently_interacting():
            participant = self.interact_type.get_interaction_participant(human)
            if not self.interact_type.tick(participant):
                self.interact_type.leave_interaction(self.interact_type.get_interaction_participant(human))
                # swap back to old interaction type (in case someone give this person their interaction type)
                self.interact_type = self.inital_interact_type
                return True

        """
        Acquire and start new fight loop        
        """
        if human.needs[NEED_TYPE.CURRENT_INTERACTION].need_level == -1:
            """
            Regen in safe location for a bit
            """
            if human.body.health.get() < 100:
                if human.location != self.personal_safe_zone_location:
                    if human.arrived_at_location():
                        human.find(self.personal_safe_zone_location)
                    human.step_towards_route()

                return True

            """
            Look for person to fight
            """

            if not self.looking_for_person:
                self.current_interaction_target = self.get_next_interaction_target(human)
                if self.current_interaction_target == -1:
                    self.looking_for_person = True
                    human.find(self.personal_safe_zone_location)
                    return True
                if not PrerequisiteKnowsPersonLocation(self.current_interaction_target).is_satisfied(human):
                    return True
                self.believed_target_location = PrerequisiteKnowsPersonLocation(self.current_interaction_target).get_data(human)
                human.find(self.believed_target_location)
                self.looking_for_person = True

            # complete if we run into person
            if self.current_interaction_target != -1:
                if human.knowledge_people_locations.knows_people_at_location(human.location):
                    if self.current_interaction_target in human.knowledge_people_locations.get_people_at_location(human.location):
                        human.route = []
                        # does checks if participant wants to interact and if so initalises interact state for both
                        # AKA FIGHT BEGIN
                        logging.info("%s -> %s | %s" % (human.id_number, self.current_interaction_target,
                                                        guiwindow.WORLD_INSTANCE.humanDict[
                                                            self.current_interaction_target].current_action))

                        """
                        YES this check is justified.
                        It should be expected that not all people they target have yet executed battle action tree,
                        or part of the battle at all.                     
                        """
                        if isinstance(guiwindow.WORLD_INSTANCE.humanDict[self.current_interaction_target].current_action, ActionBattle)\
                                and ActionInteractPersonInitiate(self.interact_type, self.current_interaction_target).pre_begin_checks(human):

                            logging.info(guiwindow.WORLD_INSTANCE.humanDict[self.current_interaction_target].current_action)
                            guiwindow.WORLD_INSTANCE.humanDict[self.current_interaction_target].current_action.interact_type = self.interact_type
                        # Person doesn't/cant fight so reset
                        self.looking_for_person = False
                        return True
            # couldn't find person
            if human.arrived_at_location():
                self.looking_for_person = False
                return True

            human.step_towards_route()


        return True

    """
    Returns true/false to indicate whether the action is complete or not.
    Called every tick before tick() is executed.    
    """
    def is_complete(self, human):
        return False

    """
    Called whenever a action is completed 
    """
    def on_finish(self, human):
        if self.interact_type.human_in_interaction(human):
            self.interact_type.leave_interaction(self.interact_type.get_interaction_participant(human))
        self.group_action.interaction_group_participant.soldier_leave_battle(human)


    def __str__(self):
        return "Battling"
