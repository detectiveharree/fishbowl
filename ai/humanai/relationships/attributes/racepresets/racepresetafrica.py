from ai.humanai.relationships.attributes.racepresets.racepreset import RacePreset, RACE_PRESET_TYPE


class RacePresetAfrica(RacePreset):


    """
    Returns the enum race preset type
    """
    def get_preset_type(self):
        return RACE_PRESET_TYPE.AFRICAN

    """
    Gets standard neuroticism value for this race.
    Default: value the game was tuned for
    """
    def get_personality_standard_neuroticism(self, gender):
        return 0.99

    """
    Gets standard agreeble value for this race.
    Default: value the game was tuned for
    """
    def get_personality_standard_agreeableness(self, gender):
        return -1