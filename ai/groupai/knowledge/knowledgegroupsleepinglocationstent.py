
from ai.humanai.relationships.knowledge.knowledge import Knowledge
import guiwindow
from gameworld.cell.cellbuilding.cellbuildinghouse import BuildingHouse
from ai.groupai.knowledge.knowledgegroupsleepinglocations import KnowledgeGroupSleepingLocations, SleepingLocation, personality_multiplier, multiplier
from ai import pathfinding
from ai.humanai.actions.actionsleep import ActionSleep
import math
from ai.humanai.relationships.attributes.personality import MAX_PERSONALITY_DIFFERENCE_CONSTANT
from ai.need import NEED_TYPE

class SleepingLocationTent(SleepingLocation):

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
        super().__init__(location, group.knowledge_sleeping_location_tents) # ALWAYS CALL PARENT CONSTRUCTOR
        self.location = location


    def get_action(self):
        return ActionSleep(self.location)


    def __repr__(self):
        return str("Tent at %s" % (str(self.location)))



class KnowledgeGroupSleepingLocationsTent(KnowledgeGroupSleepingLocations):

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
        self.hash_id = guiwindow.WORLD_INSTANCE.knowledge_sleeping_location_tent_id_counter
        guiwindow.WORLD_INSTANCE.knowledge_sleeping_location_tent_id_counter += 1
        self.sleeping_location_to_person = {} # {location : person}

    """
    Returns set of occupants at a specific location
    """
    def get_occupants_at(self, location):
        if location in self.sleeping_location_to_person.keys():
            if self.sleeping_location_to_person[location] is None:
                return set()
            return set([self.sleeping_location_to_person[location]])
        return set()

    """
    Returns all locations 
    """
    def get_all_locations(self):
        ...

    """
    Returns all locations that are free
    """
    def get_all_free_locations(self):
        return set([loc for (loc, person) in self.sleeping_location_to_person.items() if person is None])

    """
    Called when a person leaves a location
    """
    def take_location(self, person, location):
        self.sleeping_location_to_person[location] = person.id_number

    """
    Called when registering a person onto a location
    """
    def leave_location(self, person):
        if person.sleeping_location.location in self.sleeping_location_to_person.keys():
            self.sleeping_location_to_person[person.sleeping_location.location] = None

    """
    Should return a sleeping location object given a location.
    """
    def create_sleeping_location(self, group, location):
        return SleepingLocationTent(group, location)


    def amount_taken_spaces(self):
        return sum(x is not None for x in self.sleeping_location_to_person.values())


    def valid_sleep_at(self, location, human):
        return self.is_a_location(location) and self.person_at(location) == human.id_number


    def is_a_location(self, location):
        return location in self.sleeping_location_to_person.keys()

    """
    Returns true or false if the location is a valid spot to sleep, despite who sleeps there
    """
    def is_valid_location(self, location):
        return location in self.sleeping_location_to_person.keys()


    def register_group_sleeping_locations(self, new_sleeping_locations):
        remove = []
        for location in self.sleeping_location_to_person.keys():
            if location not in new_sleeping_locations:
                remove.append(location)

        for location in remove:
            """
            Inform them their house is gone.
            This is important otherwise they try travel back
            """
            person_id_dehoused = self.sleeping_location_to_person[location]
            if person_id_dehoused is not None:
                human = guiwindow.WORLD_INSTANCE.humanDict[person_id_dehoused]
                human.needs[NEED_TYPE.BETTER_SLEEPING_LOCATION].set_new_sleeping_location(human, None)
            del self.sleeping_location_to_person[location]

        for location in new_sleeping_locations:
            if location not in self.sleeping_location_to_person.keys():
                self.sleeping_location_to_person[location] = None

        """
        PURELY FOR DISPLAY (JUST RERENDERS OLD CELLS TO GET RID OF BLACK)
        """
        if guiwindow.WORLD_INSTANCE.rerender_group_sleeper_cells:
            for sleeper_cell in set(new_sleeping_locations).union(set(remove)):
                guiwindow.WORLD_INSTANCE.rerender_location(sleeper_cell)

    def get_sleeping_locations(self):
        return self.sleeping_location_to_person.keys()


    """
    Used to determine preference of sleeping locations
    """
    def calculate_sleeping_location_score(self, human, location):
        score = pathfinding.get_euclidean_distance(location, human.group.stockpile_location)
        for loc in pathfinding.get_adjacent(location):
            occupants_at_location = self.get_occupants_at(loc)
            if self.is_a_location(loc) and occupants_at_location:
                inhabitant_id = list(occupants_at_location)[0] # will only ever be one occupant at a tent spot
                score += human.knowledge_of_people.human_opinions.overall_score_sorted[inhabitant_id] * personality_multiplier
            else:
                score += MAX_PERSONALITY_DIFFERENCE_CONSTANT * personality_multiplier

        return (score * multiplier, location)
