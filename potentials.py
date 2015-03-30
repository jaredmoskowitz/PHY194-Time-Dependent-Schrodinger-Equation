import numpy as np
import matplotlib.pyplot as plt

def infiniteSquareWell(x):
    if(x<0 or x > 1):
        return np.inf
    return 0

def triangularWell(x):
    return abs(x)

def flatWell(x):
    return 0

def makePotentialBarrier(offset, width, height):
    return lambda x: (x > offset and x < (offset+width))*height

def plot(waveFunction, deltaX):
    #If waveFunction is 1d array
    plt.plot([deltaX*i for i in range(waveFunction.shape[0])], [i.real for i in waveFunction], label="Real")
    plt.plot([deltaX*i for i in range(waveFunction.shape[0])], [i.imag for i in waveFunction], label="Imaginary")
    legend = plt.legend(loc='upper right', shadow=True, fontsize='x-large')

    plt.show()

a=np.array([complex(np.sin(i/100.0), np.cos(i/100.0)) for i in range(100)])
plot(a, .1)

