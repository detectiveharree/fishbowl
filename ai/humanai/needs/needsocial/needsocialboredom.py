from ai.need import NEED_TYPE
from ai.humanai.needs.needsocial.needsocial import NeedSocial
from ai.humanai.task.taskinitiateinteraction import TaskInitiateInteraction
from ai.humanai.task.taskwander import TaskWander
from ai.humanai.relationships.interaction.interactionsocialise.interactionsocialisebanter import InteractionBanter
from ai.humanai.relationships.interaction.interactionsocialise.interactionsocialisechat import InteractionChat
from ai.humanai.relationships.interaction.interactionsocialise.interactionsocialiseromance import InteractionRomance
import numpy as np


class NeedSocialBoredom(NeedSocial):

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
        super().__init__(NEED_TYPE.BOREDOM) # ALWAYS CALL PARENT CONSTRUCTOR

    """
    Each person will tick
    """
    def tick(self, human):
        # boredom is the absence of any other emotion, so we increment the value by the inverse of the traits

        """
        Absence of frustration, sad, fear <= the lower these, the higher the boredom score.
        Loneliness - the higher the more bored.
        Happiness - the lower the more bored.
        """

        frustration = human.emotions.frustration.value.get()
        fear = human.emotions.fear.value.get()
        happiness = human.emotions.happiness.value.get()
        loneliness = human.emotions.loneliness.value.get()

        happiness *= -1
        happiness += 100
        frustration *= -1
        frustration += 100
        fear *= -1
        fear += 100

        self.need_level = (frustration + fear + loneliness + (happiness * 8)) / 11




    has_wondered = False

    # def minimum_level_for_switch(self):
    #     return 100


    """
    Called when this need is the highest out of all of needs 
    """
    def get_task(self, human):
        # some logic to determine which task is appropriate for this person
        if not self.has_wondered:
            exploration_personality_mean = (abs(human.personality.social.value-1))
            rand = np.random.normal(exploration_personality_mean, 0.8)
            if rand > 1.4:
                self.has_wondered = True
                return TaskWander(human)
                # if this if statement is satisfied, we need to call the explore/walk function
        # return TaskInitiateInteraction(InteractionInsult(human), human)

        neurotic_rand = np.random.normal(0, human.personality.neuroticism.as_percentage() / 2)
        agreeable_rand = np.random.normal(0, (1 - human.personality.agreeable.as_percentage()) / 2)


        #return TaskInitiateInteraction(InteractionChat(human), human)
        # return TaskInitiateInteraction(InteractionRomance(human), human)

        # relatively low neurotism
        if -0.3 < neurotic_rand < 0.3:
            # most agreeable just chat
            if -0.2 < agreeable_rand < 0.2:
                return TaskInitiateInteraction(InteractionChat(human), human)
            # sligtly less agreeable banter
            else:
                return TaskInitiateInteraction(InteractionBanter(human), human)

        # high neutorism
        else:
            return TaskInitiateInteraction(InteractionRomance(human), human)




# self.need_level = 0
# # all lustful people will want intimacy, so increment irrespective of personality
# self.need_level += (human.emotions.lust.value.get())
# # lonely people will want intimacy if they are extraverted/curious, so increment by average of both
# self.need_level += (human.emotions.loneliness.value.get()) * (human.personality.social.value+1)/2
# self.need_level *= 3