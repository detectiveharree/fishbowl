from ai import task
from ai.humanai.actions.actioninteractpersoninitiate import ActionInteractPersonInitiate
from ai.humanai.relationships.interaction.interaction import INTERACTION_TYPE
from ai.need import NEED_TYPE
from ai.humanai.actions.actiongotolocation import ActionGoToLocation
import global_params
from ai.humanai.actions.actionlookforinteractablecell import ActionLookForInteractableCell
from ai.humanai.prerequisites.prerequisiteknowsinteractablecelllocation import PrerequisiteKnowsInteractableCellLocation
from gameworld.cell.cell import CELL_CATEGORY
from gameworld.cell.cellbuilding.cellbuilding import BUILDING_TYPE
from ai.humanai.actions.actioninteractcellbuildinginteract import ActionInteractCellBuildingInteract

class TaskInitiateInteraction(task.Task):


    def __init__(self, interaction_type, human):
        self.human = human

        # DELETE THIS AFTER
        self.human.historical_tasks.append(interaction_type.get_interaction_type())
        # DELETE THIS AFTER

        self.interaction_type = interaction_type

        """
        Helper data for this interaction attempt.
        """
        self.not_possible_people = set()

        self.person_targets = list(self.interaction_type.calculate_interaction_targets(self.human))
        self.current_target = -1
        # print("PID %s" % self.human.id_number)

    def next_target(self):
        # if self.human.id_number == 1:
        #     print("FUCK! %s" % self.person_targets)
        if not self.person_targets:
            self.current_target = -1
            return
        self.current_target = self.person_targets.pop(0)


    def terminate_task_early(self, human):
        human_highest_need = human.current_highest_need.need_type
        return human_highest_need == NEED_TYPE.GROUP_TASK or\
               human_highest_need == NEED_TYPE.HUNGER or\
               human_highest_need == NEED_TYPE.THIRST or\
               human_highest_need == NEED_TYPE.SLEEP or \
               human_highest_need == NEED_TYPE.BETTER_SLEEPING_LOCATION or \
               (human_highest_need == NEED_TYPE.FRUSTRATION and
                self.interaction_type.get_interaction_type() != INTERACTION_TYPE.FIGHT_BRAWL and
                self.interaction_type.get_interaction_type() != INTERACTION_TYPE.FIGHT_BATTLE and
                self.interaction_type.get_interaction_type() != INTERACTION_TYPE.INSULT) or \
               (human_highest_need == NEED_TYPE.ANGER and
                self.interaction_type.get_interaction_type() != INTERACTION_TYPE.FIGHT_BRAWL and
                self.interaction_type.get_interaction_type() != INTERACTION_TYPE.FIGHT_BATTLE and
                self.interaction_type.get_interaction_type() != INTERACTION_TYPE.INSULT) or \
               human_highest_need == NEED_TYPE.NONE


    """
    Possible actions that the user can do to satisfy this pre requisite.
    Note the action with the cheapest action tree will be picked.
    """
    def possible_actions(self):
        return [ActionInteractPersonInitiate(self.interaction_type, self.current_target)]
        # return [ActionInteractCellBuildingInteract(BUILDING_TYPE.TAVERN, self.interaction_type)]


    """
    Called when the action tree is completed.
    Returns True/False. If true, task will terminate, else the task will be restarted via begin()
    Default: returns true
    """
    def is_task_complete(self, human):
        """
        This just confirms that the person does not attempt
        to interact again (although he may have found someone who agrees,
        this task may get activated again)
        """
        return human.needs[NEED_TYPE.CURRENT_INTERACTION] != -1

    """
    Called when the task is begun for the first time.
    Must Return a action tree.
    Default: returns best action tree
    """
    def begin(self, human):
        """
        Since action_failed_response is relied on so often to find another person,
        just use that when we begin.
        """
        return self.action_failed_response(human)


    """
    Called when the proposed action tree returns empty,
    suggesting it was not satisfied.
    Default: removes the persons task
    """
    def action_tree_not_satisfied(self, human):
        # do nothing, aka executes begin which looks for next person
        pass

    """
    Called when the a action in a task has failed.
    Must Return a action tree.
    Default: returns best action tree
    """
    def action_failed_response(self, human):
        """
        is_task_complete not called before action_failed_response
        """
        if human.needs[NEED_TYPE.CURRENT_INTERACTION].need_level != -1:
            return []

        # if person_target
        self.next_target()
        """
        If person has attempted to look for people, and realises none are around,
        just go home. 
        If they still want to socialise after going home,
        begin() will return nothing if there are no possible candidates at all,
        therefore keeping them at home (aka the most likely place they will 
        see someone else)        
        """
        if self.current_target == -1:
            interact_building_action = self.interaction_type.interact_in_building_action()
            if self.interaction_type.interact_in_building_action() is not None:
                building_type = interact_building_action.building_type

                if PrerequisiteKnowsInteractableCellLocation(CELL_CATEGORY.BUILDING, building_type).is_satisfied(human):
                    return self._get_best_action_tree(human, [self.interaction_type.interact_in_building_action()])


            return self._get_best_action_tree(human, [ActionGoToLocation(human.group.stockpile_location)])
        return self._get_best_action_tree(human, self.possible_actions())


    def __repr__(self):
        return str("Initiate interaction (%s)" % self.interaction_type.get_interaction_type())