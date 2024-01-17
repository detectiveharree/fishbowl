from abc import ABC, abstractmethod
from ai.humanai.relationships.attributes.attributes import BoundedNumber
from ai.need import NEED_TYPE

MAX_EMOTION = 100




"""
Emotion base class.
"""
class Emotion(ABC):


    def __init__(self):
        self.value = BoundedNumber(0, 0, MAX_EMOTION)


    @abstractmethod
    def change(self, human, delta):
        ...

class FrustrationEmotion(Emotion):

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
        super().__init__()

    def change(self, human, delta, ):
        print("Do not use this version of change. Use the other one, which contains the target id")
        assert(False)

    def change(self, human, delta, reason):
        # an act that makes a person angry is only effected by neuroticism/neuroticism
        # we might think that disagreeable people are more angry
        # but it is only true that disagreeable people engage in behaviour that makes
        # them more likely to engage in events that make them angry
        # i.e. disagreeable people insult and bully (which prompts retaliation which frustrations them)
        # but a person is only more likely to be angry the more neurotic/less confident they are
        self.value.set(self.value.get() + (delta * (human.personality.neuroticism.value+1)))

        if delta > 0:
            human.needs[NEED_TYPE.FRUSTRATION].reason = reason


class AngerEmotion(Emotion):

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
        super().__init__()

    def change(self, human, delta, ):
        print("Do not use this version of change. Use the other one, which contains the target id")
        assert(False)


    def change(self, human, delta, target_id_and_reason):
        self.value.set(self.value.get() + (delta *
                                           (human.personality.neuroticism.value+1) *
                                           (human.personality.carelessness.value+1)))
        if delta > 0:
            target_id, reason = target_id_and_reason
            human.needs[NEED_TYPE.ANGER].target_id_and_reason = target_id_and_reason
            assert(target_id != human.id_number)

class FearEmotion(Emotion):

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
        super().__init__()

    def change(self, human, delta):
        # (as frustration)
        self.value.set(self.value.get() + (delta * (human.personality.neuroticism.value+1)))



class LonelinessEmotion(Emotion):

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
        super().__init__()

    def change(self, human, delta):
        # for those with social < -0.75 it ticks up by none, for those > -0.75 it ticks up by increasing amounts

        # this is necessary otherwise we'll only get positive values
        if human.personality.social.value <= -0.75:
            return

        self.value.set(self.value.get() + (delta * (human.personality.social.value + 0.76)))

class LustEmotion(Emotion):

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
        super().__init__()

    def change(self, human, delta):
        # lust would tick up as loneliness would, but by some combination of social and carelessness

        # this is necessary otherwise we'll only get positive values
        if human.personality.social.value <= -0.75:
            return

        self.value.set(self.value.get() + (delta * 1.5 * (human.personality.carelessness.value + 0.76)))



class HappinessEmotion(Emotion):

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
        super().__init__()

    def change(self, human, delta):
        # neurotic people experience more extreme changes to happiness
        self.value.set(self.value.get() + (delta * (human.personality.neuroticism.value + 1)))


"""
FILL IN HERE
"""
class EmotionAttributes():

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
        self.frustration = FrustrationEmotion()
        self.fear = FearEmotion()
        self.loneliness = LonelinessEmotion()
        self.lust = LustEmotion()
        self.happiness  = HappinessEmotion()
        self.anger  = AngerEmotion()

    def to_string(self):
        output = f'Frustration: {round(self.frustration.value.get(),2)}, Anger: {round(self.anger.value.get(),2)}, Fear: {round(self.fear.value.get(),2)}, Loneliness: {round(self.loneliness.value.get(),2)}, Lust: {round(self.lust.value.get(),2)}, Happiness: {round(self.happiness.value.get(),2)}'
        return output