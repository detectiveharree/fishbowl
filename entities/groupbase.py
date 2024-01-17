
from items.itemresources.itemresource import ResourceType, GROUP_BUFFER_FACTOR
from ai.groupai.bufferfactor.bufferfactorskill import BufferFactorSkill
from ai.humanai.skill import SKILL_TYPE
import global_params

from enum import Enum
from ai.groupai.knowledge.knowledgegroupinventoryshelf import KnowledgeGroupInventoryShelf


class GroupType(Enum):
    SETTLEMENT = 1  # i.e. the standard group
    CARAVAN = 2  # i.e. a group that moves around stockpile location moves with it
    RALLY_POINT = 3  # i.e. a group with a meeting point

    def __repr__(self):
        return self.name

class GroupBase(object):

    def __init__(self, id_number, group_type, stockpile_contents = { resource_type:0 for resource_type in list(ResourceType)}, stockpile_location=None, parent_group = None):
        self.id_number = id_number
        self.group_type = group_type
        self.parent_group = parent_group
        self.stockpile_location = stockpile_location
        self.buffer_factors = {GROUP_BUFFER_FACTOR.FOOD_HARVESTING: BufferFactorSkill(GROUP_BUFFER_FACTOR.FOOD_HARVESTING),
                               GROUP_BUFFER_FACTOR.WATER_HARVESTING:BufferFactorSkill(GROUP_BUFFER_FACTOR.WATER_HARVESTING),
                               GROUP_BUFFER_FACTOR.WOOD_HARVESTING:BufferFactorSkill(GROUP_BUFFER_FACTOR.WOOD_HARVESTING),
                               GROUP_BUFFER_FACTOR.BLACK_STEEL_HARVESTING:BufferFactorSkill(GROUP_BUFFER_FACTOR.BLACK_STEEL_HARVESTING),
                               GROUP_BUFFER_FACTOR.BRASS_HARVESTING:BufferFactorSkill(GROUP_BUFFER_FACTOR.BRASS_HARVESTING),
                               GROUP_BUFFER_FACTOR.BRONZE_HARVESTING:BufferFactorSkill(GROUP_BUFFER_FACTOR.BRONZE_HARVESTING),
                               GROUP_BUFFER_FACTOR.DARK_IRON_HARVESTING:BufferFactorSkill(GROUP_BUFFER_FACTOR.DARK_IRON_HARVESTING),
                               GROUP_BUFFER_FACTOR.IRON_HARVESTING:BufferFactorSkill(GROUP_BUFFER_FACTOR.IRON_HARVESTING),
                               GROUP_BUFFER_FACTOR.WHITE_STEEL_HARVESTING:BufferFactorSkill(GROUP_BUFFER_FACTOR.WHITE_STEEL_HARVESTING),
                               GROUP_BUFFER_FACTOR.STONE_HARVESTING:BufferFactorSkill(GROUP_BUFFER_FACTOR.STONE_HARVESTING),
                               GROUP_BUFFER_FACTOR.CRAFTING:BufferFactorSkill(GROUP_BUFFER_FACTOR.CRAFTING),
                               GROUP_BUFFER_FACTOR.BUILDING:BufferFactorSkill(GROUP_BUFFER_FACTOR.BUILDING)}

        #self.stockpile_contents = { resource_type:3600 for resource_type in list(ResourceType)}
        self.stockpile_contents = stockpile_contents

        """
        id to shelf for the specific person.
        ID -1 belongs to everyone.
        When someone leaves a group, there inventory shelf goes to everyone.
        """

        # members and demands
        self.members = set()
        self.member_ids = set()




