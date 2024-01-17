from ai.need import Need, NEED_TYPE


class NeedSocial(Need):

    def __init__(self, need_type):
        super().__init__(need_type) # ALWAYS CALL PARENT CONSTRUCTOR


    def minimum_level_for_switch(self):
        return 30