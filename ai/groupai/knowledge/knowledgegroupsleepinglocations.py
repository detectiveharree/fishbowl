from ai.humanai.relationships.knowledge.knowledge import Knowledge
from abc import ABC, abstractmethod
import guiwindow
from gameworld.cell.cellbuilding.cellbuildinghouse import BuildingHouse
from ai.humanai.actions.actioninteractcellsleephouse import ActionInteractCellSleepHouse
from ai.humanai.actions.actionsleep import ActionSleep

multiplier = 1
personality_multiplier = 5




class SleepingLocation(ABC):

    """
    DO NOT DELETE THIS. PASTE THIS IN FOR EVERY NEW OBJECT THAT WILL BE STORED IN A SET/DICTIONARY.
    THIS IS ESSENTIAL FOR MAKING SURE THE PROGRAM PERFORMS EXACTLY THE SAME EVERY TIME!

    assert(false) WILL CRASH THE PROGRAM IF YOU ATTEMPT TO PUT THIS OBJECT INTO A SET/DICT WITHOUT FIRST MODIFYING THE FUNCTION.
    THIS IS DONE ON PURPOSE TO PREVENT YOU FROM ACCIDENTALLY LEAKING NON-DETERMINISM INTO THE PROGRAM.
    SPEAK TO ME (TOM) AND I WILL EXPLAIN WHAT TO DO.
    """
    def __hash__(self):
        assert(False)

    def __init__(self, location, group_sleeping_knowledge_helper):
        self.location = location
        self.group_sleeping_knowledge_helper = group_sleeping_knowledge_helper

    def check_still_valid(self, person):
        return self.group_sleeping_knowledge_helper.can_sleep_here(person, self.location)

    def get_preference_score(self, person):
        return self.group_sleeping_knowledge_helper.calculate_sleeping_location_score(person, self.location)[0]

    def take_location(self, human):
        self.group_sleeping_knowledge_helper.take_location(human, self.location)

    def leave_location(self, human):
        self.group_sleeping_knowledge_helper.leave_location(human)

    @abstractmethod
    def get_action(self):
        ...



class KnowledgeGroupSleepingLocations(ABC):


    """
    Returns set of occupants at a specific location
    """
    @abstractmethod
    def get_occupants_at(self, location):
        ...


    """
    Returns all locations 
    """
    @abstractmethod
    def get_all_locations(self):
        ...

    """
    Returns all locations that are free
    """
    @abstractmethod
    def get_all_free_locations(self):
        ...


    """
    Called when a person leaves a location
    """
    @abstractmethod
    def take_location(self, person, location):
        ...

    """
    Called when registering a person onto a location
    """
    @abstractmethod
    def leave_location(self, person):
        ...

    """
    Used to determine preference of sleeping locations
    """
    @abstractmethod
    def calculate_sleeping_location_score(self, person, location):
        ...

    """
    Returns true or false if the location is a valid spot to sleep, despite who sleeps there
    """
    @abstractmethod
    def is_valid_location(self, location):
        ...

    """
    Should return a sleeping location object given a location.
    """
    @abstractmethod
    def create_sleeping_location(self, group, location):
        ...


    """
    Called when a person checks to see if they can go to sleep at a specific
    location. 
    Should be concerned with verifying if it's a valid sleeping location and 
    if the person actually belongs there.
    """
    def can_sleep_here(self, person, location):
        return self.is_valid_location(location) and person.id_number in self.get_occupants_at(location)

    """
    Finds and returns the best sleeping location.
    Returns (score, location)
    """
    def find_best_sleeping_location(self, human):
        possible_locs = []
        for loc in self.get_all_free_locations():
            possible_locs.append(self.calculate_sleeping_location_score(human, loc))

        if not possible_locs:
            return None

        best = sorted(possible_locs, key=lambda x: x[0])[0]
        return best
