from ai.humanai.relationships.attributes.racepresets.racepreset import RacePreset, RACE_PRESET_TYPE


class RacePresetDefault(RacePreset):


    """
    Returns the enum race preset type
    """
    def get_preset_type(self):
        return RACE_PRESET_TYPE.DEFAULT