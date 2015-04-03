import numpy as np
import matplotlib.pyplot as plt
from matplotlib import animation
import time

def triangularWell(x):
    return abs(x)

def flatWell(x):
    return 0

def makeInfiniteSquareWell(offset, width):
    return lambda x: np.inf if (x<offset or x > offset+width) else 0

def makePotentialBarrier(offset, width, height):
    return lambda x: (x > offset and x < (offset+width))*height

def generateWavePacket( x0, k0, sigma):
    return lambda x: np.exp(.25*(x-x0)*complex((x0-x)*sigma ** 2, 4*k0)*np.sqrt(np.pi)*sigma/np.sqrt(np.sqrt(2)*np.pi ** 3/2 * sigma))

psi = generateWavePacket( 0, .5, .5)
dt = 0.08
dx = dt

boundaryConditions = (-45, 45)
length = (boundaryConditions[1] - boundaryConditions[0])/dt

figure = plt.figure()
axes   = plt.axes(xlim=boundaryConditions, ylim=(-2, 10))

realPlot, = axes.plot([], [], 'r',  label="Real")
imPlot,   = axes.plot([], [], 'b',  label="Imaginary")
probPlot, = axes.plot([], [], 'k-', label="Probablility", linewidth=2)
potPlot,  = axes.plot([], [], 'k:', label="Potential")
legend = plt.legend(loc='upper right', shadow=True, fontsize='x-large')


potential = makeInfiniteSquareWell(-10, 20)

boundaryConditions = (-45, 45)


def init():
    realPlot.set_data([],[])
    imPlot  .set_data([],[])
    probPlot.set_data([],[])
    potPlot .set_data([],[])
    return (realPlot, imPlot, probPlot, potPlot)

def animate(i):
    psi=generateWavePacket(0,1,1/(i/50.0 + 1))
    waveFunction=np.array([psi((i-40.0)) for i in range(80)])
    deltaX=1
    length=80
    xPositions = [deltaX*i - 40 for i in range(length)]
    
    realPlot.set_data(xPositions, [i.real for i in waveFunction])
    imPlot.set_data(xPositions, [i.imag for i in waveFunction])
    probPlot.set_data(xPositions, [abs(i) for i in waveFunction])
    potPlot.set_data(xPositions, [potential(x) if potential(x) != np.inf else 100 for x in xPositions])
    return (realPlot, imPlot, probPlot, potPlot)
    
#def plot(waveFunction, potential, deltaX):
    ##If waveFunction is 1d array
    #length = waveFunction.shape[0]
    #xPositions = [deltaX*i - 40 for i in range(waveFunction.shape[0])]
    #plt.ylim([-2 , 10])
    #plt.xlim([-40,40])
    #plt.plot(xPositions, [i.real for i in waveFunction], label="Real")
    #plt.plot(xPositions, [i.imag for i in waveFunction], label="Imaginary")
    #plt.plot(xPositions, [abs(i) for i in waveFunction], label="Probablility")
    #plt.plot(xPositions, [potential(x) if potential(x) != np.inf else 100 for x in xPositions], label="Potential")

    #plt.show()

if __name__ == "__main__":
    anim = animation.FuncAnimation(figure, animate, init_func=init,
                               frames=1000, interval=2, blit=True)

    plt.show()


