from ai.humanai.actions.actiongotolocation import ActionGoToLocation


"""
Goes to a location

A wrapper for performing an action, including a cost function, prerequisite conditions and worker logic.
"""
class ActionMoveWithCaravan(ActionGoToLocation):


    def __init__(self, human, group_action):

        self.group_action = group_action

        super().__init__(human.expected_caravan_location) # ALWAYS CALL PARENT CONSTRUCTOR


    """
    Called every tick while the action has begun and not completed yet.
    Returns True/False to indicate if an error occurs.
    """
    def tick(self, human):

        if self.group_action.move:
            human.find(human.expected_caravan_location)

        if not human.arrived_at_location():
            return super().tick(human) # ALWAYS CALL PARENT CONSTRUCTOR
        else:
            self.group_action.people_arrived.add(human.id_number)

        return True


    """
    Called whenever a action is completed 
    """
    def on_finish(self, human):
        # if you finish for whatever other reason just treat it as arrived so as not to freeze group task
        self.group_action.people_arrived.add(human.id_number)

    """
    Returns true/false to indicate whether the action is complete or not.
    Called every tick before tick() is executed.    
    """
    def is_complete(self, human):
        return self.group_action.is_complete(human.group)

    def __str__(self):
        return "Moving with caravan"

