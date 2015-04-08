import numpy as np

potentialNames = ["Flat",
                  "Triangular",
                  "Infinite Square",
                  "Step", 
                  "Barrier",
                  "Crystal",
                  "Harmonic"]

def triangularWell(x):
    return abs(x)

def flatWell(x):
    return 0

def generateTriangularWell(offset, slope):
    return lambda x: abs(x - offset)*slope

def generateInfiniteSquareWell(offset, width):
    return lambda x: np.inf if (x<offset-width/2 or x > offset+width/2) else 0

def generateStep(offset, height):
    return lambda x: height if (x > offset) else 0

def generatePotentialBarrier(offset, width, height):
    return lambda x: (x > offset and x < (offset+width))*height

def generateHarmonicWell(offset, slope):
    return lambda x: slope*(x-offset)**2

def generateCrystal(offset, width, height):
    return lambda x: 0 if (x<offset or (x/width)%2 < 1) else height

def generatePotential(name, offset, a, b):
    vType = potentialNames.index(name)
    #print vType
    if (vType == 0):
        return flatWell
    elif (vType == 1):
        return generateTriangularWell(offset, a)
    elif (vType == 2):
        return generateInfiniteSquareWell(offset, a)
    elif (vType == 3):
        return generateStep(offset, a)
    elif (vType == 4):
        return generatePotentialBarrier(offset, a, b)
    elif (vType == 5):
        return generateCrystal(offset, a, b)
    elif (vType == 6):
        return generateHarmonicWell(offset, a)
    return None
