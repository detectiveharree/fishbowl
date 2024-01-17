from ai.need import NEED_TYPE
from ai.humanai.needs.needsocial.needsocial import NeedSocial

from ai.humanai.task.taskinitiateinteraction import TaskInitiateInteraction
from ai.humanai.relationships.interaction.interactionfighting.interactionfightbrawltargeted import InteractionFightBrawlTargeted
from ai.humanai.relationships.interaction.interaction import ANGER_REASON
import logging

# anger is a emotion between 0 and 100, this factor will increase it by a fixed constant
# to essentially make the anger swings more extreme and thus a higher chance of it being picked
ANGER_FACTOR = 1

class NeedSocialAnger(NeedSocial):

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
        super().__init__(NEED_TYPE.ANGER) # ALWAYS CALL PARENT CONSTRUCTOR
        self.target_id_and_reason = None


    """
    Each person will tick
    """
    def tick(self, human):
        self.need_level = (human.emotions.anger.value.get()) * ANGER_FACTOR
        if self.need_level <= self.minimum_level_for_switch():
            self.target_id_and_reason = None


    """
    Called when this need is the highest out of all of needs 
    """
    def get_task(self, human):

        if self.target_id_and_reason is not None:
            if human.body.health.get() >= 100:
                target_id, reason = self.target_id_and_reason
                return TaskInitiateInteraction(InteractionFightBrawlTargeted(human, target_id, True, 80, reason), human)
        # if not angry at anyone in particular, convert anger to frustration

        human.emotions.frustration.value.set(human.emotions.anger.value.get())
        return None