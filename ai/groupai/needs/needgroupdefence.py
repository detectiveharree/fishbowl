from ai.groupai.needs.needgroup import NeedGroup, GROUP_NEED_TYPE
from items.itemresources.itemresource import ResourceType
from gameworld.cell.cellbuilding.cellbuildinghouse import BuildingHouse
import global_params
import random
import ai.pathfindingbuilding
from gameworld.cell.cellbuilding.cellbuilding import BUILDING_TYPE
import logging

class NeedGroupDefence(NeedGroup):

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
        super().__init__(GROUP_NEED_TYPE.DEFENCE) # ALWAYS CALL PARENT CONSTRUCTOR
        self.need_level = 0
        # LEAK HERE
        self.threats = {} # dict of threats

    """
    Register a incoming enemy army
    """
    def register_campaign_threat(self, group, campaign):
        if not self.have_registered_threat(campaign):
            logging.info("%s has noticed %s's threat %s" % (group.id_number, campaign.original_group.id_number, campaign.get_campaign_type()))
            threat_level = campaign.get_defence_type().get_campaign_threat_score(group, campaign)
            self.threats[campaign] = threat_level
            self.need_level += threat_level

    """
    Have we already registered a certain army
    """
    def have_registered_threat(self, campaign):
        return campaign in self.threats.keys()

    """
    Called once a day.
    """
    def get_task(self, group, adjusted_need_level):

        if self.need_level > 0:
            for campaign, need_level in self.threats.items():
                if need_level != 0:
                    campaign.get_defence_type().get_campaign_response(group, campaign)
                    self.threats[campaign] = 0
                    self.need_level -= need_level

        return []
