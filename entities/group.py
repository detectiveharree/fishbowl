import global_params
import ai.groupai.task.taskgroupgetdayssurvivalfood
import guiwindow
from items.itemresources.itemresource import ResourceType
from ai.groupai.task.taskgroupcreatecaravan import TaskGroupCreateCaravan
from ai.groupai.task.taskgroupgetdayssurvivalfood import TaskGroupGetDaySurvivalFood
from ai.groupai.task.taskgroupgetdayssurvivalwater import TaskGroupGetDaySurvivalWater
from gameworld.cell.cellbuilding.cellbuilding import BUILDING_TYPE
from gameworld.cell.cellbuilding.cellbuildinghouse import BuildingHouse
from gameworld.cell.cellbuilding.cellbuildingtavern import BuildingTavern
from gameworld.cell.cellbuilding.cellbuildingfightingarena import BuildingFightingArena
from gameworld.cell.cellbuilding.cellbuildingblacksmith import BuildingBlacksmith
from ai.humanai.relationships.information.informationlocationcell import InformationLocationCell
from ai.need import NEED_TYPE
from ai.groupai.needs.needgroup import GROUP_NEED_TYPE
from ai.groupai.needs.needgroupshelter import NeedGroupShelter
from ai.groupai.needs.needgroupcraftitems import NeedGroupCraftItems
from ai.groupai.needs.needgrouprequestitems import NeedGroupRequestItems
from ai.groupai.needs.needgroupdefence import NeedGroupDefence
from ai.groupai.bufferfactor.bufferfactorskill import BufferFactorSkillStats
from ai.groupai.knowledge.knowledgegroupcelllocations import KnowledgeGroupCellLocations
from ai.groupai.knowledge.knowledgegroupsleepinglocationstent import KnowledgeGroupSleepingLocationsTent
from ai.groupai.knowledge.knowledgegroupsleepinglocationshouse import KnowledgeGroupSleepingLocationsHouse
from ai.groupai.knowledge.knowledgegroupinventoryshelf import KnowledgeGroupInventoryShelf
from ai.groupai.knowledge.knowledgegroupterritorynodes import KnowledgeGroupTerritoryNodes
from ai.groupai.knowledge.knowledgegroupleader import KnowledgeGroupLeader
from ai.groupai.knowledge.knowledgegrouphumanopinions import KnowledgeGroupHumanOpinions
from ai.groupai.knowledge.knowledgegroupgroupopinions import KnowledgeGroupGroupOpinions
from ai.groupai.task.caravan.taskgroupcaravanswitchgroup import TaskGroupCaravanSwitchGroup
import ai.pathfindingbuilding
from entities.groupbase import GroupBase, GROUP_BUFFER_FACTOR
from gameworld.timestamp import TimeStamp
from ai import pathfinding
from copy import deepcopy, copy
from functools import reduce
from entities.groupbase import GroupType
import operator
from humanbase import HumanState
import logging
from collections import Counter

"""
At start of day, distribute stockpile contents to each task based on its demand up to the amount it needs
IF task complete, add contents to stockpile content
For each action/task have some kind of reset plug at start of day

People can only eat/drink from Survival Task Inventory

"""

