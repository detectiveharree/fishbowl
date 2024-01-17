from random import randint
import numpy as np

"""
* We need to find a better place for this list of functions *

Genetic attributes are:
- eye colour
- skin colour
- fatness
- geneticspeed
- geneticstrength
- height

There are a few cosmetic traits that aren't covered here:
- those traits are *not* genetic, they are just selected randomly (e.g. hair type, head type, etc.)
"""

"""
This function returns (as tuple):
- geneticeyecolour (list of eye colours you have in your genetics but don't show)
- eyecolour (your actual eye colour)
Logic:
- for geneticeyecolour, just join together parents' list
- for eyecolour, randomly pick from the child's geneticeyecolour, and with 1% probability, swap a random eye colour
"""
def get_child_attributes_eyecolour(parent1,parent2):
    genetic_eye_colour = parent1.body.geneticeyecolours + parent2.body.geneticeyecolours
    eyecolour = genetic_eye_colour[randint(0,len(genetic_eye_colour)-1)]
    if randint(0,100) == 0:
        eyecolour[randint(0,1)] = genetic_eye_colour[randint(0,len(genetic_eye_colour)-1)][0]

    return (genetic_eye_colour,eyecolour)

"""
This function returns (only):
- skincolour
Logic:
- for each shade, average the colours of the parents
"""
def get_child_attributes_skincolour(parent1,parent2):
    skincolour = []
    for i,shade in enumerate(parent1.body.skincolour):
        child_shade = (int((parent1.body.skincolour[i][0] + parent2.body.skincolour[i][0]) / 2),
                       int((parent1.body.skincolour[i][1] + parent2.body.skincolour[i][1]) / 2),
                       int((parent1.body.skincolour[i][2] + parent2.body.skincolour[i][2]) / 2),
                       int((parent1.body.skincolour[i][3] + parent2.body.skincolour[i][3]) / 2),
                       int((parent1.body.skincolour[i][4] + parent2.body.skincolour[i][4]) / 2),
                       )
        skincolour.append(child_shade)
    return skincolour

"""
This function returns (as boolean), whether the child is genetically fat
- True (fat)
- False (skinny)
Logic:
- if both fat/skinny : 90% chance of child being fat/skinny, else: 50% chance of being fat/skinny
"""
def get_child_attributes_fatness(parent1,parent2):
    if parent1.body.geneticfatness and parent2.body.geneticfatness:
        # both parents fat (90% probability of being fat)
        if randint(0,10) == 0:
            return False
        else:
            return True
    elif parent1.body.geneticfatness or parent2.body.geneticfatness:
        # one parent is fat (50% probability of being fat)
        if randint(0,1) == 0:
            return False
        else:
            return True
    else:
        # neither parent is fat (90% probability of being skinny)
        if randint(0,10) == 0:
            return True
        else:
            return False

"""
This function returns (as float):
- geneticspeed
Logic:
- average parent speed attributes, and sample from normal distribution with that mean
"""
def get_child_attributes_speed(parent1,parent2):
    mean_geneticspeed = (parent1.body.geneticspeed + parent2.body.geneticspeed)/2
    return max(0.1,np.random.normal(mean_geneticspeed,1))

"""
This function returns (as float):
- geneticstrength
Logic:
- (same as speed)
"""
def get_child_attributes_strength(parent1,parent2):
    mean_geneticstrength = (parent1.body.geneticstrength + parent2.body.geneticstrength)/2
    return max(0.1,np.random.normal(mean_geneticstrength,1))

"""
This function returns (as float):
- height
Logic:
- (same as speed)
"""
def get_child_attributes_height(parent1,parent2):
    mean_geneticstrength = (parent1.body.geneticstrength + parent2.body.geneticstrength)/2
    return max(0.1,np.random.normal(mean_geneticstrength,1))