from gameworld.timestamp import TimeStamp
from ai import pathfindingterritory

MAX_POSSIBLE_CORRIDOR_SIZE = 7
DEFAULT_TERRITORY_BUFFER = 3

class TerritoryNode():


    def __init__(self, locations, cellbase, visited):
        self.cellbase = cellbase
        self.locations = locations
        self.last_route_to_stockpile = []
        self.last_day_updated = TimeStamp().day
        self.all_territory_pixels = set()
        self.must_update = False

        self.visited = visited
        self.territory_default_buffer = DEFAULT_TERRITORY_BUFFER
        self.max_corridor_size = MAX_POSSIBLE_CORRIDOR_SIZE

        """
        Essentially prevents expansion until visited at least once
        """
        if not self.visited:
            self.territory_default_buffer = 1
            self.max_corridor_size = 1
        """
        Store adhoc data
        MAX possible expansion level
        When another gorup takes resource, surrounding nodes in that max expansion level is reset
        """

    """
    If a node has now been visited mark it as such
    """
    def set_visited(self):
        self.visited = True
        self.territory_default_buffer = DEFAULT_TERRITORY_BUFFER
        self.max_corridor_size = MAX_POSSIBLE_CORRIDOR_SIZE


    def hostile_takeover_max_territory_pixels(self, group, allowed_groups):
        self.calculate_route_back(group, allowed_groups)
        return self.get_territory_at_maturity(self.max_corridor_size, [group.id_number] + allowed_groups)


    """
    When stock pile is moved, we need make sure we can still travel back.    
    """
    def connected_to_stockpile(self, group):
        for loc in self.locations:
            if len(list(pathfindingterritory.get_territory_route(loc, group.stockpile_location, group))) != 0:
                return True
        return False

    def update_route_back(self, group):
        self.all_territory_pixels.clear()
        self.last_day_updated = TimeStamp().day
        self.calculate_route_back(group, [])

        territory_buffer = set()
        for loc in self.locations:
            territory_buffer.update(pathfindingterritory.territory_flood_fill_radius(loc, self.territory_default_buffer, [group.id_number]))

        self.all_territory_pixels.update(territory_buffer)
        self.all_territory_pixels.update(self.last_route_to_stockpile)

    def calculate_route_back(self, group, allowed_groups):
        # try any of the locations route back
        for loc in self.locations:
            self.last_route_to_stockpile = list(pathfindingterritory.get_corridor_territory_route(group.stockpile_location, loc, [group.id_number] + allowed_groups))
            if len(self.last_route_to_stockpile) != 0:
                break

    def reset_size(self):
        self.all_territory_pixels.clear()
        self.last_day_updated = TimeStamp().day
        self.must_update = True

    def get_current_size(self):
        """
        Don't register progress
        """
        if not self.visited:
            self.last_day_updated = TimeStamp().day


        difference = (TimeStamp().day - self.last_day_updated) + 2
        if difference <= self.max_corridor_size:
            return difference
        return self.max_corridor_size



    def daily_update(self, group):
        """
        Don't register progress
        """
        if not self.visited:
            self.last_day_updated = TimeStamp().day

        new_territory = set()
        difference = (TimeStamp().day - self.last_day_updated) + 2
        if difference <= self.max_corridor_size:

            new_territory.update(self.get_territory_at_maturity(difference, [group.id_number]))
            self.all_territory_pixels = new_territory

        return new_territory

    def get_territory_at_maturity(self, maturity, allowed_groups):
        new_territory = set()

        """
        Expand group buffer
        """
        for loc in self.locations:
            new_territory.update(pathfindingterritory.territory_flood_fill_radius(loc, self.territory_default_buffer, allowed_groups))

        """
        Expand corridor
        """
        for corridoor_node in list(self.last_route_to_stockpile):
            new_territory.update(pathfindingterritory.territory_flood_fill_radius(corridoor_node, maturity, allowed_groups))

        return new_territory

    def __hash__(self):
        return hash((self.locations, self.cellbase))

    def __eq__(self, other):
        return self.__class__ == other.__class__ and\
               self.locations == other.locations and\
               self.cellbase == other.cellbase

    def __repr__(self):
        return "Territory Node Location: %s Cell: %s" % (self.locations, self.cellbase)