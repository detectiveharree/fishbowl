from ai.humanai.relationships.attributes.personality import PersonalityAttributes
from humanbase import HumanBase, HumanState
from ai.humanai.relationships.interactionmemory import InteractionMemoryCache
from ai.humanai.relationships.attributes.body.body import GENDER_TYPE
import guiwindow

"""
The knowledge of a person
"""
class KnowledgeHuman(HumanBase):

    """
    DO NOT DELETE THIS. PASTE THIS IN FOR EVERY NEW OBJECT THAT WILL BE STORED IN A SET/DICTIONARY.
    THIS IS ESSENTIAL FOR MAKING SURE THE PROGRAM PERFORMS EXACTLY THE SAME EVERY TIME!

    assert(false) WILL CRASH THE PROGRAM IF YOU ATTEMPT TO PUT THIS OBJECT INTO A SET/DICT WITHOUT FIRST MODIFYING THE FUNCTION.
    THIS IS DONE ON PURPOSE TO PREVENT YOU FROM ACCIDENTALLY LEAKING NON-DETERMINISM INTO THE PROGRAM.
    SPEAK TO ME (TOM) AND I WILL EXPLAIN WHAT TO DO.
    """
    def __hash__(self):
        assert(False)


    def __init__(self, person_id):
        super().__init__(person_id) # ALWAYS CALL PARENT CONSTRUCTOR

        """
        A bit cheaty but automatically gain knowledge of persons personality when they are first discovered of
        as an optimisation.
        
        Can be justified as:
        You either discover a person by seeing them or being told of them.
        It would make sense that you gain insight into their personality this way.
        """
        self.gender = GENDER_TYPE.MALE
        self.age = 40

        if person_id in guiwindow.WORLD_INSTANCE.humanDict.keys():
            self.personality_attributes = guiwindow.WORLD_INSTANCE.humanDict[person_id].personality
            self.gender = guiwindow.WORLD_INSTANCE.humanDict[person_id].body.gender
            self.age = guiwindow.WORLD_INSTANCE.humanDict[person_id].body.age


        # container of interaction summaries
        self.interaction_memory_cache = InteractionMemoryCache()

        # believed group of person
        self.group_id = None
        self.state = HumanState.AWAKE

        # believed health of other person
        self.health = 100
        self.genetic_weight = 1 # only can be set once tbf
        self.strength = 1
        self.current_kit_rating = 1

        self.total_interactions = 0