class Group(GroupBase):



    def __init__(self, location, stockpile_contents = { resource_type:0 for resource_type in list(ResourceType)}, group_type=GroupType.SETTLEMENT, parent_group=None):
        super().__init__(guiwindow.WORLD_INSTANCE.group_id_counter, group_type, stockpile_contents, stockpile_location=location, parent_group=parent_group) # ALWAYS CALL PARENT CONSTRUCTOR
        # incriment group id whenever created
        guiwindow.WORLD_INSTANCE.group_id_counter += 1

        self.colour = global_params.group_colour_palette[guiwindow.WORLD_INSTANCE.group_id_counter % len(global_params.group_colour_palette)]


        # knowledge
        self.knowledge_cell_locations = KnowledgeGroupCellLocations(self)
        self.knowledge_sleeping_location_tents = KnowledgeGroupSleepingLocationsTent()
        self.knowledge_sleeping_location_house = KnowledgeGroupSleepingLocationsHouse()
        self.knowledge_group_item_inventory = KnowledgeGroupInventoryShelf(self)
        self.knowledge_group_territory_nodes = KnowledgeGroupTerritoryNodes(self)
        self.human_opinions = KnowledgeGroupHumanOpinions(self)
        self.group_opinions = KnowledgeGroupGroupOpinions(self)
        self.knowledge_group_leader = KnowledgeGroupLeader(self, self.human_opinions)

        self.possible_sleeping_location_types = [self.knowledge_sleeping_location_house, self.knowledge_sleeping_location_tents]

        # buffer factors

        self.buffer_factor_water = self.buffer_factors[GROUP_BUFFER_FACTOR.WATER_HARVESTING]
        self.buffer_factor_food = self.buffer_factors[GROUP_BUFFER_FACTOR.FOOD_HARVESTING]


        # needs
        self.needs = {}
        self.register_need(NeedGroupShelter())
        self.register_need(NeedGroupCraftItems())
        self.register_need(NeedGroupRequestItems())
        self.register_need(NeedGroupDefence())
        self.need_crafting = self.needs[GROUP_NEED_TYPE.CRAFTING]
        self.need_defence = self.needs[GROUP_NEED_TYPE.DEFENCE]
        self.need_request_item = self.needs[GROUP_NEED_TYPE.RESOURCE_REQUESTING]

        # stockpile
        self.all_trafficked_locations = set()
        self.current_expansion_level = 1

        # stockpile location
        self.average_member_locations = []



        #tasks
        self.task_survival_food = TaskGroupGetDaySurvivalFood(self, GROUP_NEED_TYPE.SURVIVAL, 10000)
        self.task_survival_water = TaskGroupGetDaySurvivalWater(self, GROUP_NEED_TYPE.SURVIVAL, 10000 * global_params.food_water_ratio)
        self.tasks = []
        if GroupType == GroupType.SETTLEMENT:
            self.tasks = [self.task_survival_food, self.task_survival_water]


        self.new_tasks = []
        self.daily_schedule = None
        self.collection_stats = {skill_type: BufferFactorSkillStats(skill_type) for skill_type in list(GROUP_BUFFER_FACTOR)}
        self.current_tasks_satisfaction = {skill_type: 0 for skill_type in list(GROUP_BUFFER_FACTOR)}
        self.buffer_factor_update = False
        self.start_hour_work_day = 8
        # THIS +2 OFFSET IS BEACUSE WE START THE WORLD AT 8AM
        # (NEED A BUFFER TO INIT SOME STUFF OTHERWISE FIRST DAY WON'T TASK ALLOC WHICH IS ANNOYING)
        # GET RID OF THIS BEFORE RELEASE
        self.start_time_in_ticks = (self.start_hour_work_day * global_params.hourly_ticks) + 2
        self.amount_hours_work_day = 9
        self.total_hours_float_allocation = 0
        self.leader_id = None # in practise will never be NONE

        # territory

        self.campaign = None

        # building
        self.invalid_building_placements = {building_type: set() for building_type in list(BUILDING_TYPE)}

        # debug
        self.own_group = False


    """
    Registers a threat 
    """
    def register_threat(self, human, other_human):
        # if other person on army
        if other_human.group.campaign is not None:
            # if not already registered
            if not self.need_defence.have_registered_threat(other_human.group.campaign):
                # if army enemy is our group
                if other_human.group.campaign.get_enemy_group_id() == self.id_number:
                    human.needs[NEED_TYPE.SIGNAL_GROUP].begin_signal(other_human.group.campaign)



    def test_city(self):
        for i in range(0, 1, 1):
            house = BuildingFightingArena(ai.pathfindingbuilding.place_building(BUILDING_TYPE.FIGHTINGARENA, self))
            house.register_to_world()


        for f in range(0, 1, 1):
            tavern = BuildingTavern(ai.pathfindingbuilding.place_building(BUILDING_TYPE.TAVERN, self))
            tavern.register_to_world()

        for f in range(0, 1, 1):
            tavern = BuildingBlacksmith(ai.pathfindingbuilding.place_building(BUILDING_TYPE.BLACKSMITH, self))
            tavern.register_to_world()

        for f in range(0, 1, 1):
            tavern = BuildingHouse(ai.pathfindingbuilding.place_building(BUILDING_TYPE.HOUSE, self))
            tavern.register_to_world()

        # ai.pathfindingbuilding.place_n_farms(self.stockpile_location, 100, max_blob_size=15, max_blob_length=5)


    def register_need(self, need):
        self.needs[need.need_type] = need


    """
    Called when a group is disabled, i.e. when the members drop to zero.
    Do necessary clean up to remove the group from the world.
    """
    def disable(self):

        # this iniating this call back is necessary because otherwise
        # the new rally point group might not have it's task set.
        for task in self.tasks:
            if (type(task) is TaskGroupCreateCaravan):
                task.finish_task(None)

        logging.info("Group %s has disbanded" % self.id_number)
        guiwindow.WORLD_INSTANCE.world[self.stockpile_location[0]][
            self.stockpile_location[1]].group_center = None
        guiwindow.WORLD_INSTANCE.rerender_location(self.stockpile_location)
        self.all_trafficked_locations.clear()
        self.average_member_locations.clear()
        self.knowledge_group_territory_nodes.lose_all_territory()

        for bf in self.buffer_factors.values():
            bf.value = bf.default_value


    def should_disable(self):
        return len(self.members) == 0


    def enable(self):
        if len(self.members) == 1:
            logging.info("Group %s has begun as a %s" % (self.id_number, self.group_type))
            logging.info(self.tasks)
            logging.info(self.new_tasks)
            # set the stockpile location to wherever the person who forms the group is located
            self.set_stockpile_location(list(self.members)[0].location)
            self.knowledge_group_territory_nodes.daily_update_territories()


    def tickly_update(self):
        self.check_tasks_require_update()




    def hourly_update(self):



        # hourly update of member locations array
        # if self.group_type == GroupType.SETTLEMENT:
        #     for member in self.members:
        #         if member.current_task is not None:
        #             pass
        #             # only record if they are doing a task related to group
        #             if isinstance(member.current_action, ActionInteractCell):
        #                 self.average_member_locations.append(member.location)

        """
        At 8am, task allocation begins
        """
        if guiwindow.WORLD_INSTANCE.time_hour == self.start_hour_work_day:
            # print(self.knowledge_cell_locations.cells)


            for human in self.members:
                for (loc, cellbase) in self.knowledge_cell_locations.location_to_cell.items():
                    if not human.knowledge_cell_locations.is_same_cell_type(loc, cellbase):
                        cellbase = deepcopy(cellbase)
                        """
                        IF first time telling a person about it, give them a memory of it without any occupants on it
                        """
                        cellbase.reset_interactable_locations()
                        InformationLocationCell({loc}, cellbase).register_to_knowledge(human)


            if self.group_type == GroupType.SETTLEMENT:
                # Deposit extra cell and get collection statistics
                if not self.tasks:
                    self.add_task(self.task_survival_food)
                    self.add_task(self.task_survival_water)
                if self.task_survival_food in self.tasks or self.task_survival_water in self.tasks:
                    self.set_stockpile_location(self.get_new_stockpile_location())
                self.knowledge_group_territory_nodes.daily_update_territories()

        # if guiwindow.WORLD_INSTANCE.time_hour == (8 + global_params.human_work_hours_per_day):





    def modify_buffer_factor(self, skill, achieved, required):
        self.collection_stats[skill].amount_achieved += achieved
        self.collection_stats[skill].amount_required += required
        self.buffer_factor_update = True

    def calculate_buffer_factors_if_required(self):
        if self.buffer_factor_update:

            """
            We'll have no collection statistics on the first day
            """

            for stat in self.collection_stats.keys():
                self.buffer_factors[stat].daily_update(self.collection_stats[stat].amount_required,
                                                       self.collection_stats[stat].amount_achieved,
                                                       self.total_hours_float_allocation)

            self.buffer_factor_update = False
            self.collection_stats = {skill_type: BufferFactorSkillStats(skill_type) for skill_type in list(GROUP_BUFFER_FACTOR)}

    def check_tasks_require_update(self):

        """
        Reset daily worker schedule
        """
        if self.start_time_in_ticks == guiwindow.WORLD_INSTANCE.time_ticks:
            # reset daily schedule
            self.daily_schedule = self.generate_daily_schedule()


        hourly_allocated_actions = {}
        other_actions = {}
        tasks_modified = False

        for new_task in self.new_tasks:
            if new_task.should_be_only_group_task():
                for task in self.tasks:
                    # task.task_finish_callback(self)
                    task.terminate_task_early(self)
                    task.finish_task(self)
                    task.deactivate(self)
                self.tasks.clear()
            self.tasks.append(new_task)
            tasks_modified = True
        self.new_tasks.clear()


        def register_actions_to_execute(task, actions):
            nonlocal other_actions, hourly_allocated_actions
            for action in actions:
                """
                Basically just split the new actions into
                those that require hourly allocation
                and those that do not
                """
                if action.requires_hourly_task_allocation_algo():
                    if task not in hourly_allocated_actions:
                        hourly_allocated_actions[task] = []
                    hourly_allocated_actions[task].append(action)
                else:
                    if task not in other_actions:
                        other_actions[task] = []
                    other_actions[task].append(action)

        """
        Tick tasks and check if they are complete
        """

        for task in self.tasks:
            if task.tick_when(self):
                # see if tasks have any new actions
                new_actions = task.tick(self)
                register_actions_to_execute(task, new_actions)

            # finish task check
            if task.is_task_complete(self):
                if task.should_deplete_need_on_task_completion():
                    self.needs[task.need_type].need_level -= task.need_level
                # task.task_finish_callback(self)
                task.finish_task(self)
                task.deactivate(self)
                tasks_modified = True

        self.calculate_buffer_factors_if_required()

        # removes tasks if they are complete
        self.tasks[:] = [task for task in self.tasks if not task.is_task_complete(self)]


        """
        If any tasks are finished then recalculate task satisfaction level
        """
        if tasks_modified:
            self.current_tasks_satisfaction = self.get_current_tasks_demand_satisfaction()

        """
        Check needs to see if any new tasks are generated
        """

        for need in self.needs.values():
            # Calculate adjusted need level taking into account current tasks
            adjusted_need_level = need.need_level
            if need.need_type in self.current_tasks_satisfaction.keys():
                adjusted_need_level -= self.current_tasks_satisfaction[need.need_type]
            # Get the new tasks
            new_tasks = need.get_task(self, adjusted_need_level)
            self.tasks += new_tasks
            if new_tasks:
                tasks_modified = True

        """
        If any tasks are added then recalculate task satisfaction level
        """
        if tasks_modified:
            self.current_tasks_satisfaction = self.get_current_tasks_demand_satisfaction()



        """
        Check if a task that should be activated is currently not activated or vice versa
        """
        for task in self.tasks:
            task_should_be_activated = task.activate_when(self)
            if task_should_be_activated:
                task.activate(self)
                register_actions_to_execute(task, task.current_actions)
                #self.calculate_buffer_factors_if_required()


        """
        Allocate actions
        """
        self.allocate_actions(other_actions)
        self.allocate_hourly_actions(hourly_allocated_actions)


    def add_task(self, new_task):
        self.new_tasks.append(new_task)




    def amount_hours_left_work_day(self):
        return self.start_hour_work_day + self.amount_hours_work_day - TimeStamp().hour


    def generate_daily_schedule(self):
        """
        Stores ratios of available workers
        """
        worker_schedule = {}
        for human in self.members:
            worker_schedule[human] = human.get_skill_ratio()
            worker_schedule[human]["free_hours"] = self.amount_hours_left_work_day()
            human.needs[NEED_TYPE.GROUP_TASK].new_allocation = True
        return worker_schedule

    def get_total_free_hours_from_daily_schedule(self):
        free_hours = 0
        for human in self.daily_schedule.keys():
            free_hours += self.daily_schedule[human]["free_hours"]
        return free_hours


    def allocate_actions(self, other_actions):
        for task in other_actions:
            for action in other_actions[task]:
                action.excluded_people_from_task_allocation_algo(self)
                action.activate(None, self.daily_schedule, self)


                                        #  {task : [actions]}
    def allocate_hourly_actions(self, task_hourly_actions_list):

        if not task_hourly_actions_list:
            return

        """
        Helper function scales the demands
        """
        def calculate_daily_scaled_demand(dict, freehours):

            # sum total demand between all actions and their tasks
            total_demand = sum([sum(dict[task].values()) for task in dict.keys()])
            new_dict = {}
            for task in dict.keys():
                new_dict[task] = {action: dict[task][action] * (freehours / total_demand) for action in
                                  dict[task].keys()}
            return new_dict

        """
        action_hour_costs is a map of tasks to their current actions which are mapped to a hour
        i.e. [task : [action1 : 1000, action2 : 2000]]
        task_demands is the current action in the task BUT the demand for it's complete task
        """
        task_actions_hour_costs = {}
        task_demands = {}
        task_action_hours = {} # {task : {action : hours}}

        for (task, actions) in task_hourly_actions_list.items():
            task_actions_hour_costs[task] = {}
            task_demands[task] = {}
            task_action_hours[task] = {}
            total_task_demand = task.need_level

            demand_per_action = int(total_task_demand / len(actions))

            for action in actions:
                task_actions_hour_costs[task][action] = action.estimated_hours(self)
                task_demands[task][action] = demand_per_action

        total_free_hours = self.get_total_free_hours_from_daily_schedule()

        if total_free_hours <= 0.9:
            return
        demand_daily_scaled = calculate_daily_scaled_demand(task_demands, total_free_hours) # {task : {action : scaled_demand}}

        """
        Makes sure demand (or hours at this point) is not over allocated. 
        """
        while True:
            # over_allocations = True
            over_allocations = False
            for task in demand_daily_scaled.keys():

                terminate_loop = False
                for action in demand_daily_scaled[task].keys():
                    if demand_daily_scaled[task][action] >= task_actions_hour_costs[task][action]:
                        task_action_hours[task].update({action: task_actions_hour_costs[task][action]})
                        total_free_hours -= task_actions_hour_costs[task][action]
                        del demand_daily_scaled[task][action]
                        if demand_daily_scaled[task] == {}:
                            del demand_daily_scaled[task]
                        demand_daily_scaled = calculate_daily_scaled_demand(demand_daily_scaled, total_free_hours)
                        terminate_loop = True
                        break
                    # over_allocations = False
                if terminate_loop:
                    over_allocations = True
                    break
            if not over_allocations or len(demand_daily_scaled) == 0:
                break

        """
        Adds remaining non over allocated demands
        """
        for item in demand_daily_scaled.keys():
            task_action_hours[item].update(demand_daily_scaled[item])

        """
        Activate actions
        """
        for task in task_action_hours:
            for action in task_action_hours[task]:
                hours = task_action_hours[task][action]
                action.activate(hours, self.daily_schedule, self)


        """
        Stat collection
        NOTE THIS DOES NOT TAKE INTO ACCOUNT 
        THAT PEOPLE CAN BE ALLOCATED NON HOURED TASKS
        """

        # self.total_hours_float_allocation = ((self.amount_hours_work_day * len(members)) -\
        #                                     self.get_total_free_hours_from_daily_schedule()) /\
        #                                     self.amount_hours_work_day * len(members)




    def get_current_tasks_demand_satisfaction(self):
        demands_in_progress = {}
        for task in self.tasks:
            if task.need_type not in demands_in_progress.keys():
                demands_in_progress[task.need_type] = task.need_level
                continue
            demands_in_progress[task.need_type] += task.need_level
        return demands_in_progress



    """
    Should only need to be called when a new person enters a group
    """
    def daily_update(self):
        self.human_opinions.update_opinions()
        self.group_opinions.update_opinions()


    """
    Initiates caravan and sequence of actions required for person to try join 
    a different group
    """
    def attempt_switch_group(self, human, other_group):
        human.state = HumanState.AWAKE
        human.force_finish_task()
        # note group location below is temp: just a meeting point of inital caravan
        """
        Find inital meetup point at edge of our territory
        """
        meet_up_point = pathfinding.get_first_location_given(human.location, other_group.stockpile_location,
                                                                  lambda worldcell : worldcell.territory != self.id_number)

        caravan_group = Group(meet_up_point, group_type=GroupType.RALLY_POINT, parent_group=self)
        switch_group_task = TaskGroupCaravanSwitchGroup(caravan_group, other_group, other_group.stockpile_location)
        self.add_task(TaskGroupCreateCaravan(self, caravan_group, {human}, lambda : caravan_group.add_task(switch_group_task)))

    """
    Returns true/False to indicate if person is allowed to join a group.
    """
    def request_permission_to_join(self, other_group):

        # if not self.members:
        #     logging.info("Attempted to join a empty group")
        #     return False

        return True
        # join instantly if no members (shouldn't really ever be called)
        if not self.members:
            return True
        all_this_skills = reduce(operator.concat, [list(member.skills.values()) for member in self.members])
        avg_this = sum(all_this_skills) / len(all_this_skills)

        all_their_skills = reduce(operator.concat, [list(member.skills.values()) for member in other_group.members])
        avg_their = sum(all_their_skills) / len(all_their_skills)

        # only let them join if their average skills are better then ours
        return avg_their > avg_this



    def set_stockpile_location(self, location):

        old_location = self.stockpile_location
        # update worlds stockpile location
        guiwindow.WORLD_INSTANCE.world[self.stockpile_location[0]][
            self.stockpile_location[1]].group_center = None
        guiwindow.WORLD_INSTANCE.rerender_location(self.stockpile_location)
        self.stockpile_location = location

        # update worlds stockpile location
        guiwindow.WORLD_INSTANCE.world[self.stockpile_location[0]][
            self.stockpile_location[1]].group_center = self.id_number
        guiwindow.WORLD_INSTANCE.rerender_location(self.stockpile_location)
        """
        If stockpile location changes, wipe all the sleeping locations
        """
        if old_location != self.stockpile_location:
            self.update_sleeper_locations()
            self.knowledge_group_territory_nodes.update_stockpile_territory()


    """
    Disbands this group kicking everyone off into their own groups
    """
    def disband_group(self):
        logging.info("%s has disbanded" % self.id_number)
        members = copy(self.members)

        for member in members:
            member.switch_group(member.own_group)

    """
    Called when person joins group
    """
    def add_member(self, human):

        self.members.add(human)
        self.member_ids.add(human.id_number)

        if self not in guiwindow.WORLD_INSTANCE.groups.keys():
            guiwindow.WORLD_INSTANCE.groups[self.id_number] = self
            self.enable()


        """
        This will make it so the person will now know of a person but not 
        necessarily know any details about them. Purely done for convienence. 
        """
        for member in self.members:
            if member.id_number != human.id_number:
                human.knowledge_of_people.register_knowledge_of_person(member.id_number)
            member.knowledge_of_people.register_knowledge_of_person(human.id_number)
        """
        Temp
        """
        # if len(self.members) == 5 and self.group_type == GroupType.SETTLEMENT:
            #self.test_city()
        self.update_sleeper_locations()
        self.knowledge_group_leader.member_added(human)


    """
    Called when person leaves group
    """
    def remove_member(self, human):
        self.members.remove(human)
        self.member_ids.remove(human.id_number)

        # put his uncollected contents in group shared inventory
        for item in self.knowledge_group_item_inventory.remove_all_items_from_collection(human.id_number):
            item.add_item_to_shelf(self)
        if human.sleeping_location is not None:
            human.needs[NEED_TYPE.BETTER_SLEEPING_LOCATION].set_new_sleeping_location(human, None)
        self.update_sleeper_locations()
        self.knowledge_group_leader.member_removed(human)


    """
    Updates groups sleeping locations
    """
    def update_sleeper_locations(self):

        if len(self.members) == 0:
            return

        self.current_expansion_level = pathfinding.find_minimum_expansion_function_size(pathfinding.flood_fill_radius,
                                                                                        self.stockpile_location,
                                                                                        self.current_expansion_level,
                                                                                        len(self.members))

        self.knowledge_sleeping_location_tents.register_group_sleeping_locations(
            pathfinding.sort_by_closest(self.stockpile_location,
                                        pathfinding.flood_fill_radius(
                                                                   self.stockpile_location,
                                                                   self.current_expansion_level)))



    def acceptable_stockpile_location(self, loc):
        other_group_claim = guiwindow.WORLD_INSTANCE.world[loc[0]][loc[1]].territory
        return other_group_claim is None or other_group_claim == self.id_number


    def can_place_stockpile(self, loc):

        # centre = guiwindow.WORLD_INSTANCE.world[loc[0]][loc[1]].territory
        # if centre != self.id_number:
        #     return False



        if not guiwindow.WORLD_INSTANCE.world[loc[0]][loc[1]].can_place_stockpile():
            return False

        if not self.acceptable_stockpile_location(loc):
            return False

        required_expansion_level = pathfinding.find_minimum_expansion_function_size(pathfinding.flood_fill_radius, loc,
                                                                                        self.current_expansion_level,
                                                                                        len(self.members)) + self.knowledge_group_territory_nodes.stockpile_territory_buffer
        for coord in pathfinding.flood_fill_radius(loc, required_expansion_level):
            if not self.acceptable_stockpile_location(coord):
                return False
        return True



    def get_new_stockpile_location(self):
        if len(self.average_member_locations) == 0:
            return self.stockpile_location
        mean_x = int(round(sum(x for y, x in self.average_member_locations)/len(self.average_member_locations),0))
        mean_y = int(round(sum(y for y, x in self.average_member_locations)/len(self.average_member_locations),0))
        self.average_member_locations.clear()

        min_locs = sorted([(pathfinding.get_euclidean_distance((y1, x1), (mean_y, mean_x)), (y1, x1)) for y1, x1 in self.all_trafficked_locations], key=lambda x: x[0])
        """
        Make sure that we can place stock pile in proposed position. 
        """
        for closest_loc in min_locs:
            distance = closest_loc[0]
            new_loc = closest_loc[1]
            # if can place base there i.e. is not water
            # if can claim territory
            if self.can_place_stockpile(new_loc):
                # if best is a small jump its not worth moving
                if distance < global_params.minimum_stockpile_move_distance:
                    break
                return new_loc
        return self.stockpile_location


    def format_task_info_debug(self):
        text = ""
        text += "type: %s\n" % self.group_type
        for i in range(len(self.tasks)):
            task = self.tasks[i]
            text += "(%s/%s) Task: %s \n" % (i + 1, len(self.tasks), task)
            text += "Active: %s \n" % (task.is_activated)
            text += "Content: %s \n" % (task.contents)
            text += "Current Actions (%s left):\n" % (len(task.current_actions))
            for action in task.current_actions:
                text += action.get_stats(self) + " \n"
        return text

    def format_task_info(self):
        text = ""
        for i in range(len(self.tasks)):
            task = self.tasks[i]
            text += "(%s/%s) Task: %s \n" % (i + 1, len(self.tasks), task)
            text += "Active: %s \n" % (task.is_activated)
            text += "%s actions left:\n" % (len(task.current_actions))
        return text

    def workout_total_resources(self):
        result = dict(self.stockpile_contents)
        for task in self.tasks:
            for key in task.contents.keys():
                result[key] += task.contents[key].storage
        return result

    def __repr__(self):
        return "Group %s" % self.id_number


    def get_buffer_factor_info(self):
        out = ""
        out += "buffer factors: %s\n" % self.buffer_factors
        out += "total buffer factors: %s\n" % sum([bf.value for bf in self.buffer_factors.values()])
        out += "hours used: %s%%\n" % (self.total_hours_float_allocation * 100)
        return out

    def get_debug_info(self):
        out = ""
        out += "location: %s\n" % str(self.stockpile_location)
        out += "type: %s\n" % self.group_type
        out += "members: %s\n" % len(self.members)
        out += "%s" % len(self.knowledge_group_leader.to_string(3))
        out += "tent spots taken: %s/%s\n" % (self.knowledge_sleeping_location_tents.amount_taken_spaces(), len(self.knowledge_sleeping_location_tents.sleeping_location_to_person.keys()))
        out += "house spots taken: %s/%s\n" % (self.knowledge_sleeping_location_house.count_house_spots_taken(),
                                               self.knowledge_sleeping_location_house.total_spots_available())
        out += "needs: %s\n" % self.needs
        return out

    """
    DO NOT DELETE THIS. PASTE THIS IN FOR EVERY NEW OBJECT THAT WILL BE STORED IN A SET/DICTIONARY.
    THIS IS ESSENTIAL FOR MAKING SURE THE PROGRAM PERFORMS EXACTLY THE SAME EVERY TIME!

    assert(false) WILL CRASH THE PROGRAM IF YOU ATTEMPT TO PUT THIS OBJECT INTO A SET/DICT WITHOUT FIRST MODIFYING THE FUNCTION.
    THIS IS DONE ON PURPOSE TO PREVENT YOU FROM ACCIDENTALLY LEAKING NON-DETERMINISM INTO THE PROGRAM.
    SPEAK TO ME (TOM) AND I WILL EXPLAIN WHAT TO DO.
    """
    def __hash__(self):
        return hash(self.id_number)

    def __eq__(self, other):
        return self.__class__ == other.__class__ and self.id_number == other.id_number




