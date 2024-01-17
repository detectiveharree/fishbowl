from ai.action import Action
import ai.humanai.prerequisites.prerequisiteknowspersonlocation
import guiwindow

class ActionGoToPerson(Action):

    """
    DO NOT DELETE THIS. PASTE THIS IN FOR EVERY NEW OBJECT THAT WILL BE STORED IN A SET/DICTIONARY.
    THIS IS ESSENTIAL FOR MAKING SURE THE PROGRAM PERFORMS EXACTLY THE SAME EVERY TIME!

    assert(false) WILL CRASH THE PROGRAM IF YOU ATTEMPT TO PUT THIS OBJECT INTO A SET/DICT WITHOUT FIRST MODIFYING THE FUNCTION.
    THIS IS DONE ON PURPOSE TO PREVENT YOU FROM ACCIDENTALLY LEAKING NON-DETERMINISM INTO THE PROGRAM.
    SPEAK TO ME (TOM) AND I WILL EXPLAIN WHAT TO DO.
    """
    def __hash__(self):
        assert(False)

    def __init__(self, target_person_id):
        self.target_person_id = target_person_id
        self.person_location = None



    """
    Returns a list of prerequisites that must be satisfied in order to complete the action.

    Note the order of these prerequisites reflects the order of their potential actions that need
    to be completed for this action to be possible to do. Therefore order it appropriately.
    Note the action may not necessarily be executed if all the prerequisites are true.
    The prerequisites are used in the decision making process, however the optional
    method pre_begin_checks returns the final check before the action is executed in case new information
    is is revealed.
    """

    def get_prerequisites(self):
        return [ai.humanai.prerequisites.prerequisiteknowspersonlocation.PrerequisiteKnowsPersonLocation(self.target_person_id)]

    """
    The estimated cost of this action.
    This occurs during the decision making process of a action tree.
    For extra accuracy, use data from prerequisites.
    """

    def get_costs(self, human):
        return 0

    """
    Returns true/false if the action should proceed.
    Optional final checks that occur prior to the action starting (i.e. action is currently in a action tree).
    """

    def pre_begin_checks(self, human):
        return True

    """
    This is called once when the action begins.
    """

    def begin(self, human):
        self.person_location = ai.humanai.prerequisites.prerequisiteknowspersonlocation.PrerequisiteKnowsPersonLocation(self.target_person_id).get_data(human)
        human.find(self.person_location)
        pass

    """
    Called every tick while the action has begun and not completed yet.
    Returns True/False to indicate if an error occurs.
    """

    def tick(self, human):
        # if we now know the person to have changed location, fail
        if human.knowledge_people_locations.get_person_location(self.target_person_id) != self.person_location:
            return False
        human.step_towards_route()
        return True

    """
    Returns true/false to indicate whether the action is complete or not.
    Called every tick before tick() is executed.    
    """

    def is_complete(self, human):
        # also complete if we run into person in our travels
        if human.knowledge_people_locations.get_person_location(self.target_person_id) != self.person_location:
            human.route = []
            return True
        return human.arrived_at_location()

    def __str__(self):
        return "Going to person %s" % self.target_person_id
