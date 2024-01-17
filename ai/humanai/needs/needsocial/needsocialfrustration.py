from ai.need import NEED_TYPE
from ai.humanai.needs.needsocial.needsocial import NeedSocial

from ai.humanai.task.taskinitiateinteraction import TaskInitiateInteraction
from ai.humanai.relationships.interaction.interactionfighting.interactionfightbrawl import InteractionFightBrawl
from ai.humanai.relationships.interaction.interactionsocialise.interactioninsult import InteractionInsult
import numpy as np
from ai.humanai.relationships.interaction.interaction import ANGER_REASON

class NeedSocialFrustration(NeedSocial):

    """
    DO NOT DELETE THIS. PASTE THIS IN FOR EVERY NEW OBJECT THAT WILL BE STORED IN A SET/DICTIONARY.
    THIS IS ESSENTIAL FOR MAKING SURE THE PROGRAM PERFORMS EXACTLY THE SAME EVERY TIME!

    assert(false) WILL CRASH THE PROGRAM IF YOU ATTEMPT TO PUT THIS OBJECT INTO A SET/DICT WITHOUT FIRST MODIFYING THE FUNCTION.
    THIS IS DONE ON PURPOSE TO PREVENT YOU FROM ACCIDENTALLY LEAKING NON-DETERMINISM INTO THE PROGRAM.
    SPEAK TO ME (TOM) AND I WILL EXPLAIN WHAT TO DO.
    """
    def __hash__(self):
        assert(False)


    def __init__(self):
        super().__init__(NEED_TYPE.FRUSTRATION) # ALWAYS CALL PARENT CONSTRUCTOR
        self.reason = None

    """
    Each person will tick
    """
    def tick(self, human):
        self.need_level = 0
        self.need_level = (human.emotions.frustration.value.get())

        if self.need_level <= self.minimum_level_for_switch():
            self.reason = None

    """
    Called when this need is the highest out of all of needs 
    """
    def get_task(self, human):
        # some logic to determine which task is appropriate for this person

        """
        IF over 80 in frustration then fight else insult
        """
        if self.need_level < 80 or human.body.health.get() < 100:
            return TaskInitiateInteraction(InteractionInsult(human, self.reason), human)


        neurotic_agreeble = (human.personality.neuroticism.as_percentage() + (1 - human.personality.agreeable.as_percentage())) / 2
        neurotic_agreeable_rand = np.random.normal(0, neurotic_agreeble) / 2

        # relatively low neurotism and agreeablness
        if -0.4 < neurotic_agreeable_rand < 0.4:
            return TaskInitiateInteraction(InteractionInsult(human, self.reason), human)

        # else engage unarmed brawl to 80 health
        return TaskInitiateInteraction(InteractionFightBrawl(human, True, 80, self.reason), human)

