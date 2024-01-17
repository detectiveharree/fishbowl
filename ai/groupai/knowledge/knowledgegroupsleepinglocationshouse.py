
from ai.humanai.relationships.knowledge.knowledge import Knowledge
import guiwindow
from gameworld.cell.cellbuilding.cellbuildinghouse import BuildingHouse
from ai.groupai.knowledge.knowledgegroupsleepinglocations import KnowledgeGroupSleepingLocations, SleepingLocation, personality_multiplier, multiplier
from ai.humanai.actions.actioninteractcellsleephouse import ActionInteractCellSleepHouse
import math
import guiwindow
from ai import pathfinding
from ai.need import NEED_TYPE

class SleepingLocationHouse(SleepingLocation):

    """
    DO NOT DELETE THIS. PASTE THIS IN FOR EVERY NEW OBJECT THAT WILL BE STORED IN A SET/DICTIONARY.
    THIS IS ESSENTIAL FOR MAKING SURE THE PROGRAM PERFORMS EXACTLY THE SAME EVERY TIME!

    assert(false) WILL CRASH THE PROGRAM IF YOU ATTEMPT TO PUT THIS OBJECT INTO A SET/DICT WITHOUT FIRST MODIFYING THE FUNCTION.
    THIS IS DONE ON PURPOSE TO PREVENT YOU FROM ACCIDENTALLY LEAKING NON-DETERMINISM INTO THE PROGRAM.
    SPEAK TO ME (TOM) AND I WILL EXPLAIN WHAT TO DO.
    """
    def __hash__(self):
        assert(False)

    def __init__(self, group, location):
        super().__init__(location, group.knowledge_sleeping_location_house) # ALWAYS CALL PARENT CONSTRUCTOR

    def get_action(self):
        return ActionInteractCellSleepHouse(self.location)

    def __repr__(self):
        return str("House at %s" % (str(self.location)))



class KnowledgeGroupSleepingLocationsHouse(KnowledgeGroupSleepingLocations):

    """
    DO NOT DELETE THIS. PASTE THIS IN FOR EVERY NEW OBJECT THAT WILL BE STORED IN A SET/DICTIONARY.
    THIS IS ESSENTIAL FOR MAKING SURE THE PROGRAM PERFORMS EXACTLY THE SAME EVERY TIME!

    assert(false) WILL CRASH THE PROGRAM IF YOU ATTEMPT TO PUT THIS OBJECT INTO A SET/DICT WITHOUT FIRST MODIFYING THE FUNCTION.
    THIS IS DONE ON PURPOSE TO PREVENT YOU FROM ACCIDENTALLY LEAKING NON-DETERMINISM INTO THE PROGRAM.
    SPEAK TO ME (TOM) AND I WILL EXPLAIN WHAT TO DO.
    """
    def __hash__(self):
        return hash(self.hash_id)

    def __eq__(self, other):
        return self.__class__ == other.__class__ and self.hash_id == other.hash_id

    def __init__(self):
        self.hash_id = guiwindow.WORLD_INSTANCE.knowledge_sleeping_location_house_id_counter
        guiwindow.WORLD_INSTANCE.knowledge_sleeping_location_house_id_counter += 1
        self.house_location_to_people = {} # {location : [people]}
        self.houses_with_capacity = set()

    def total_spots_available(self):
        return len(self.house_location_to_people) * BuildingHouse.get_building_capacity()

    def count_house_spots_taken(self):
        return sum([sum(people) for location, people in self.house_location_to_people.items()])


    """
    Returns true or false if the location is a valid spot to sleep, despite who sleeps there
    """
    def is_valid_location(self, location):
        return location in self.house_location_to_people.keys()

    """
    Returns set of occupants at a specific location
    """
    def get_occupants_at(self, location):
        return self.house_location_to_people[location]


    """
    Returns all locations 
    """
    def get_all_locations(self):
        ...

    """
    Returns all locations that are free
    """
    def get_all_free_locations(self):
        return self.houses_with_capacity

    """
    Should return a sleeping location object given a location.
    """
    def create_sleeping_location(self, group, location):
        return SleepingLocationHouse(group, location)



    """
    Called when a person leaves a location
    """
    def take_location(self, person, location):

        amount_occupants = len(self.house_location_to_people[location])
        if amount_occupants == BuildingHouse.get_building_capacity():
            return False

        if (amount_occupants + 1) == BuildingHouse.get_building_capacity():
            self.houses_with_capacity.remove(location)

        self.house_location_to_people[location].add(person.id_number)
        return True


    """
    Called when registering a person onto a location
    """
    def leave_location(self, person):
        if person.sleeping_location.location in self.house_location_to_people.keys():
            self.house_location_to_people[person.sleeping_location.location].remove(person.id_number)
            self.houses_with_capacity.add(person.sleeping_location.location)



    """
    Used to determine preference of sleeping locations
    """
    def calculate_sleeping_location_score(self, human, location):
        score =  pathfinding.get_euclidean_distance(location, human.group.stockpile_location)
        for occupant in self.get_occupants_at(location):
            score += human.knowledge_of_people.human_opinions.overall_score_sorted[occupant] * personality_multiplier

        score -= 20
        return (score * multiplier, location)



    def register_house(self, group, location):
        if location in self.house_location_to_people.keys():
            return
        print("registering house at %s " % (str(location)))
        self.house_location_to_people[location] = set()
        self.houses_with_capacity.add(location)


    def remove_house(self, location):
        # sometimes we may not have recorded the house in the first place
        # due to for example not being out territory
        print("removing house at %s" % (str(location)))
        """
        Inform them their house is gone.
        This is important otherwise they try travel back
        """

        for person_id in list(self.house_location_to_people[location]):
            if person_id is not None:
                human = guiwindow.WORLD_INSTANCE.humanDict[person_id]
                human.needs[NEED_TYPE.BETTER_SLEEPING_LOCATION].set_new_sleeping_location(human, None)



        del self.house_location_to_people[location]
        self.houses_with_capacity.remove(location)

