import numpy as np
import matplotlib.pyplot as plt
from matplotlib import animation
import helpers, schrodinger, time

length = schrodinger.totalSteps

figure = plt.figure()
axes   = plt.axes(xlim=schrodinger.boundaryConditions, ylim=(-2, 10))

realPlot, = axes.plot([], [], 'r',  label="Real")
imPlot,   = axes.plot([], [], 'b',  label="Imaginary")
probPlot, = axes.plot([], [], 'k-', label="Probablility", linewidth=2)
potPlot,  = axes.plot([], [], 'k:', label="Potential")
legend = plt.legend(loc='upper right', shadow=True, fontsize='x-large')


potential = helpers.flatWell

boundaryConditions = (-45, 45)

currentWaveFunction = np.array(schrodinger.generateWavePacket( 0, .5, .5))
print(currentWaveFunction[:10])
def init():
    realPlot.set_data([],[])
    imPlot  .set_data([],[])
    probPlot.set_data([],[])
    potPlot .set_data([],[])
    return (realPlot, imPlot, probPlot, potPlot)

def animate(i):
    global currentWaveFunction
    currentWaveFunction = schrodinger.finiteDifferenceEquation(currentWaveFunction, potential)
    print currentWaveFunction[:10]
    time.sleep(1)
    length=80
    xPositions = [schrodinger.dx*i - 45 for i in range(len(currentWaveFunction))]
    
    
    realPlot.set_data(xPositions, [i.real for i in currentWaveFunction])
    imPlot.set_data(xPositions, [i.imag for i in currentWaveFunction])
    probPlot.set_data(xPositions, [abs(i) for i in currentWaveFunction])
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
                               frames=1, interval=2, blit=True)

    plt.show()


