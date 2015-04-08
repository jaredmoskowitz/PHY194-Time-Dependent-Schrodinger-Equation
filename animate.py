import matplotlib
matplotlib.use('TkAgg')

import numpy as np
import matplotlib.pyplot as plt
from matplotlib import animation
from matplotlib import widgets
import potentials, schrodinger, time

# Get some values from schrodinger

totalSteps = schrodinger.totalSteps

boundaryConditions = schrodinger.boundaryConditions
dx = schrodinger.dx
dt = schrodinger.dt


waveFunction = schrodinger.generateWavePacket(0,1.5,.5)

potential = potentials.generateTriangularWell(0, 0.005)
potentialData = {'x_offset':0, 'a':0.05, 'b':1}

# Initialize GUI stuff from matplotlib
figure, axes = plt.subplots()
#plt.subplot(211)
axes.set_xlim(schrodinger.boundaryConditions)
axes.set_ylim(-0.5, 1)
plt.subplots_adjust(left=0.3, right=0.7)


xData=[dx*i + boundaryConditions[0] for i in range(len(waveFunction))]
# Initialize plots of the real, complex, and probability of the wave function ...
#plt.subplot(211)
realPlot, = axes.plot(xData, xData, 'r',  label="Real")
imPlot,   = axes.plot(xData, xData, 'b',  label="Imaginary")
probPlot, = axes.plot(xData, xData, 'k-', label="Probablility", linewidth=2)
#  And the plot of the potential
potPlot,  = axes.plot(xData, [potential(x) if potential(x) != np.inf else 100 for x in xData], 'k:', label="Potential")
legend = axes.legend(loc='upper right', shadow=True, fontsize='x-large')


guiAxes= plt.axes([0.05, 0.7, 0.2, 0.15], axisbg='lightgoldenrodyellow')
potentialChooser = widgets.RadioButtons(guiAxes, potentials.potentialNames)

def setPotential(potentialName):
    print "Changing??"
    potential = potentials.generatePotential(potentialName, 
                                             potentialData['x_offset'],
                                             potentialData['a'], 
                                             potentialData['b'])
    print potential(10)
    potPlot.set_ydata ([potential(x) if potential(x) != np.inf else 100 for x in xData])

potentialChooser.on_clicked(setPotential)



print(waveFunction[:10])



def animate(j):
    global waveFunction
    print potential(10)
    waveFunction = schrodinger.finiteDifferenceEquation(waveFunction, potential)

    realPlot.set_ydata([i.real for i in waveFunction])
    imPlot  .set_ydata([i.imag for i in waveFunction])
    probPlot.set_ydata([abs(i) for i in waveFunction])


if __name__ == "__main__":
    anim = animation.FuncAnimation(figure, animate)
    
    #animate(1)
    plt.show()
