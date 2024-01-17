

class Opinions():

    def __init__(self):
        pass

    def get_n_least(self, valuesorteddict, number):
        return [(key, round(numb, 2)) for key, numb in valuesorteddict.items()[:number]]

    def get_n_most(self, valuesorteddict, number):
        return [(key, round(numb, 2)) for key, numb in valuesorteddict.items()[-number:][::-1]]

    def get_best(self, valuesorteddict):
        return valuesorteddict.keys()[-1]