import random
from ai import pathfinding
from gameworld.cell.cellresource.cellresourcefarm import CellResourceFarm
import guiwindow
from random import shuffle
from math import sqrt

"""
iterates out from the rally point, placing farms
"""


def place_n_farms(rally_point_coord, n_farms, max_blob_size, max_blob_length):
    non_farm_buildings = set([rally_point_coord])

    # lists to store invalid coordinates
    invalid_coordinates = set()
    potential_coordinates = []
    potential_coordinates_helper = set()

    # list to store placed_farms
    placed_farms = []

    # adding first coordinates to test
    for coord in get_perimeter(rally_point_coord):
        potential_coordinates.append(coord)
        potential_coordinates_helper.add(coord)

    # placing coordinates
    for coord in potential_coordinates:
        if coord[0] >= 127 or coord[1] >= 127 or coord[0] < 0 or coord[1] < 0:
            continue

        # check if all farms have been placed
        if n_farms == 0:
            break

        # adding perimeter coordinates to coordinate being checked
        for coord2 in get_perimeter(coord):

            if (coord2 not in invalid_coordinates) and (coord2 not in potential_coordinates_helper) and \
                    guiwindow.WORLD_INSTANCE.traverse_map[coord2[0]][coord2[1]] != -1:
                potential_coordinates.append(coord2)
                potential_coordinates_helper.add(coord2)

        # check if farm can be placed on this coordinate
        if is_farm_placeable(coord, non_farm_buildings, max_blob_size, max_blob_length):
            # place farm
            CellResourceFarm({coord}).register_to_world()
            placed_farms.append(coord)
            n_farms -= 1
        else:
            # farm unplaceable
            invalid_coordinates.add(coord)


"""
Optimised verison of flood fill used for determining a valid placement of
a building, utilising groups building info.
"""
"""
Returns the flood filled coordinates for n_waves
n_waves = 0 will return just the given coordinate
n_waves = 1 will return the given coordinate and the 4 adjacents 
etc...
"""
def place_building(building_type,group):

    # defining the first 'wave' of coordinates we will be checking through
    current_wave = [group.stockpile_location]

    # this will be our output

    # keeping track of coordinates we've already checked
    checked = set()
    checked.add(group.stockpile_location)
    # checking n_waves worth of coordinates
    while True:
        next_wave = set()
        # once this for loop has iterated once, we will use this 'next_wave' to loop through

        for coord in current_wave:
            checked.add(coord)

            for potential_coord in pathfinding.get_adjacent(coord):

                if (potential_coord not in checked) and guiwindow.WORLD_INSTANCE.traverse_map[potential_coord[0]][potential_coord[1]] != -1:

                    """
                    If start coord is not marked as invalid, go for it
                    """
                    if potential_coord not in group.invalid_building_placements[building_type]:
                        building_coords = []
                        """
                        If all other coords are buildable and free
                        """
                        for i in range(0, building_type.cells, 1):
                            new_coord = (potential_coord[0], potential_coord[1]-i)
                            if guiwindow.WORLD_INSTANCE.world[new_coord[0]][new_coord[1]].is_buildable():
                                building_coords.append(new_coord)
                                continue
                            building_coords.clear()
                            break
                        if building_coords:
                            if random.uniform(0, 1) < building_type.rng_placement_probability:
                                print("building_type %s %s" % (building_type, potential_coord))
                                return building_coords

                        group.invalid_building_placements[building_type].add(potential_coord)

                    next_wave.add(potential_coord)

        current_wave = next_wave


"""

FARM PLACING HELPER FUNCTIONS

"""


"""
checks blob_size of the blob the coordinate would create (if it were to be placed)
checks blob_max_length (max between height and width of blob),
   if blob_size and blob_max_length are below what is given in input:
       return True
   else:
       return False
"""

def check_blob_parameters(coord, max_blob_size, max_blob_length):
    # make a set to store members of the 'blob', and define potential_coordinates to check first
    blob_members = set([coord])
    potential_coordinates = get_perimeter(coord)
    potential_coordinates_helper = set(get_perimeter(coord))
    checked_coordinates = set()
    # iterate through potential coordinates
    for perim in potential_coordinates:
        # check if the coordinate is a farm, if so, add it to blob_members
        cell = guiwindow.WORLD_INSTANCE.world[perim[0]][perim[1]]
        if cell.is_farm():
            blob_members.add(perim)

            # add perimeter coordinates of the coordinate you just added to potential_coordinates
            for perim2 in get_perimeter(perim):
                if (perim2 not in potential_coordinates_helper) and (perim2 not in checked_coordinates) and \
                        guiwindow.WORLD_INSTANCE.world[perim2[0]][perim2[1]].is_farm():
                    potential_coordinates.append(perim2)
                    potential_coordinates_helper.add(perim2)
                    checked_coordinates.add(perim)


    # if number of blob_members is below max allowed blob length, we can just return True
    if len(blob_members) < max_blob_length:
        return True

    # get the leftmost, rightmost, etc. coordinates (in order to check length)
    blob_members = list(blob_members)
    leftmost = min(blob_members, key=lambda i: i[0])[0]
    rightmost = max(blob_members, key=lambda i: i[0])[0]
    topmost = min(blob_members, key=lambda i: i[1])[1]
    bottommost = max(blob_members, key=lambda i: i[1])[1]

    return (len(blob_members) + 1 < max_blob_size) and (
            max(rightmost - leftmost, bottommost - topmost) < max_blob_length)



"""
returns 8 coordinates in immediate periphery of input coordinate
"""


def get_perimeter(coord):
    perimeter = []
    for i in [coord[0] - 1, coord[0], coord[0] + 1]:
        for j in [coord[1] - 1, coord[1], coord[1] + 1]:
            if (i, j) != coord:
                perimeter.append((i, j))
    shuffle(perimeter)
    return perimeter


"""
receives map_array and coord for prospective farm, returns whether it is placeable as boolean
"""


def is_farm_placeable(coord, non_farm_buildings, max_blob_size, max_blob_length):
    # defining unplaceables
    cell = guiwindow.WORLD_INSTANCE.world[coord[0]][coord[1]]
    if not cell.is_buildable():
        return False

    if not cell.is_farmable():
        return False
    # checking if coord is within 2 euclidean distance of non_farm_buildings
    for non_farm_building_coord in non_farm_buildings:
        if pathfinding.get_euclidean_distance(coord, non_farm_building_coord) <= 0:
            return False

    # checking if periphery is river/seawater
    for perim in get_perimeter(coord):
        cell = guiwindow.WORLD_INSTANCE.world[perim[0]][perim[1]]
        if cell.can_farm_adjacent():
            return False

    # checking blob parameters are satisfied
    if not check_blob_parameters(coord, max_blob_size, max_blob_length):
        return False

    return True

