from enum import Enum
import global_params


class SKILL_TYPE(Enum):



    FOOD_HARVESTING = 1
    WATER_HARVESTING = 2
    WOOD_HARVESTING = 3
    MINING = 4
    BUILDING = 5
    CRAFTING = 6

    def __repr__(self):
        return self.name