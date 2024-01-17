from entities.group import Group
import human
import global_params
from ai.humanai.relationships.attributes.racepresets.racepresetdefault import RacePresetDefault
from ai.humanai.relationships.attributes.body.body import Body, GENDER_TYPE
from random import randint
from human import Human
import numpy as np
import guiwindow
from ai import pathfinding

def standard_human(starting_location):
    gender = GENDER_TYPE.MALE if randint(0, 1) == 1 else GENDER_TYPE.FEMALE

    # its essential we don't init two groups on each other from the very start
    assert(guiwindow.WORLD_INSTANCE.world[starting_location[0]][starting_location[1]].group_center is None)
    # return Human(starting_location, RacePresetDefault().get_standard_personality(gender), body=RacePresetDefault().get_standard_body(gender))
    body = Body(gender, genetic_weight=np.random.uniform(0, 1), genetic_strength=np.random.uniform(0, 1), age=randint(18, 50))
    return Human(starting_location, RacePresetDefault().get_standard_personality(gender), body=body)

def spawn_group(loc, amount):


    people = []


    current_expansion_level = pathfinding.find_minimum_expansion_function_size(pathfinding.flood_fill_radius,
                                                                                    loc,
                                                                                    1,
                                                                                    amount)

    spots = list(pathfinding.sort_by_closest(loc, pathfinding.flood_fill_radius(loc, current_expansion_level)))


    for i in range(amount):
        people.append(standard_human(spots[i]))

    for i in range(amount):
        if i == 0:
            continue
        people[i].switch_group(people[0].group)

def spawn_person(loc):
    return standard_human(loc)

