import guiwindow
from ai.pathfinding import get_adjacent, get_euclidean_distance, Result
from global_params import UNCLAIMED_TERRITORY_FLAG

import math
from sortedcontainers import SortedSet

"""
Proposes a route for territory corridors
Will pass through existing territory and unclaimed
"""
def get_corridor_territory_route(start, end, passable_groups):
    # print("In " + str(len(ends)))
    IMPASSABLE_CONST = -1
    # print("START %s END %s" % (str(start), str(end)))

    allowed_group_corridors = set()
    for group_id in passable_groups:
        allowed_group_corridors.add(group_id + 10000)


    # producing a new array (same size as world_map) to keep track of "costs" between nodes
    cost_map = guiwindow.WORLD_INSTANCE.territory_map.copy()



    """
    Optimisation: Remove end points that we know are impassable.
    """
    cell = guiwindow.WORLD_INSTANCE.world[end[0]][end[1]]
    if not cell.is_explorable():
        return tuple()

    # if not (cost_map[start[0]][start[1]] in allowed_group_corridors or cost_map[end[0]][end[1]] in allowed_group_corridors):
    #     return tuple()

    """
    Optimisation
    When a end point is discovered, we create a CandidateRoute.
    We then attempt to find home from this new end point, before fully expanding the map as an optimisation.

    This class is used to store the information between the expansions. E.g. path so far, current x and y pos etc.
    """

    class CandidateRoute():

        """
        DO NOT DELETE THIS. PASTE THIS IN FOR EVERY NEW OBJECT THAT WILL BE STORED IN A SET/DICTIONARY.
        THIS IS ESSENTIAL FOR MAKING SURE THE PROGRAM PERFORMS EXACTLY THE SAME EVERY TIME!

        assert(false) WILL CRASH THE PROGRAM IF YOU ATTEMPT TO PUT THIS OBJECT INTO A SET/DICT WITHOUT FIRST MODIFYING THE FUNCTION.
        THIS IS DONE ON PURPOSE TO PREVENT YOU FROM ACCIDENTALLY LEAKING NON-DETERMINISM INTO THE PROGRAM.
        SPEAK TO ME (TOM) AND I WILL EXPLAIN WHAT TO DO.
        """

        def __hash__(self):
            assert (False)

        def __init__(self, end):
            # current coords of lowest cost neighbour
            self.y = end[0]
            self.x = end[1]
            self.end = end  # the inital end point from the ends array

            # upgrade this to map for order and fast lookup instead of two different lists
            self.path_out = [end]
            self.path_out_set = set()
            self.path_out_set.add(end)

    class HeuristicLOCATION():
        def __init__(self, location, cost, end):
            # current coords of lowest cost neighbour
            self.location = location
            self.cost = cost

            self.distance = get_euclidean_distance(location, end)

        def __hash__(self):
            return hash(self.location)

        def __lt__(self, other):
            return other.distance < self.distance

        def __eq__(self, other):
            return self.location == other.location

    perimeter_coords = SortedSet()
    perimeter_coords.add(HeuristicLOCATION(start, 0, end))

    while len(perimeter_coords) != 0:
        """
        If no end points left to reach, and no end points still being considered terminate.
        """

        heuristic_location = perimeter_coords.pop()

        loc = heuristic_location.location
        cost_map[loc[0]][loc[1]] = heuristic_location.cost
        # continue expanding if we own the territory or its free
        if cost_map[loc[0] - 1][loc[1]] == UNCLAIMED_TERRITORY_FLAG or cost_map[loc[0] - 1][loc[1]] in allowed_group_corridors:
            perimeter_coords.add(HeuristicLOCATION((loc[0] - 1, loc[1]), heuristic_location.cost + 1, end))

        # print("%s,%s    %s" % (loc[0], loc[1] + 1, cost_map.shape))

        if cost_map[loc[0]][loc[1] + 1] == UNCLAIMED_TERRITORY_FLAG or cost_map[loc[0]][loc[1] + 1] in allowed_group_corridors:
            perimeter_coords.add(HeuristicLOCATION((loc[0], loc[1] + 1), heuristic_location.cost + 1, end))

        if cost_map[loc[0]][loc[1] - 1] == UNCLAIMED_TERRITORY_FLAG or cost_map[loc[0]][loc[1] - 1] in allowed_group_corridors:
            perimeter_coords.add(HeuristicLOCATION((loc[0], loc[1] - 1), heuristic_location.cost + 1, end))

        if cost_map[loc[0] + 1][loc[1]] == UNCLAIMED_TERRITORY_FLAG or cost_map[loc[0] + 1][loc[1]] in allowed_group_corridors:
            perimeter_coords.add(HeuristicLOCATION((loc[0] + 1, loc[1]), heuristic_location.cost + 1, end))

        if loc == end:
            test_loc = CandidateRoute(loc)
            while True:
                results = SortedSet()


                """
                Finds minimum cost path
                We check to see if the tile in question:
                cost != IMPASSABLE_COST : tile is passable

                cost < 1000 : tile is not free const, therefore we have assigned it a value i.e. it has been checked
                OR
                cost in allowed_group_corridors : we can pass through any of these groups

                """
                if (test_loc.y - 1, test_loc.x) not in test_loc.path_out_set:
                    if test_loc.y - 1 >= 0:
                        cost = cost_map[test_loc.y - 1][test_loc.x]
                        if cost != IMPASSABLE_CONST and (cost < UNCLAIMED_TERRITORY_FLAG or cost in allowed_group_corridors):
                            results.add(Result((test_loc.y - 1, test_loc.x), cost))

                if (test_loc.y + 1, test_loc.x) not in test_loc.path_out_set:
                    if test_loc.y + 1 < len(guiwindow.WORLD_INSTANCE.world):
                        cost = cost_map[test_loc.y + 1][test_loc.x]
                        if cost != IMPASSABLE_CONST and (cost < UNCLAIMED_TERRITORY_FLAG or cost in allowed_group_corridors):
                            results.add(Result((test_loc.y + 1, test_loc.x), cost))

                if (test_loc.y, test_loc.x - 1) not in test_loc.path_out_set:
                    if test_loc.x - 1 >= 0:
                        cost = cost_map[test_loc.y][test_loc.x - 1]
                        if cost != IMPASSABLE_CONST and (cost < UNCLAIMED_TERRITORY_FLAG or cost in allowed_group_corridors):
                            results.add(Result((test_loc.y, test_loc.x - 1), cost))

                if (test_loc.y, test_loc.x + 1) not in test_loc.path_out_set:

                    if test_loc.x + 1 < len(guiwindow.WORLD_INSTANCE.world[0]):

                        cost = cost_map[test_loc.y][test_loc.x + 1]
                        if cost != IMPASSABLE_CONST and (cost < UNCLAIMED_TERRITORY_FLAG or cost in allowed_group_corridors):
                            results.add(Result((test_loc.y, test_loc.x + 1), cost))

                """
                If no locations possible at this time, break and incriment no move counter
                """
                if len(results) == 0:
                    return tuple()

                """
                If start point in potential locations, we are finished
                """

                if Result(start, 0) in results:
                    test_loc.path_out.reverse()
                    return tuple(test_loc.path_out)

                """
                Registers lowest cost location.
                """

                best_result = results.pop()

                test_loc.y = best_result.location[0]
                test_loc.x = best_result.location[1]
                test_loc.path_out.append((test_loc.y, test_loc.x))
                test_loc.path_out_set.add((test_loc.y, test_loc.x))
    return tuple()




