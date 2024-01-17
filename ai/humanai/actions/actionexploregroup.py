from ai.action import Action
from copy import deepcopy


"""
Goes to a location

A wrapper for performing an action, including a cost function, prerequisite conditions and worker logic.
"""
class ActionExploreGroup(Action):


    """
    The estimated cost of this action.
    This occurs during the decision making process of a action tree.
    For extra accuracy, use data from prerequisites.
    """
    def get_costs(self, human):
        """
        Cost is how long it takes to get to that location
        """
        return 0

    """
    This is called once when the action begins.
    """
    def begin(self, human):
        self.locations = deepcopy(human.group.sleeping_locations)

        human.find(self.locations[0])
        self.locations.pop(0)

    """
    Called every tick while the action has begun and not completed yet.
    Returns True/False to indicate if an error occurs.
    """
    def tick(self, human):
        if human.arrived_at_location():
            self.locations.pop(0)
            if self.locations:
                human.find(self.locations[0])
            # print(print(human.knowledge_people_sleeping_locations.believes_all_group_sleeping_locations_taken(human)))
        human.step_towards_route()
        return True


    """
    Returns true/false to indicate whether the action is complete or not.
    Called every tick before tick() is executed.    
    """
    def is_complete(self, human):
        return len(self.locations) == 0


    def __str__(self):
        return "Explore group"

