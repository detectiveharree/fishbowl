
from ai.humanai.relationships.attributes.personality import PersonalityAttributes
from enum import Enum

class HumanState(Enum):
    AWAKE = 1
    SLEEPING = 2
    INCAPACITATED = 3
    DEAD = 4

class HEALTH_CHANGE_TYPE(Enum):
    HEAL = 1
    FIGHT = 2
    STARVE = 3
    THIRST = 4


class HumanBase(object):

    def __init__(self, id_number, location = None):
        self.id_number = id_number
        self.location = location
        self.personality_attributes = PersonalityAttributes()
