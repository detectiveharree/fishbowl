import numpy as np

import global_params
from humanbase import HumanBase, HumanState, HEALTH_CHANGE_TYPE

from items.humaninventory import HumanInventory
from ai.humanai.relationships.attributes.emotion import EmotionAttributes
# from ai.humanai.relationships.knowledge.knowledgeresourcelocations import KnowledgeResourceLocations
from ai.humanai.relationships.knowledge.knowledgepeople import KnowledgePeople
from ai.humanai.relationships.knowledge.knowledgepeoplelocations import KnowledgePeopleLocations
from ai.humanai.relationships.knowledge.knowledgeinteractablecelllocations import KnowledgeInteractableCellLocations
from ai.humanai.relationships.knowledge.knowledgegroupstockpilesurvivalcontents import KnowledgeGroupStockpileSurvivalContents
from ai.humanai.relationships.knowledge.knowledgegroupstats import KnowledgeGroupStats
from ai.humanai.relationships.knowledge.knowledgepeoplegroups import KnowledgePeopleGroups
from ai.humanai.relationships.knowledge.knowledgeinteractions import KnowledgeInteractions
from ai.humanai.relationships.knowledge.knowledgegroups import KnowledgeGroups
from ai.humanai.relationships.knowledge.knowledgegroupstockpilelocations import KnowledgeGroupStockpileLocations
from ai.humanai.relationships.information.informationlocationcell import InformationLocationCell
from ai.humanai.relationships.information.informationlocationpeople import InformationLocationPeople
from ai.humanai.relationships.information.informationgroupstockpilesurvivalcontents import InformationGroupStockpileSurvivalContents
from ai.humanai.relationships.interaction.interactionfighting.interactionfight import InteractionFight
from ai.humanai.relationships.information.informationpersongroup import InformationPersonGroup
from ai.humanai.relationships.information.informationgroupstockpilelocation import InformationGroupStockpileLocation
from ai.humanai.relationships.information.informationgroupstats import InformationGroupStats
from ai.groupai.knowledge.knowledgegroupcelllocations import KnowledgeGroupCellLocations
from ai.humanai.task.taskinitiateinteraction import TaskInitiateInteraction
from ai.humanai.task.taskinteract import TaskInteract
from entities.groupbase import GroupType
from entities.groupbase import GroupBase, GROUP_BUFFER_FACTOR
from ai.need import NEED_TYPE
from ai.humanai.needs.needsleep import NeedSleep
from ai.humanai.needs.needtrain import NeedTrain
from ai.humanai.needs.needsocial.needsocialboredom import NeedSocialBoredom
from ai.humanai.needs.needsocial.needsocialfrustration import NeedSocialFrustration
from ai.humanai.needs.needsocial.needsocialanger import NeedSocialAnger
from ai.humanai.needs.needfood import NeedFood
from ai.humanai.needs.needwater import NeedWater
from ai.humanai.needs.needsignalgroup import NeedSignalGroup
from ai.humanai.needs.needgrouptask import NeedTaskGroup
from ai.humanai.needs.needcurrentinteraction import NeedCurrentInteraction
from ai.humanai.needs.needbettersleepinglocation import NeedBetterSleepingLocation
from ai.humanai.needs.neednone import NeedNone
from ai.humanai.actions.actioninteractperson import ActionInteractPerson
from ai.humanai.skill import SKILL_TYPE
from ai import pathfinding
import logging
from gameworld.timestamp import TimeStamp

import guiwindow

from entities.group import Group

import copy

"""
Use tuples instead of arrays where possible
Tuple are immutable. FASTER

Use sets instead of lists where possible. FASTER
Dictionaries when you need fast lookups and you know the key.

FURTHER OPTIMISATIONS:
get_unexplored_points could probable be configured so that it doesn't need to be called every tick just on look (maybe)
    for now it will complicate things and im skipping
if there has been no change in task (i.e. human is still navigating to a food source like he was last tick)
    then we could make that route an attribute and use it again and not call get_route_array again
"""



# WARNING: only use self.move() to modify location.

