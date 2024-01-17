from ai.humanai.relationships.knowledge.knowledge import Knowledge
from ai.humanai.relationships.information.informationlocationpeople import InformationLocationPeople
import random

class KnowledgePeopleLocations(Knowledge):

    """
    DO NOT DELETE THIS. PASTE THIS IN FOR EVERY NEW OBJECT THAT WILL BE STORED IN A SET/DICTIONARY.
    THIS IS ESSENTIAL FOR MAKING SURE THE PROGRAM PERFORMS EXACTLY THE SAME EVERY TIME!

    assert(false) WILL CRASH THE PROGRAM IF YOU ATTEMPT TO PUT THIS OBJECT INTO A SET/DICT WITHOUT FIRST MODIFYING THE FUNCTION.
    THIS IS DONE ON PURPOSE TO PREVENT YOU FROM ACCIDENTALLY LEAKING NON-DETERMINISM INTO THE PROGRAM.
    SPEAK TO ME (TOM) AND I WILL EXPLAIN WHAT TO DO.
    """
    def __hash__(self):
        assert(False)

    def __init__(self, knowledge_people):
        self.knowledge_people = knowledge_people
        self.last_known_people_locations = {} # {location : person}


    """
    Helper function, quickly register if a location has no people in
    """
    def _location_is_empty(self, loc):
        # if people not in cell
        # if previously seen people in this cell
        if loc in self.last_known_people_locations.keys():
            for person_id in self.last_known_people_locations[loc]:
                # we no longer know where this person is
                self.knowledge_people.get_knowledge_of_person(person_id).location = None

            del self.last_known_people_locations[loc]

    """
    For use when registering MULTIPLE people at location
    """
    def register_from_information(self, human, informationlocationpeople):
        people = informationlocationpeople.people
        loc = informationlocationpeople.location
        if len(people) > 0:
            # if we have previously seen people on cell
            if self.knows_people_at_location(loc):
                # if it is different people on cell
                prev_people_at_location = self.get_people_at_location(loc)

                if prev_people_at_location != people:
                    # all the people who are no longer on cell get removed
                    for missing_person in prev_people_at_location.difference(people):
                        self.knowledge_people.get_knowledge_of_person(missing_person).location = None

                    # the remaining people, remove them from their existing set
                    for person_id in people.difference(prev_people_at_location):
                        person_location = self.knowledge_people.get_knowledge_of_person(person_id).location
                        if person_location is not None:
                            old_seen_loc = self.last_known_people_locations[person_location]
                            old_seen_loc.remove(person_id)
                            if len(old_seen_loc) == 0:
                                del self.last_known_people_locations[person_location]

                    # take note of all people on cells
                    self.last_known_people_locations[loc] = people

                    # register where individual people are
                    for person_id in self.last_known_people_locations[loc]:
                        self.knowledge_people.get_knowledge_of_person(person_id).location = loc
                        # print("spotted")


            else:
                # print("Never seen anyone on this cell before")
                # if never been on this cell register all the individual people

                for person_id in people:
                    person_location = self.knowledge_people.get_knowledge_of_person(person_id).location
                    if person_location is not None:
                        old_seen_loc = self.last_known_people_locations[person_location]
                        old_seen_loc.remove(person_id)
                        if len(old_seen_loc) == 0:
                            del self.last_known_people_locations[person_location]

                    self.knowledge_people.get_knowledge_of_person(person_id).location = loc
                    # print("spotted")

                # take not of all people on cells
                self.last_known_people_locations[loc] = people  # optimise potentially
        else:
            self._location_is_empty(loc)


    def knows_people_at_location(self, location):
        return location in self.last_known_people_locations.keys()

    def get_people_at_location(self, location):
        return self.last_known_people_locations[location]

    def knows_person_location(self, person_id):
        return self.knowledge_people.get_knowledge_of_person(person_id).location is not None

    def get_person_location(self, person_id):
        return self.knowledge_people.get_knowledge_of_person(person_id).location


    def amount_known_locations_with_people(self):
        return len(self.last_known_people_locations)

    def get_all_locations(self):
        return self.last_known_people_locations.keys()


    """
    Use this method to return a random piece of information
    that you can create from the knowledge. 
    This is for use in interactions, get_random_information may be called
    to simulate random conversation being passed.
    """
    def get_random_information(self):
        loc = random.choice(list(self.last_known_people_locations.keys()))
        return InformationLocationPeople(loc, self.get_people_at_location(loc))