"""
Gets route within a territory.
"""
def get_territory_route(start, end, group):
    # print("In " + str(len(ends)))
    IMPASSABLE_CONST = -1
    our_group_id = group.id_number + 10000

    # producing a new array (same size as world_map) to keep track of "costs" between nodes
    cost_map = guiwindow.WORLD_INSTANCE.territory_map.copy()

    """
    Optimisation: Remove end points that we know are impassable.
    """
    cell = guiwindow.WORLD_INSTANCE.world[end[0]][end[1]]
    if not cell.is_explorable():
        return tuple()

    """
    Optimisation
    When a end point is discovered, we create a CandidateRoute.
    We then attempt to find home from this new end point, before fully expanding the map as an optimisation.

    This class is used to store the information between the expansions. E.g. path so far, current x and y pos etc.
    """

    class CandidateRoute():
        def __init__(self, end):
            # current coords of lowest cost neighbour
            self.y = end[0]
            self.x = end[1]
            self.end = end  # the inital end point from the ends array

            # upgrade this to map for order and fast lookup instead of two different lists
            self.path_out = [end]
            self.path_out_set = set()
            self.path_out_set.add(end)

    class HeuristicLOCATION():
        def __init__(self, location, cost, end):
            # current coords of lowest cost neighbour
            self.location = location
            self.cost = cost

            self.distance = get_euclidean_distance(location, end)

        def __hash__(self):
            return hash(self.location)

        def __lt__(self, other):
            return other.distance < self.distance

        def __eq__(self, other):
            return self.location == other.location

    perimeter_coords = SortedSet()
    perimeter_coords.add(HeuristicLOCATION(start, 0, end))

    while len(perimeter_coords) != 0:
        """
        If no end points left to reach, and no end points still being considered terminate.
        """

        heuristic_location = perimeter_coords.pop()

        loc = heuristic_location.location

        cost_map[loc[0]][loc[1]] = heuristic_location.cost
        # continue expanding if we own the territory or its free
        if cost_map[loc[0] - 1][loc[1]] == our_group_id:
            perimeter_coords.add(HeuristicLOCATION((loc[0] - 1, loc[1]), heuristic_location.cost + 1, end))

        if cost_map[loc[0]][loc[1] + 1] == our_group_id:
            perimeter_coords.add(HeuristicLOCATION((loc[0], loc[1] + 1), heuristic_location.cost + 1, end))

        if cost_map[loc[0]][loc[1] - 1] == our_group_id:
            perimeter_coords.add(HeuristicLOCATION((loc[0], loc[1] - 1), heuristic_location.cost + 1, end))

        if cost_map[loc[0] + 1][loc[1]] == our_group_id:
            perimeter_coords.add(HeuristicLOCATION((loc[0] + 1, loc[1]), heuristic_location.cost + 1, end))

        if loc == end:
            test_loc = CandidateRoute(loc)
            while True:
                results = SortedSet()

                """
                Finds minimum cost path
                We check to see if the tile in question:
                cost != IMPASSABLE_COST : tile is passable

                cost < 1000 : tile is not free const, therefore we have assigned it a value i.e. it has been checked
                OR
                cost == our_group_id : we own it therefore by definition we can do it

                """
                if (test_loc.y - 1, test_loc.x) not in test_loc.path_out_set:
                    if test_loc.y - 1 >= 0:
                        cost = cost_map[test_loc.y - 1][test_loc.x]
                        if cost != IMPASSABLE_CONST and (cost < UNCLAIMED_TERRITORY_FLAG or cost == our_group_id):
                            results.add(Result((test_loc.y - 1, test_loc.x), cost))

                if (test_loc.y + 1, test_loc.x) not in test_loc.path_out_set:
                    if test_loc.y + 1 < len(guiwindow.WORLD_INSTANCE.world):
                        cost = cost_map[test_loc.y + 1][test_loc.x]
                        if cost != IMPASSABLE_CONST and (cost < UNCLAIMED_TERRITORY_FLAG or cost == our_group_id):
                            results.add(Result((test_loc.y + 1, test_loc.x), cost))

                if (test_loc.y, test_loc.x - 1) not in test_loc.path_out_set:
                    if test_loc.x - 1 >= 0:
                        cost = cost_map[test_loc.y][test_loc.x - 1]
                        if cost != IMPASSABLE_CONST and (cost < UNCLAIMED_TERRITORY_FLAG or cost == our_group_id):
                            results.add(Result((test_loc.y, test_loc.x - 1), cost))

                if (test_loc.y, test_loc.x + 1) not in test_loc.path_out_set:

                    if test_loc.x + 1 < len(guiwindow.WORLD_INSTANCE.world[0]):

                        cost = cost_map[test_loc.y][test_loc.x + 1]
                        if cost != IMPASSABLE_CONST and (cost < UNCLAIMED_TERRITORY_FLAG or cost == our_group_id):
                            results.add(Result((test_loc.y, test_loc.x + 1), cost))

                """
                If no locations possible at this time, break and incriment no move counter
                """
                if len(results) == 0:
                    return tuple()

                """
                If start point in potential locations, we are finished
                """

                if Result(start, 0) in results:
                    test_loc.path_out.reverse()
                    return tuple(test_loc.path_out)

                """
                Registers lowest cost location.
                """

                best_result = results.pop()

                test_loc.y = best_result.location[0]
                test_loc.x = best_result.location[1]
                test_loc.path_out.append((test_loc.y, test_loc.x))
                test_loc.path_out_set.add((test_loc.y, test_loc.x))

    return tuple()