class Human(HumanBase):


    def __init__(self, starting_location, personality, body):

        super().__init__(guiwindow.WORLD_INSTANCE.human_id_counter, location=starting_location) # ALWAYS CALL PARENT CONSTRUCTOR

        # incriment person id whenver new one made
        guiwindow.WORLD_INSTANCE.human_id_counter += 1

        # group:
        self.own_group = Group(starting_location)
        self.own_group.own_group = True
        self.group = None
        self.last_attempt_switch_group = TimeStamp()


        # self.current_group_score = 0

        # sleep
        self.sleep_hour = 0
        self.sleeping_location = None

        # state
        self.state = HumanState.AWAKE
        self.current_building = None

        # attrributes

        self.personality = personality
        self.emotions = EmotionAttributes()
        self.body = body

        # orientation:
        self.explored_points = set()
        self.unexplored_points = set()



        # Memory
        self.knowledge_cell_locations = KnowledgeInteractableCellLocations()
        self.knowledge_of_people = KnowledgePeople(self)
        self.knowledge_people_locations = KnowledgePeopleLocations(self.knowledge_of_people)
        self.knowledge_interactions = KnowledgeInteractions(self.knowledge_of_people, self)


        self.knowledge_groups = KnowledgeGroups(self)
        self.knowledge_group_stockpile_contents = KnowledgeGroupStockpileSurvivalContents(self.knowledge_groups)
        # self.knowledge_people_sleeping_locations = KnowledgePeopleSleepingLocations(self.knowledge_of_people)
        self.knowledge_people_groups = KnowledgePeopleGroups(self.knowledge_groups, self.knowledge_of_people)
        self.knowledge_group_stockpile_locations = KnowledgeGroupStockpileLocations(self.knowledge_groups)
        self.knowledge_group_stats = KnowledgeGroupStats(self.knowledge_groups)

        # skills:
        self.skills = { skill:np.clip(round(np.random.normal(0.5,0.25),2),0.1,1) for skill in list(SKILL_TYPE)}



        # needs:
        self.needs = {}
        self.register_need(NeedFood())
        self.register_need(NeedWater())
        # NOTE: BORED OFTEN LEADS TO INTIMACY IN NEXT TICK (ARE THERE ALGOS TOO CLOSELY ALIGNED?)

        self.register_need(NeedSocialBoredom())
        self.register_need(NeedSocialFrustration())
        self.register_need(NeedSocialAnger())
        self.register_need(NeedTrain()) # DONT DISABLE
        self.register_need(NeedSleep()) # DONT DISABLE
        self.register_need(NeedTaskGroup())
        self.register_need(NeedCurrentInteraction())
        self.register_need(NeedBetterSleepingLocation()) # DONT DISABLE
        self.register_need(NeedSignalGroup())
        self.register_need(NeedNone())  # DONT DISABLE

        self.current_highest_need = self.needs[NEED_TYPE.NONE]


        # working:

        self.inventory = HumanInventory()


        self.route = []

        # tasks/actions
        self.prev_action = None # used to compare if still doing same task

        # current task. WARNING! ONLY CHANGE VIA change_task(new_task)
        self.current_task = None
        self.time_on_current_action = 0
        self.max_ticks_per_action = 1000 # amount of ticks of current action before recalculating current task action tree.

        self.actions = []
        self.current_action = None
        self.historical_tasks = [str(self.personality.to_string())]

        # a convinent place to store this value, but really this should be temp
        self.expected_caravan_location = None

        # debug logic
        self.need_change_debug = ""

        #

        """
        INIT LOGIC
        """


        # register new unexplored points
        self.reset_explored_points()

        guiwindow.WORLD_INSTANCE.world[self.location[0]][self.location[1]].people_on_cell.add(copy.copy(self.id_number))

        # initalise person in world classes
        guiwindow.WORLD_INSTANCE.world[self.location[0]][self.location[1]].people_on_cell.add(self.id_number)
        guiwindow.WORLD_INSTANCE.rerender_location(self.location)

        # register self
        guiwindow.WORLD_INSTANCE.humanDict[self.id_number] = self

        # join your own group (we can never be groupless)
        self.switch_group(self.own_group)
        # just done so we can register knowledge of our group if we spawn into one.
        # set buffer factors as None

        """
        register knowledge/stats of own group.
        This might be the only occasion they record this info if they're born into another group.
        """
        InformationGroupStats(self.own_group.id_number,
                              self.own_group.group_type,
                              self.own_group.buffer_factors[GROUP_BUFFER_FACTOR.FOOD_HARVESTING].value,
                              self.own_group.buffer_factors[GROUP_BUFFER_FACTOR.WATER_HARVESTING].value).register_to_knowledge(self)


    def reset_explored_points(self):
        print("%s is resetting his explored map" % self.id_number)
        self.explored_points.clear()
        self.unexplored_points.clear()
        # register new unexplored points
        for loc in list(pathfinding.perimeter_radius(self.location, 2, 0, 0, 128, 128)):
            if guiwindow.WORLD_INSTANCE.traverse_map[loc[0]][loc[1]] != -1:
                if loc not in self.explored_points:
                    self.unexplored_points.add(loc)



    def register_need(self, need):
        self.needs[need.need_type] = need


    """
    /// ==========================================================================================
    /// DESIGN (non helper functions)
    /// ==========================================================================================
    """
    def tickly_update(self):
        # print("idno %s" % self.id_number)

        # health and stamina tick


        for need in self.needs.values():
            need.tick(self)

        """
        Doesn't really make sense to tick up health in a fight.
        More importantly it leads to fights that never end.
        """
        if self.needs[NEED_TYPE.CURRENT_INTERACTION].interaction_type is None or \
                (not isinstance(self.needs[NEED_TYPE.CURRENT_INTERACTION].interaction_type, InteractionFight)):

            self.change_health(global_params.health_rejuvination_rate, HEALTH_CHANGE_TYPE.HEAL)

        self.change_stamina(global_params.stamina_rejuvination_rate)

        if self.state == HumanState.INCAPACITATED or self.state == HumanState.DEAD:
            self.force_finish_task()
            return



        # if self.id_number == 0:
        #     print(self.emotions.loneliness.value.get())

        if self.state == HumanState.AWAKE:
            if self.needs[NEED_TYPE.CURRENT_INTERACTION].need_level == -1:

                self.emotions.loneliness.change(self, 1)
                self.emotions.happiness.change(self, -1)
                self.emotions.fear.change(self, -1)
                self.emotions.lust.change(self, -1)

                self.emotions.frustration.change(self, -0.5, None)
                self.emotions.anger.change(self, -1, None)
            self.observe_surroundings()
        elif self.state == HumanState.SLEEPING:
            self.emotions.frustration.change(self, -1, None)
            self.emotions.anger.change(self, -1, None)


        """
        Action/task system
        """

        for need in self.needs.values():
            if need.need_level > self.current_highest_need.need_level:
                # has to be above this level
                if need.need_level > need.minimum_level_for_switch():
                    if self.current_highest_need != need:
                        # if self.id_number == 0:
                        #     print("CHANGED (%s) %s -> %s" % (self.id_number, self.current_highest_need.need_type, need.need_type))
                        self.need_change_debug = ("%s -> %s" % (self.current_highest_need.need_type, need.need_type))

                    self.current_highest_need = need

        # corner case, sometimes the current highest need will drop below its minimum level, its important to address this
        if self.current_highest_need.need_level < self.current_highest_need.minimum_level_for_switch():
            # if self.id_number == 0:
            #     print("CHANGED (%s) %s -> NONE" % (self.id_number, self.current_highest_need.need_type))
            self.current_highest_need = self.needs[NEED_TYPE.NONE]


        if self.current_task is None:
            self.change_current_task(self.current_highest_need.get_task(self))
            self.need_over_taken = False





        # if no action work out a action tree for task
        if self.current_action is None and self.current_task is not None:


            self.actions = self.current_task.begin(self)

            if self.actions == []:
                self.current_task.action_tree_not_satisfied(self)
                return
            # print(self.actions)


            self.start_next_action()


        if self.current_task is not None:
            self.current_task.tick(self)
            if self.current_task.terminate_task_early(self):
                # if random.randint(0, 100) == 10:
                # print("YEA FUCK THIS (%s)" % self.id_number )
                # print(self.current_highest_need.need_type)
                self.force_finish_task()

        if self.current_action:



            if self.current_action.is_complete(self):



                if self.actions != []:
                    # start new job
                    self.start_next_action()
                else:
                    self.finish_task()
            else:



                if self.prev_action == self.current_task and self.time_on_current_action >= self.max_ticks_per_action:

                    self.change_current_action(None)
                else:
                    self.time_on_current_action += 1
                    self.prev_action = self.current_action

                    # if current action fails this will cause task action tree to be recalculated on next tick
                    if not self.current_action.tick(self):
                        # potentially something could have happened in tick to cause current task to go to None
                        if self.current_task is not None:
                            self.change_current_action(None)
                            self.actions = self.current_task.action_failed_response(self)
                            if not self.actions:
                                self.finish_task()
                    else:
                        """
                        Its important to start next action i.e. action.begin() right after they finish the previous
                        on the same tick
                        """
                        if self.current_action is None:
                            return

                        if self.current_action.is_complete(self):
                            if self.actions:
                                # start new job
                                self.start_next_action()
                            else:
                                self.finish_task()
        if self.state == HumanState.INCAPACITATED or self.state == HumanState.DEAD:
            self.force_finish_task()


    """
    Called every one hour
    """
    def hourly_update(self):
        pass


    """
    Called at end of day,
    but before the group tick
    """
    def daily_update(self):

        """
        register knowledge/stats of current group.
        this will be used if the person is in a solo group
        (he won't meet people in own group therefore can't
        gain knowledge that way)
        """
        InformationGroupStats(self.group.id_number,
                              self.group.group_type,
                              self.group.buffer_factors[GROUP_BUFFER_FACTOR.FOOD_HARVESTING].value,
                              self.group.buffer_factors[GROUP_BUFFER_FACTOR.WATER_HARVESTING].value).register_to_knowledge(self)

        self.knowledge_groups.group_opinions.calculate_group_scores()

        if TimeStamp().day >= (self.last_attempt_switch_group.day + global_params.min_days_between_group_switch_attempt):
            self.knowledge_groups.join_best_group(self)
            self.last_attempt_switch_group = TimeStamp()

        self.knowledge_of_people.decay_opinions()

    """
    Starts a job, making sure that its pre beginning checks are satisfied.
    """
    def start_next_action(self):
        self.change_current_action(self.actions.pop(0))

        i = 0
        while not self.current_action.pre_begin_checks(self):


            if i >= 100:
                print("Warning: task %s failed at action %s for the %s time" % (self.current_task, self.current_action, i))
            self.actions = self.current_task.action_failed_response(self)


            if not self.actions:
                self.finish_task()
                break
            self.change_current_action(self.actions.pop(0))

            i += 1

        if self.current_action is not None:
            self.current_action.begin(self)

    def finish_task(self):
        self.change_current_action(None)
        if self.current_task is not None:
            if self.current_task.is_task_complete(self):
                self.change_current_task(None)


    def force_finish_task(self):
        self.change_current_action(None)
        self.change_current_task(None)


    def change_current_action(self, action):
        if self.current_action is not None:
            self.current_action.on_finish(self)
        self.current_action = action
        self.time_on_current_action = 0

    """
    WARNING
    Do not set to None.
    If you want to end the current task
    use finish_task
    """
    def change_current_task(self, new_task):
        if self.current_task is not None:
            self.current_task.finish_task(self)
        self.current_task = new_task



    """
    Gets current interaction as string if is one
    """
    def get_current_interaction_to_string(self):
        out = ""

        out += "current interaction: %s\n" % None
        out += "as action: %s\n" % None
        if isinstance(self.current_task, TaskInitiateInteraction) or isinstance(self.current_task, TaskInteract):
            out = ""
            out += "current interaction: %s\n" % self.current_task.interaction_type.to_string()
            out += "as action: %s\n" % self.current_action
        return out



    memory_tick = 0
    """
    Expands personal path
    Registers observations such as player locations, resource locations etc.
    """
    def observe_surroundings(self):

        # if they're on the stockpile update their knowledge of its contents
        if self.location in self.group.knowledge_sleeping_location_tents.get_sleeping_locations():
            InformationGroupStockpileSurvivalContents(self.group.task_survival_food.contents,
                                                      self.group.task_survival_water.contents,
                                                      self.group.id_number).register_to_knowledge(self)

        if self.current_building is not None:
            for person_id in self.current_building.current_occupants:
                if person_id == self.id_number:
                    continue
                self.observe_person(person_id)
            return

        to_observe = list(pathfinding.get_area(self.location, 1, 0, 0, 128, 128))

        for loc in to_observe:
            self.explored_points.add(loc)
            cell = (guiwindow.WORLD_INSTANCE.world[loc[0]][loc[1]])


            # registers cell
            if cell.cell_type is not None:
                cell_base = cell.cell_type.to_cell_base(self)

                InformationLocationCell(cell_base.locations, cell_base).register_to_knowledge(self)
                InformationLocationCell(cell_base.locations, cell_base).register_to_knowledge(self.group)
            else:
                InformationLocationCell({loc}, None).register_to_knowledge(self)
                InformationLocationCell({loc}, None).register_to_knowledge(self.group)



            current_people_on_cell_copy = copy.deepcopy(cell.people_on_cell)
            if self.id_number in current_people_on_cell_copy:
                current_people_on_cell_copy.remove(self.id_number)



            """
            Record observable information regardless.
            """
            for person_id in current_people_on_cell_copy:
                self.observe_person(person_id)

            InformationLocationPeople(loc, current_people_on_cell_copy).register_to_knowledge(self)
            InformationGroupStockpileLocation(loc, cell.group_center).register_to_knowledge(self)






    def observe_person(self, person_id):

        other_human = guiwindow.WORLD_INSTANCE.humanDict[person_id]
        knowledge_person = self.knowledge_of_people.get_knowledge_of_person(person_id)
        knowledge_person.action = other_human.current_action
        knowledge_person.state = other_human.state
        knowledge_person.health = other_human.body.health.get()
        knowledge_person.strength = other_human.body.strength
        knowledge_person.genetic_weight = other_human.body.genetic_weight
        knowledge_person.current_kit_rating = other_human.needs[NEED_TYPE.TRAIN].current_kit_rating
        InformationPersonGroup(other_human.id_number, other_human.group.id_number).register_to_knowledge(self)
        InformationGroupStats(other_human.group.id_number,
                              other_human.group.group_type,
                              other_human.group.buffer_factors[GROUP_BUFFER_FACTOR.FOOD_HARVESTING].value,
                              other_human.group.buffer_factors[GROUP_BUFFER_FACTOR.WATER_HARVESTING].value).register_to_knowledge(self)
        self.group.register_threat(self, other_human)

        if isinstance(other_human.current_action, ActionInteractPerson):
            other_human.current_action.interaction_type.witness_interaction_public_information(self)




    """
    /// ==========================================================================================
    /// PERSONAL MAP   
    /// ==========================================================================================
    """




    def get_personal_map_array(self):
        new_map = np.ndarray((guiwindow.WORLD_INSTANCE.world.shape[0], guiwindow.WORLD_INSTANCE.world.shape[1],),dtype=np.object)
        for loc in self.explored_points:
            new_map[loc[0]][loc[1]] = guiwindow.WORLD_INSTANCE.world[loc[0]][loc[1]]
        return new_map



    """
    /// ==========================================================================================
    /// MOVEMENT
    /// ==========================================================================================
    """


    """
    Sets the current route via one of the closest input cells.
    Can take a set of tuples, or a tuple.
    """
    def find(self, target):

        if self.location == target:
            return
        route = pathfinding.get_route(self.location, target)

        if route == ():
            print("ERROR FIND RETURNED NO ROUTE %s to %s." % (self.location, target))
        else:
            self.route = list(route)

    def set_route(self):
        pass


    """
    Sets the current route via one of the closest input cells.
    Can take a set of tuples, or a tuple.
    
    (function specially designed for exploration - checks surrounding squares first).
    """
    def explore(self, targets):
        target = targets
        # if type(targets) is set:
            # loc_left = (self.location[0], self.location[1] - 1)
            # loc_right = (self.location[0], self.location[1] + 1)
            # loc_up = (self.location[0] - 1, self.location[1])
            # loc_down = (self.location[0] + 1, self.location[1])
            # if loc_left in targets:
            #     target = loc_left
            # elif loc_right in targets:
            #     target = loc_right
            # elif loc_up in targets:
            #     target = loc_up
            # elif loc_down in targets:
            #     target = loc_down
            # else:
            # take into account distance from stockpile location too
            # target = sorted([(pathfinding.get_euclidean_distance(self.group.stockpile_location, end2), end2) for end2 in targets],
            #                 key=lambda x: x[0])[0][1]

            # target = targets.pop()

        # target = targets.pop()

        route = pathfinding.get_route(self.location, target)
        # print("%s destination %s route %s" % (self.id_number, str(target), str(route)))

        if route == ():
            print("ERROR FIND RETURNED NO ROUTE.")
            self.unexplored_points.remove(target)
            self.explored_points.add(target)
        else:
            self.route = list(route)


    """
    Moves the player and updates it on the global world map.
    """
    def move(self, new_location):
        guiwindow.WORLD_INSTANCE.rerender_location(self.location)
        guiwindow.WORLD_INSTANCE.world[self.location[0]][self.location[1]].people_on_cell.remove(copy.copy(self.id_number))
        self.location = new_location
        if self.location in self.unexplored_points:
            self.group.all_trafficked_locations.add(self.location)
            self.unexplored_points.remove(self.location)
        guiwindow.WORLD_INSTANCE.world[self.location[0]][self.location[1]].people_on_cell.add(copy.copy(self.id_number))
        guiwindow.WORLD_INSTANCE.rerender_location(self.location)
        # register new unexplored points
        for loc in list(pathfinding.perimeter_radius(self.location, 2, 0, 0, 128, 128)):
            if guiwindow.WORLD_INSTANCE.traverse_map[loc[0]][loc[1]] != -1:
                if loc not in self.explored_points:
                    self.unexplored_points.add(loc)


    """
    If the route array has more then two it has not arrived
    """
    def arrived_at_location(self):
        return len(self.route) == 0


    """
    Moves one step closer towards destination
    """
    def step_towards_route(self):
        if not self.arrived_at_location():
            new_loc = self.route.pop(0)
            self.move(new_loc)
            self.observe_surroundings()

    """
    /// ==========================================================================================
    /// GROUPS   
    /// ==========================================================================================
    """






    """
    To change group call this function and pass in the group.
    If it is just one person in their own group, a new group will be generated
    and both members will be added to it.
    
    If group drops to one person, territory not transferred.
    If group grows from one person, territory is transferred.
    """
    def switch_group(self,target_group):

        # if no members in target group, it shouldn't exist
        # (e.g. denied entry into a group so rejoining their own)
        # then they will join their own group instead
        # if not target_group.members:
        #     target_group = self.own_group

        # just in case
        if target_group == self.group:
            return

        # this human has somehow managed to gain reference
        # to a own_group class, of which is currently empty
        # prevent them from joining this group entirely instead get them to join their own
        if target_group != self.own_group and target_group.own_group and len(target_group.members) != 1:
            target_group = self.own_group
            # print(target_group.members)
            # print("yea")
            # return

        # prevents people from attempting to join disbanded group
        if target_group != self.own_group and target_group.group_type == GroupType.SETTLEMENT and len(target_group.members) == 0:
            target_group = self.own_group


        self.needs[NEED_TYPE.TRAIN].reset_kit_change_request(self)
        self.needs[NEED_TYPE.BETTER_SLEEPING_LOCATION].set_new_sleeping_location(self, None)

        # case for first joining a group i.e. self.group will be none
        if self.group is not None:
            self.group.remove_member(self)

            """
            If current group is now 1 person, convert their group into own group            
            """
            if len(self.group.members) == 1 and\
                    self.group.group_type == GroupType.SETTLEMENT:
                # if group is now only 1 person, get that person to join his old group
                other_member = list(self.group.members)[0]

                # also transfer the items from the now empty group to the other guys group
                other_member.own_group.knowledge_group_item_inventory.transfer_items(self.group)

                # transfer knowledge of cell locations
                other_member.own_group.knowledge_cell_locations = self.group.knowledge_cell_locations
                self.group.knowledge_cell_locations = KnowledgeGroupCellLocations(self.group)
                other_member.own_group.knowledge_cell_locations.group = other_member.own_group

                other_member.needs[NEED_TYPE.TRAIN].reset_kit_change_request(other_member)
                other_member.needs[NEED_TYPE.BETTER_SLEEPING_LOCATION].set_new_sleeping_location(other_member, None)
                other_member.group.remove_member(other_member)
                other_member.own_group.add_member(other_member)
                other_member.finish_task()
                other_member.group = other_member.own_group

        new_group = target_group

        # if forming a new group
        if len(target_group.members) == 1:
            other_person = list(target_group.members)[0]
            new_group = Group(other_person.own_group.stockpile_location)
            new_group.add_member(self)
            logging.info("%s is forming a new group %s with %s" % (self.id_number, new_group.id_number, other_person.id_number))

            self.finish_task()

            # transfer our stuff to new group
            new_group.knowledge_group_item_inventory.transfer_items(other_person.own_group)

            # transfer knowledge of cell locations
            new_group.knowledge_cell_locations = other_person.own_group.knowledge_cell_locations
            other_person.own_group.knowledge_cell_locations = KnowledgeGroupCellLocations(other_person.own_group)
            new_group.knowledge_cell_locations.group = new_group

            # transfer territories
            guiwindow.WORLD_INSTANCE.transfer_territories(other_person.own_group, new_group)

            # transfer buffer factors
            new_group.buffer_factors = copy.deepcopy(other_person.own_group.buffer_factors)

            # transfer human location tracking
            new_group.average_member_locations = list(other_person.own_group.average_member_locations)
            new_group.all_trafficked_locations = set(other_person.own_group.all_trafficked_locations)

            other_person.needs[NEED_TYPE.TRAIN].reset_kit_change_request(other_person)
            other_person.needs[NEED_TYPE.BETTER_SLEEPING_LOCATION].set_new_sleeping_location(other_person, None)
            other_person.group.remove_member(other_person)
            new_group.add_member(other_person)
            other_person.finish_task()
            other_person.group = new_group
        else:
            logging.info("%s joined group %s of size %s" % (self.id_number, new_group.id_number, len(new_group.members)))

            # print(new_group.members)
            new_group.add_member(self)
            self.finish_task()

        self.group = new_group

    def die(self, damage_type):
        self.state = HumanState.DEAD
        logging.info("%s has died! (%s)" % (self.id_number, damage_type))
        #self.force_finish_task()


    def enter_incapacitated(self):
        logging.info("%s is incapacitated!" % self.id_number)
        # self.force_finish_task()
        self.state = HumanState.INCAPACITATED

    def leave_incapacitated(self):
        logging.info("%s recovered from incapacitation!" % self.id_number)
        # self.force_finish_task()
        self.state = HumanState.AWAKE


    def change_health(self, delta, change_type):
        if self.body.health.get() + delta <= 0:
            self.die(change_type)
            return

        if (self.body.health.get() < global_params.incapacitated_health) and\
                (self.body.health.get() + delta > global_params.incapacitated_health) and\
                self.state == HumanState.INCAPACITATED:
            self.leave_incapacitated()

        if (self.body.health.get() > global_params.incapacitated_health) and\
                (self.body.health.get() + delta < global_params.incapacitated_health) and\
                change_type == HEALTH_CHANGE_TYPE.FIGHT:
            self.enter_incapacitated()
        self.body.health.set(self.body.health.get() + delta)

    def change_stamina(self, delta):
        self.body.stamina.set(self.body.stamina.get() + delta)





    """
    /// ==========================================================================================
    /// STATISTICS   
    /// ==========================================================================================
    """

    def get_skill_ratio(self):
        ratios = {}
        for skill in self.skills:
            values = list(self.skills.values())
            values.remove(self.skills[skill])
            ratios.update({str(skill)+str('_ratio'):self.skills[skill]/np.array(values).mean()})
            for skill in self.skills:
                ratios.update({str(skill)+str('_hours'):0})
                ratios.update({str(skill)+str('_skill'):self.skills[skill]})

        return ratios


    def get_debug_info(self):
        out = ""

        # out += "route: %s\n" % self.route
        out += self.body.to_string()
        out += "location: %s\n" % str(self.location)
        out += "state: %s\n" % self.state
        out += "group: %s\n" % self.group.id_number
        out += "sleep_hour: %s\n" % self.sleep_hour
        out += "sleeping_loc: %s\n" % str(self.sleeping_location)
        out += "current_building: %s\n" % self.current_building
        #out += "food factor: %s\n" % self.group.buffer_factors['food']
        #out += "water factor: %s\n" % self.group.buffer_factors['water']
        return out

    """
    DO NOT DELETE THIS. PASTE THIS IN FOR EVERY NEW OBJECT THAT WILL BE STORED IN A SET/DICTIONARY.
    THIS IS ESSENTIAL FOR MAKING SURE THE PROGRAM PERFORMS EXACTLY THE SAME EVERY TIME!

    assert(false) WILL CRASH THE PROGRAM IF YOU ATTEMPT TO PUT THIS OBJECT INTO A SET/DICT WITHOUT FIRST MODIFYING THE FUNCTION.
    THIS IS DONE ON PURPOSE TO PREVENT YOU FROM ACCIDENTALLY LEAKING NON-DETERMINISM INTO THE PROGRAM.
    SPEAK TO ME (TOM) AND I WILL EXPLAIN WHAT TO DO.
    """
    # def __hash__(self):
    #     return hash(self.id_number)
    #
    # def __eq__(self, other):
    #     return self.__class__ == other.__class__ and self.id_number == other.id_number
