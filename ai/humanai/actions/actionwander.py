import guiwindow
from ai.action import Action
from ai.humanai.actions.actiongotolocation import ActionGoToLocation
from ai import pathfinding
from random import randint

"""
Goes to a location

A wrapper for performing an action, including a cost function, prerequisite conditions and worker logic.
"""
class ActionWander(ActionGoToLocation):


    def __init__(self, human):

        # figure out location

        locations = pathfinding.flood_fill_radius(human.location, 30)
        random_loc = list(locations)[randint(0, len(locations)-1)]
        super().__init__(random_loc) # ALWAYS CALL PARENT CONSTRUCTOR


    """
    Called every tick while the action has begun and not completed yet.
    Returns True/False to indicate if an error occurs.
    """
    def tick(self, human):

        # if human.emotions.sadness.value.get() > 0:
        #     human.emotions.sadness.value -= max(5,human.emotions.sadness.value*0.02)
        # if human.emotions.frustration.value > 0:
        #     human.emotions.frustration.value -= max(5,human.emotions.frustration.value*0.02)
        # if human.emotions.fear.value > 0:
        #     human.emotions.fear.value -= max(5,human.emotions.frustration.value*0.02)
        # human.emotions.happiness.value += 3

        return super().tick(human) # ALWAYS CALL PARENT CONSTRUCTOR

    def __str__(self):
        return "Wandering"

