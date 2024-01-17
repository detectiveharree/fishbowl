from ai.action import Action
from ai.humanai.prerequisites.prerequisiteatinteractablecell import PrerequisiteAtInteractableCell
from ai.humanai.actions.actioninteractcell import ActionInteractCell
from gameworld.cell.cell import CELL_CATEGORY
import global_params
import guiwindow
from ai.humanai.actions.actioninteractpersoninitiate import ActionInteractPersonInitiate
from ai.humanai.actions.actioninteractperson import ActionInteractPerson
from ai.need import NEED_TYPE
import logging
import guiwindow

"""
Harvests a resource that player is currently on

A wrapper for performing an action, including a cost function, prerequisite conditions and worker logic.
"""


class ActionInteractCellBuildingInteract(ActionInteractCell):

    """
    DO NOT DELETE THIS. PASTE THIS IN FOR EVERY NEW OBJECT THAT WILL BE STORED IN A SET/DICTIONARY.
    THIS IS ESSENTIAL FOR MAKING SURE THE PROGRAM PERFORMS EXACTLY THE SAME EVERY TIME!

    assert(false) WILL CRASH THE PROGRAM IF YOU ATTEMPT TO PUT THIS OBJECT INTO A SET/DICT WITHOUT FIRST MODIFYING THE FUNCTION.
    THIS IS DONE ON PURPOSE TO PREVENT YOU FROM ACCIDENTALLY LEAKING NON-DETERMINISM INTO THE PROGRAM.
    SPEAK TO ME (TOM) AND I WILL EXPLAIN WHAT TO DO.
    """
    def __hash__(self):
        assert(False)


    def __init__(self, building_type, interact_type):
        super().__init__(CELL_CATEGORY.BUILDING, building_type) # ALWAYS CALL PARENT CONSTRUCTOR
        self.building_type = building_type
        """
        If someone else starts interaction with this person, they will give this person their interaction type.
        So make sure we have storage of old interaction type so we can swap it back after interaction is complete.
        E.g. someone may be looking to banter, but then someone romances. In that case perform romance but swap 
        back round to banter after.
        """
        self.interact_type = interact_type
        self.inital_interact_type = interact_type

        self.interaction_targets = []
        self.current_interaction_target = None


    def pre_begin_checks(self, human):

        if human.needs[NEED_TYPE.CURRENT_INTERACTION].currently_interacting():
            return False
        if not super().pre_begin_checks(human):
            return False
        return True

    """
    Cycles through interaction targets in building
    """
    def get_next_interaction_target(self, human):
        if len(self.interaction_targets) == 0:
            self.interaction_targets = self.interact_type.calculate_interaction_targets_in_building(human)
            if len(self.interaction_targets) == 0:
                return -1
        return self.interaction_targets.pop(0)


    def tick(self, human):
        human.group.average_member_locations.append(human.location)


        if human.needs[NEED_TYPE.CURRENT_INTERACTION].currently_interacting():
            participant = self.interact_type.get_interaction_participant(human)
            if not self.interact_type.tick(participant):
                self.interact_type.leave_interaction(self.interact_type.get_interaction_participant(human))
                # swap back to old interaction type (in case someone give this person their interaction type)
                self.interact_type = self.inital_interact_type
                return True

        if human.needs[NEED_TYPE.CURRENT_INTERACTION].need_level == -1:
            self.current_interaction_target = self.get_next_interaction_target(human)

            # since the people to look for was calculated some time ago, it can be the case
            # they left the building. hence check if still valid
            if not self.interact_type.valid_interaction_target_in_building(human, self.current_interaction_target):
                return True

            if self.current_interaction_target == -1:
                return True
            # does checks if participant wants to interact and if so initalises interact state for both
            if self.current_interaction_target in guiwindow.WORLD_INSTANCE.humanDict.keys():
                if ActionInteractPersonInitiate(self.interact_type, self.current_interaction_target).pre_begin_checks(human):
                        guiwindow.WORLD_INSTANCE.humanDict[self.current_interaction_target].current_action.interact_type = self.interact_type



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
        super().on_finish(human)

    def __str__(self):
        return "Interact (%s) with %s in building %s" % (self.interact_type.get_interaction_type(), self.current_interaction_target, self.building_type)
