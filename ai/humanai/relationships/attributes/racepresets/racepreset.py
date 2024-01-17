from enum import Enum
from abc import ABC, abstractmethod
from ai.humanai.relationships.attributes.personality import PersonalityAttributes
from ai.humanai.relationships.attributes.body.body import GENDER_TYPE
import numpy as np
from random import randint
from ai.humanai.relationships.attributes.body.body import Body


class RACE_PRESET_TYPE(Enum):
    DEFAULT = 1
    ARABIAN = 2
    AFRICAN = 3

    def __repr__(self):
        return self.name



class RacePreset():

    def __init__(self):
        pass

    """
    Returns the enum race preset type
    """
    @abstractmethod
    def get_preset_type(self):
        ...

    """
    Gets standard personality
    """
    def get_standard_personality(self, gender):
        return PersonalityAttributes(neuroticism=self.get_personality_standard_neuroticism(gender),
                                     charisma=self.get_personality_standard_charisma(gender),
                                     agreeableness=self.get_personality_standard_agreeableness(gender),
                                     social=self.get_personality_standard_socialness(gender),
                                     carelessness=self.get_personality_standard_carelessness(gender))

    """
    Gets standard body
    """
    def get_standard_body(self, gender):
        return Body(gender, genetic_strength=self.get_body_standard_strength(gender), genetic_speed=self.get_body_standard_speed(gender))

    def get_body_standard_strength(self, gender):
        if gender == GENDER_TYPE.MALE:
            return round(np.clip(np.random.normal(0.4, 0.2), 0, 1), 2)
        else:
            return round(np.clip(np.random.normal(0.2, 0.1), 0, 1), 2)


    def get_body_standard_speed(self, gender):
        if gender == GENDER_TYPE.FEMALE:
            return round(np.clip(np.random.normal(0.4, 0.2), 0, 1), 2)
        else:
            return round(np.clip(np.random.normal(0.3, 0.2), 0, 1), 2)


    """
    Gets standard neuroticism value for this race.
    Default: value the game was tuned for
    """
    def get_personality_standard_neuroticism(self, gender):
        if gender == GENDER_TYPE.MALE:
            rand = np.random.normal(0, 1)
            rand *= (0.72 / 1.65)
            rand -= 0.25
            return round(np.clip(rand, -1, 1), 2)
        else:
            rand = np.random.normal(0, 1)
            rand *= (0.72 / 1.65)
            rand -= 0.15
            return round(np.clip(rand, -1, 1), 2)

    """
    Gets standard agreeble value for this race.
    Default: value the game was tuned for
    """
    def get_personality_standard_agreeableness(self, gender):
        if gender == GENDER_TYPE.FEMALE:
            return round(np.clip(np.random.normal(0.4, 0.4), -1, 1), 2)
        else:
            return round(np.clip(np.random.uniform(-1, 1), -1, 1), 2)

    """
    Gets standard social value for this race.
    Default: value the game was tuned for
    """
    def get_personality_standard_socialness(self, gender):
        if gender == GENDER_TYPE.MALE:
            return round(np.clip(np.random.normal(0.3, 0.75), -1, 1), 2)
        else:
            return round(np.clip(np.random.normal(0.5, 0.75), -1, 1), 2)

    """
    Gets standard carelessness value for this race.
    Default: value the game was tuned for
    """
    def get_personality_standard_carelessness(self, gender):
        if gender == GENDER_TYPE.MALE:
            if randint(0, 100) < 35:
                return round(np.clip(np.random.uniform(-1, 0), -1, 1), 2)
            else:
                return round(np.clip(np.random.normal(0.5, 0.5), -1, 1), 2)
        else:
            if randint(0, 100) < 20:
                return round(np.clip(np.random.uniform(-1, 0), -1, 1), 2)
            else:
                return round(np.clip(np.random.normal(0.5, 0.5), -1, 1), 2)


    """
    Gets standard charisma value for this race.
    Default: value the game was tuned for
    """
    def get_personality_standard_charisma(self, gender):
        rand = randint(0, 100)
        if rand < 10:
            return round(np.clip(np.random.normal(0.9, 0.1), -1, 1), 2)
        elif rand < 30:
            return round(np.clip(np.random.normal(0.6, 0.2), -1, 1), 2)
        else:
            return round(np.clip(np.random.uniform(-1, 0.4), -1, 1), 2)


