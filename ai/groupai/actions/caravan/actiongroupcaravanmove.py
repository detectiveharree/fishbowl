from ai.groupai.actions.actiongroup import ActionGroup
from ai.humanai.task.taskjoingroup import TaskJoinGroup
from ai.humanai.task.taskmovewithcaravan import TaskMoveWithCaravan
from ai.humanai.task.taskassignedtask import TaskAssignedTask
import math
from ai.need import NEED_TYPE
from ai import pathfinding
from ai.groupai.actions.caravan.actiongroupcaravan import ActionGroupCaravan

"""
Moves an entire group along a specific path
"""
class ActionGroupCaravanMove(ActionGroupCaravan):

    def __init__(self, parent_task, move_stockpile, group, destination, start_location = None):
        super().__init__(parent_task) # ALWAYS CALL PARENT CONSTRUCTOR
        self.move_stockpile = move_stockpile
        self.group = group
        self.destination = destination
        self.route_counter = 1
        self.timer = 0
        self.move = False
        self.expansion_size = 1
        self.route_left = []
        self.original_route_size = 0
        self.current_loc = start_location
        self.people_arrived = set()
        self.marching_speed = 4



    def assign_formation(self):

        formation_shape = pathfinding.flood_fill_radius

        self.expansion_size = pathfinding.find_minimum_expansion_function_size(formation_shape,
                                                                               self.current_loc,
                                                                               self.expansion_size,
                                                                               len(self.group.members))

        locations = list(formation_shape(self.current_loc, self.expansion_size))
        members = list(self.group.members)
        for i in range(len(members)):
            members[i].expected_caravan_location = locations[i]


    """
    Should give the workers there tasks.
    """
    def activate(self, hours_left, available_people, group):

        self.current_loc = group.stockpile_location if self.current_loc is None else self.current_loc

        self.route_left = list(pathfinding.get_route(self.current_loc, self.destination))
        self.original_route_size = len(self.route_left)
        self.assign_formation()
        for worker in list(group.members):
            worker.needs[NEED_TYPE.GROUP_TASK].set_daily_task(worker, TaskMoveWithCaravan(worker, self), 10000)


    """
    Returns true/false to indicate whether the action is complete or not.
    Called every tick before tick() is executed.    
    """

    def is_complete(self, group):
        # print(self.route_left)
        # print(self.people_arrived)
        # print([member.id_number for member in group.members])
        return not self.route_left and len(self.people_arrived) >= len(group.members)


    """
    Called every tick while the action has begun and not completed yet.
    Returns True/False to indicate if an error occurs.
    """
    def tick(self, group):
        if self.timer == 0:
            self.move = False

        self.timer += 1
        # if self.timer == len(self.group.members):


        if self.timer >= self.marching_speed:

            if not self.route_left:
                self.assign_formation()
                for worker in list(group.members):
                    if not isinstance(worker.current_task, TaskMoveWithCaravan):
                        worker.needs[NEED_TYPE.GROUP_TASK].set_daily_task(worker, TaskMoveWithCaravan(worker, self), 10000)
                return True
            self.people_arrived.clear()
            self.current_loc = self.route_left.pop(0)
            self.group.average_member_locations.clear()
            if self.move_stockpile:
                self.group.set_stockpile_location(self.current_loc)
            self.assign_formation()
            self.route_counter += 1
            self.move = True
            self.timer = 0

        return True


    """
    Optional, gives tickly debug information.
    """
    def get_stats(self, group):
        return "move caravan (%s/%s)" % (self.route_counter, self.original_route_size)

    def __str__(self):
        return "Move caravan (%s): (%s/%s)" % (self.group.id_number, self.route_counter, self.original_route_size)
