
import guiwindow
from functools import lru_cache
import math
from sortedcontainers import SortedSet
from math import sqrt
from global_params import TRAVERSABLE_FLAG


class Result():
    def __init__(self, location, cost):
        # current coords of lowest cost neighbour
        self.location = location
        self.cost = cost

    def __lt__(self, other):
        return other.cost < self.cost

    def __hash__(self):
        return hash((self.location))

    def __eq__(self, other):
        return self.location == other.location

"""
Gets perimeter of current position + radius.

Returns [] if all 4 sides out of bounds.
Only records safe coordinates such that they don't exceed/preceed max/min
"""
@lru_cache(maxsize=100)
def perimeter_radius(location, radius, minX, minY, maxX,  maxY):
    violate = 0

    startX = location[1] - radius
    if location[1] - radius < minX:
        violate += 1
        startX = minX

    endX = location[1] + radius
    if location[1] + radius >= maxX:
        violate += 1
        endX = maxX - 1

    startY = location[0] - radius
    if location[0] - radius < minY:
        violate += 1
        startY = minY

    endY = location[0] + radius
    if location[0] + radius >= maxY:
        violate += 1
        endY = maxY - 1

    """
    If radius exceeds whole map on all sides return nothing.
    """
    if violate == 4:
        return set()

    locations = set()

    for x in range(startX, endX, 1):
        locations.add((startY, x))


    for x in range(startX, endX+1, 1):
        locations.add((endY, x))


    for y in range(startY, endY, 1):
        locations.add((y, startX))

    for y in range(startY, endY, 1):
        locations.add((y, endX))


    return tuple(locations)


"""
returns euclidean distance between two input coordinates
"""

@lru_cache(maxsize=100)
def get_euclidean_distance(coord1, coord2):
    return sqrt(((coord1[0] - coord2[0]) ** 2) + ((coord1[1] - coord2[1]) ** 2))


"""
Gets area of current position + radius.
"""
@lru_cache(maxsize=100)
def get_area(location, radius, minX, minY, maxX,  maxY):

    violate = 0

    startX = location[1] - radius
    if location[1] - radius < minX:
        violate += 1
        startX = minX

    endX = location[1] + radius
    if location[1] + radius >= maxX:
        violate += 1
        endX = maxX - 1

    startY = location[0] - radius
    if location[0] - radius < minY:
        violate += 1
        startY = minY

    endY = location[0] + radius
    if location[0] + radius >= maxY:
        violate += 1
        endY = maxY - 1

    """
    If radius exceeds whole map on all sides return nothing.
    """
    if violate == 4:
        return set()

    locations = set()

    for y in range(startY, endY+1, 1):
        for x in range(startX, endX+1, 1):
            locations.add((y, x))

    return tuple(locations)

@lru_cache(maxsize=100)
def get_route(start,end):
    # print("In " + str(len(ends)))
    IMPASSABLE_CONST = -1


    # producing a new array (same size as world_map) to keep track of "costs" between nodes
    cost_map = guiwindow.WORLD_INSTANCE.traverse_map.copy()


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
            self.end = end # the inital end point from the ends array

            # upgrade this to map for order and fast lookup instead of two different lists
            self.path_out = [end]
            self.path_out_set = set()
            self.path_out_set.add(end)




    class HeuristicLOCATION():
        def __init__(self, location, cost, end):
            # current coords of lowest cost neighbour
            self.location = location
            self.cost = cost

            self.distance = get_euclidean_distance(location, end) + guiwindow.WORLD_INSTANCE.world[location[0]][location[1]].ground_type.attributes.explorable_cost

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
        # print(loc)
        # print(heuristic_location.distance)

        cost_map[loc[0]][loc[1]] = heuristic_location.cost


        # print("added:")
        if cost_map[loc[0] - 1][loc[1]] >= TRAVERSABLE_FLAG :
            perimeter_coords.add(HeuristicLOCATION((loc[0] - 1, loc[1]), heuristic_location.cost + 1, end))
        if cost_map[loc[0]][loc[1]+1] >= TRAVERSABLE_FLAG:
            perimeter_coords.add(HeuristicLOCATION((loc[0], loc[1]+1), heuristic_location.cost + 1, end))
        if cost_map[loc[0]][loc[1]-1] >= TRAVERSABLE_FLAG :
            perimeter_coords.add(HeuristicLOCATION((loc[0], loc[1]-1), heuristic_location.cost + 1, end))
        if cost_map[loc[0]+1][loc[1]] >= TRAVERSABLE_FLAG:
            perimeter_coords.add(HeuristicLOCATION((loc[0]+1, loc[1]), heuristic_location.cost + 1, end))



        if loc == end:
            test_loc = CandidateRoute(loc)
            while True:
                results = SortedSet()


                """
                Finds minimum cost path
                
                We check to see if the tile in question:
                cost != IMPASSABLE_COST : tile is passable
                cost != 1000 : tile is not free const, therefore we have already considered it as a path
                """
                if (test_loc.y-1, test_loc.x) not in test_loc.path_out_set:
                    if test_loc.y - 1 >= 0:
                        cost = cost_map[test_loc.y-1][test_loc.x]
                        if cost != IMPASSABLE_CONST and cost < TRAVERSABLE_FLAG:
                            results.add(Result((test_loc.y-1, test_loc.x), cost))


                if (test_loc.y+1, test_loc.x) not in test_loc.path_out_set:
                    if test_loc.y + 1 < len(guiwindow.WORLD_INSTANCE.world):
                        cost = cost_map[test_loc.y+1][test_loc.x]
                        if cost != IMPASSABLE_CONST and cost < TRAVERSABLE_FLAG:
                            results.add(Result((test_loc.y+1, test_loc.x), cost))

                if (test_loc.y, test_loc.x-1) not in test_loc.path_out_set:
                    if test_loc.x - 1 >= 0:
                        cost = cost_map[test_loc.y][test_loc.x-1]
                        if cost != IMPASSABLE_CONST and cost < TRAVERSABLE_FLAG:
                            results.add(Result((test_loc.y, test_loc.x-1), cost))


                if (test_loc.y, test_loc.x+1) not in test_loc.path_out_set:

                    if test_loc.x + 1 < len(guiwindow.WORLD_INSTANCE.world[0]):

                        cost = cost_map[test_loc.y][test_loc.x+1]
                        if cost != IMPASSABLE_CONST and cost < TRAVERSABLE_FLAG:
                            results.add(Result((test_loc.y, test_loc.x+1), cost))

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
                    # print("Out %s" % len(test_loc.path_out))
                    # print("FUCK2")
                    return tuple(test_loc.path_out)


                """
                Registers lowest cost location.
                """

                best_result = results.pop()


                test_loc.y = best_result.location[0]
                test_loc.x = best_result.location[1]
                test_loc.path_out.append((test_loc.y, test_loc.x))
                test_loc.path_out_set.add((test_loc.y, test_loc.x))

    print("kys")
    return tuple()



