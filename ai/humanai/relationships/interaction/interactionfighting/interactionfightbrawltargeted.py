from ai.humanai.relationships.interaction.interactionfighting.interactionfightbrawl import InteractionFightBrawl




class InteractionFightBrawlTargeted(InteractionFightBrawl):

    """
    DO NOT DELETE THIS. PASTE THIS IN FOR EVERY NEW OBJECT THAT WILL BE STORED IN A SET/DICTIONARY.
    THIS IS ESSENTIAL FOR MAKING SURE THE PROGRAM PERFORMS EXACTLY THE SAME EVERY TIME!

    assert(false) WILL CRASH THE PROGRAM IF YOU ATTEMPT TO PUT THIS OBJECT INTO A SET/DICT WITHOUT FIRST MODIFYING THE FUNCTION.
    THIS IS DONE ON PURPOSE TO PREVENT YOU FROM ACCIDENTALLY LEAKING NON-DETERMINISM INTO THE PROGRAM.
    SPEAK TO ME (TOM) AND I WILL EXPLAIN WHAT TO DO.
    """
    def __hash__(self):
        assert(False)



    def __init__(self, initiator, enemy_id, unarmed, damage_requirement, brawl_reason):
        super().__init__(initiator, unarmed, damage_requirement, brawl_reason)
        self.enemy_id = enemy_id


    """
    For cases when we are looking for person outside of a building.
    Returns a factor to multiply target score on based by their distance.
    Return -1 to indicate too far and skip this person.
    """
    def target_distance_score_factor(self, distance):
        # constant i.e. don't take distance into account
        return 1

    """
    Return true/false to indicate whether the person would like to join the interaction.
    This is a static method therefore you cannot use self i.e. data cannot be accessed from this Interaction class
    """
    def to_string(self):
        if len(self.active_participants) <= 1:
            return "%s targeting participant (%s) in building %s because %s" % (self.initiator.id_number, self.get_interaction_type(), self.initiator.current_building, self.brawl_reason)
        return "%s (%s) targeted and interacting with %s (%s) (%s) in building %s because %s" % (self.initiator.id_number, self.initiator.body.gender,
                                                               self.participant.id_number, self.participant.body.gender,
                                                                self.get_interaction_type(),
                                                               self.initiator.current_building, self.brawl_reason)


    """
    Returns a id of a person to look for, for this current interaction.
    This method will be called multiple times as the person moves towards their target,
    so return new people as new information is observed.

    I.e. pick one person to talk, as they move they see another closer person.
    Choose to interact with the other person instead.

    Default: finds person with closest location to initiator.
    RETURN A LIST NOT A SET
    """

    def calculate_interaction_targets(self, initiator):
        return [self.enemy_id]

