import numpy as np

def infiniteSquareWell(x):
    if(x<0 || x > 1):
        return np.inf
    return 0

def triangularWell(x):
    return abs(x)

def flatWell(x):
    return 0