"""
The two functions below are used for flood filling
"""

"""
Returns the locations in the crosshair of the inputted coordinate
"""
def get_adjacent(coordinate):
    x, y = coordinate
    return set([(x - 1, y), (x + 1, y), (x, y - 1), (x, y + 1)])

"""
Returns the perimeter around inputted coordinate
"""
def get_perimeter(coordinate):
    x, y = coordinate
    return set([(x - 1, y), (x + 1, y), (x, y - 1), (x, y + 1), (x + 1, y + 1), (x - 1, y + 1), (x - 1, y - 1), (x + 1, y - 1)])


"""
Given a target location, and list of locations,
sort the list of locations such that the closest ones
to target locations are first
"""
def sort_by_closest(target_location, locations):
    return [ loc for cost, loc in sorted(
        [(get_euclidean_distance(target_location, end2), end2) for end2 in locations],
        key=lambda x: x[0])]


"""
Returns the flood filled coordinates for n_waves
n_waves = 0 will return just the given coordinate
n_waves = 1 will return the given coordinate and the 4 adjacents 
etc...
"""
@lru_cache(maxsize=100)
def flood_fill_radius(centre_coordinate,n_waves):

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
                if (potential_coord not in checked) and guiwindow.WORLD_INSTANCE.traverse_map[potential_coord[0]][potential_coord[1]] != -1:
                    next_wave.add(potential_coord)


        current_wave = next_wave
        n_waves -= 1

    return checked


"""
Returns the flood filled coordinates for n_waves
n_waves = 0 will return just the given coordinate
n_waves = 1 will return the given coordinate and the 4 adjacents 
etc...
"""
def flood_fill_find_closest(start,ends):

    ends = set(ends)

    if start in ends:
        return start

    # defining the first 'wave' of coordinates we will be checking through
    current_wave = set([start])

    # this will be our output

    # keeping track of coordinates we've already checked
    checked = set()
    checked.add(start)
    # checking n_waves worth of coordinates
    while current_wave:
        next_wave = set()
        # once this for loop has iterated once, we will use this 'next_wave' to loop through

        for coord in current_wave:
            checked.add(coord)

            for potential_coord in get_adjacent(coord):
                if (potential_coord not in checked) and guiwindow.WORLD_INSTANCE.traverse_map[potential_coord[0]][potential_coord[1]] != -1:
                    next_wave.add(potential_coord)
                    if potential_coord in ends:
                        return potential_coord

        current_wave = next_wave
    # exit(1)
    return tuple()


"""
Will return the first point in a route that makes a condition true
"""
def get_first_location_given(start_point, end_point, condition):
    route = list(get_route(start_point, end_point))

    if not route:
        print("Invalid end/start point defaulting to start point")
        return start_point

    rally_point = route[0]

    while route:
        next_loc = route.pop(0)
        if condition(guiwindow.WORLD_INSTANCE.world[next_loc[0]][next_loc[1]]):
            return rally_point
        rally_point = next_loc
    return rally_point

"""
Given the stockpile location and amount of members,
This calculates the minimum expansion size for flood fill
to house just enough people. 
"""
def find_minimum_expansion_function_size(function, location, original_size, required_amount_cells):
    current_size = len(function(location, original_size))
    one_smaller_size = len(function(location, original_size - 1))

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
        return find_minimum_expansion_function_size(function, location, original_size-1, required_amount_cells)

    # too small increase size
    return find_minimum_expansion_function_size(function, location, original_size + 1, required_amount_cells)