"""
Returns the flood filled coordinates for n_waves
n_waves = 0 will return just the given coordinate
n_waves = 1 will return the given coordinate and the 4 adjacents 
etc...
"""
def territory_flood_fill_radius(centre_coordinate ,n_waves, passable_groups):

    allowed_group_corridors = set()
    for group_id in passable_groups:
        allowed_group_corridors.add(group_id + 10000)


    if n_waves == 0:
        return set()

    # defining the first 'wave' of coordinates we will be checking through
    current_wave = [centre_coordinate]

    # this will be our output

    # keeping track of coordinates we've already checked
    checked = set()
    checked.add(centre_coordinate)
    # checking n_waves worth of coordinates
    while n_waves > 1:
        next_wave = set()
        # once this for loop has iterated once, we will use this 'next_wave' to loop through

        for coord in current_wave:
            checked.add(coord)

            for potential_coord in get_adjacent(coord):
                if (potential_coord not in checked) and\
                        (guiwindow.WORLD_INSTANCE.territory_map[potential_coord[0]][potential_coord[1]] == UNCLAIMED_TERRITORY_FLAG or
                         guiwindow.WORLD_INSTANCE.territory_map[potential_coord[0]][potential_coord[1]] in allowed_group_corridors):
                    next_wave.add(potential_coord)


        current_wave = next_wave
        n_waves -= 1

        if not next_wave:
            print("Empty!")
            break

    return checked





"""
Given the stockpile location and amount of members,
This calculates the minimum expansion size for flood fill
to house just enough people. 
"""
def territory_find_minimum_expansion_function_size(function, location, original_size, required_amount_cells, passable_groups):
    current_size = len(function(location, original_size, passable_groups))
    one_smaller_size = len(function(location, original_size - 1, passable_groups))

    # just the right size
    if current_size == required_amount_cells:
        return original_size

    # one size smaller is minimum
    if one_smaller_size == required_amount_cells:
        return original_size - 1

    # just the right size
    if current_size > required_amount_cells and one_smaller_size < required_amount_cells:
        return original_size


    # too big decrease size
    if one_smaller_size > required_amount_cells:
        return territory_find_minimum_expansion_function_size(function, location, original_size-1, required_amount_cells, passable_groups)

    # too small increase size
    return territory_find_minimum_expansion_function_size(function, location, original_size + 1, required_amount_cells, passable_groups)
