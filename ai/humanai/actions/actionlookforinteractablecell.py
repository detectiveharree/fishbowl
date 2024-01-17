from ai.action import Action
from ai import pathfinding

"""
Looks for a free resource.

A wrapper for performing an action, including a cost function, prerequisite conditions and worker logic.
"""
class ActionLookForInteractableCell(Action):

    """
    DO NOT DELETE THIS. PASTE THIS IN FOR EVERY NEW OBJECT THAT WILL BE STORED IN A SET/DICTIONARY.
    THIS IS ESSENTIAL FOR MAKING SURE THE PROGRAM PERFORMS EXACTLY THE SAME EVERY TIME!

    assert(false) WILL CRASH THE PROGRAM IF YOU ATTEMPT TO PUT THIS OBJECT INTO A SET/DICT WITHOUT FIRST MODIFYING THE FUNCTION.
    THIS IS DONE ON PURPOSE TO PREVENT YOU FROM ACCIDENTALLY LEAKING NON-DETERMINISM INTO THE PROGRAM.
    SPEAK TO ME (TOM) AND I WILL EXPLAIN WHAT TO DO.
    """
    def __hash__(self):
        assert(False)


    def __init__(self, cell_category, cell_type, human):
        self.cell_category = cell_category
        self.cell_type = cell_type
        self.human = human
        self.current_points = []
        self.start_point = human.location


    """
    The estimated cost of this action.
    This occurs during the decision making process of a action tree.
    For extra accuracy, use data from prerequisites.
    """
    def get_costs(self, human):
        return 1000

    def reset_current_points(self, human):
        self.current_points = sorted([(pathfinding.get_euclidean_distance(self.start_point, end2), end2) for end2 in human.unexplored_points],
               key=lambda x: x[0])

    def get_next_point(self, human):
        if not self.current_points:
            self.reset_current_points(human)
        return self.current_points.pop(0)[1]

    """
    This is called once when the action begins.
    """
    def begin(self, human):
        self.reset_current_points(human)

        pass
        # if len(human.unexplored_points) == 0:
        #     human.reset_explored_points()
        # human.explore(human.unexplored_points)

    """
    Called every tick while the action has begun and not completed yet.
    Returns True/False to indicate if an error occurs.
    """
    def tick(self, human):


        if len(human.unexplored_points) == 0:
            human.reset_explored_points()

        if human.arrived_at_location():
            human.find(self.get_next_point(human))
        human.step_towards_route()
        return True

    """
    Returns true/false to indicate whether the action is complete or not.
    Called every tick before tick() is executed.    
    """
    def is_complete(self, human):
        return len(human.knowledge_cell_locations.get_interactable_cells(self.cell_category, self.cell_type, human)) != 0


    def __str__(self):
        return "Looking for free %s: explored (%s/%s)" % (self.cell_type, len(self.human.explored_points), len(self.human.unexplored_points))