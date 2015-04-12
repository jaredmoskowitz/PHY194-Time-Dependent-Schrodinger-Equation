''''
        potentials.py

        Jared Moskowitz, Chase Crumbagh, & Nolan Hawkins
        04/08/15

        This file contains python function definitions for
        potentials.
        
        Functions begining with "generate" return a function
        pointer to a potential function generated with the
        arguments

'''
import numpy as np

potentialNames = ["Flat",
                  "Triangular",
                  "Infinite Square",
                  "Step",
                  "Barrier",
                  "Crystal",
                  "Harmonic"]


'''
generates a potential for given parameters
parameters
        name - name of potential (see top of file)
        offset - x offset
        width, height, and slope are parameters used in 
            some of the potential generator functions
'''
def generatePotential(name, offset, width, height, slope):
    vType = potentialNames.index(name)

    if (vType == 0):
        return flatWell
    elif (vType == 1):
        return generateTriangularWell(offset, slope)
    elif (vType == 2):
        return generateFiniteSquareWell(offset, width)
    elif (vType == 3):
        return generateStep(offset, height)
    elif (vType == 4):
        return generatePotentialBarrier(offset, width, height)
    elif (vType == 5):
        return generateCrystal(offset, width, height)
    elif (vType == 6):
        return generateHarmonicWell(offset, slope)

    return None

def flatWell(x):
    return 0

# Fun Lambda Functions! 

def generateTriangularWell(offset, slope):
    return lambda x: abs(x - offset)*slope

def generateFiniteSquareWell(offset, width):
    return lambda x: 100 if (x<offset-width/2 or x > offset+width/2) else 0

def generateStep(offset, height):
    return lambda x: height if (x > offset) else 0

def generatePotentialBarrier(offset, width, height):
    return lambda x: (x > offset and x < (offset+width))*height

def generateHarmonicWell(offset, slope):
    return lambda x: slope/50*(x-offset)**2

def generateCrystal(offset, width, height):
    return lambda x: 0 if (x<offset or (x/width)%2 < 1) else height

