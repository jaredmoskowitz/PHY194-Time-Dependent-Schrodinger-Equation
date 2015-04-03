def triangularWell(x):
    return abs(x)

def flatWell(x):
    return 0

def makeInfiniteSquareWell(offset, width):
    return lambda x: np.inf if (x<offset or x > offset+width) else 0

def makePotentialBarrier(offset, width, height):
    return lambda x: (x > offset and x < (offset+width))*height
