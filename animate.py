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
potentialData = {'name':'Triangular','x_offset':0, 'a':10, 'b':10}
params={'potential':potential}
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

def updatePotential():
    potential = potentials.generatePotential(potentialData['name'], 
                                             potentialData['x_offset'],
                                             potentialData['a'], 
                                             potentialData['b'])
    potPlot.set_ydata([potential(x) if potential(x) != np.inf else 100 for x in xData])
    params['potential']=potential
    
def setPotentialName(potentialName):
    print "Changing??"
    potentialData['name'] = potentialName
    updatePotential()
    
def setPotentialOffset(val):
    potentialData['x_offset']=val
    updatePotential()
    
def setPotentialA(val):
    potentialData['a']=val
    updatePotential()
    
def setPotentialB(val):
    potentialData['b']=val
    updatePotential()
 
def setMethod(methodName):
    if(methodName == "Crank Nicolson"):
        method = schrodinger.crankNicolsonMethod
    else:
        method = schrodinger.naiveMethod

def setWaveOffset(val):
    i
def setWaveMomentum(val):
    i
def setWaveDeviation(val):
    i
guiAxes = plt.axes([0.05, 0.7, 0.2, 0.15])
guiAxes.set_title("Potential:", loc="left")
potentialChooser = widgets.RadioButtons(guiAxes, potentials.potentialNames)
potentialChooser.on_clicked(setPotentialName)

guiAxes = plt.axes([0.05, 0.6, 0.2, 0.05])
guiAxes.set_title("X-Offset", loc="left")
xOffsetChooser = widgets.Slider(guiAxes, "", -20, 20, 0)
xOffsetChooser.on_changed(setPotentialOffset)

guiAxes = plt.axes([0.05, 0.5, 0.2, 0.05])
guiAxes.set_title("A", loc="left")
aChooser = widgets.Slider(guiAxes, "", -20, 20, 10)
aChooser.on_changed(setPotentialA)


guiAxes = plt.axes([0.05, 0.4, 0.2, 0.05])
guiAxes.set_title("B", loc="left")
bChooser = widgets.Slider(guiAxes, "", -20, 20, 10)
bChooser.on_changed(setPotentialB)

guiAxes = plt.axes([0.05, 0.4, 0.2, 0.05])
guiAxes.set_title("B", loc="left")
bChooser = widgets.Slider(guiAxes, "", -20, 20, 10)
bChooser.on_changed(setPotentialB)

guiAxes = plt.axes([0.75, 0.7, 0.2, 0.15])
guiAxes.set_title("Method", loc="left")
methodChooser = widgets.RadioButtons(guiAxes, [r"""$Na\ddot ive\ Method$""", r"""$Crank\ Nicolson$"""])
methodChooser.on_clicked(setMethod)

guiAxes = plt.axes([0.75, 0.6, 0.2, 0.05])
guiAxes.set_title("Wave Packet Offset", loc="left")
waveOffsetChooser = widgets.Slider(guiAxes, "", -20, 20, 0)
waveOffsetChooser.on_changed(setWaveOffset)


guiAxes = plt.axes([0.75, 0.5, 0.2, 0.05])
guiAxes.set_title("Wave Momentum", loc="left")
waveMomentumChooser = widgets.Slider(guiAxes, "", -5, 5, 0)
waveMomentumChooser.on_changed(setWaveMomentum)

guiAxes = plt.axes([0.75, 0.4, 0.2, 0.05])
guiAxes.set_title("Wave Deviation", loc="left")
waveDeviationChooser = widgets.Slider(guiAxes, "", 0.01, .9, 0.4)
waveDeviationChooser.on_changed(setWaveDeviation)



def animate(j, params):
    global waveFunction
    waveFunction = schrodinger.naiveMethod(waveFunction, potential)
    print params['potential'](10)
    realPlot.set_ydata([i.real for i in waveFunction])
    imPlot  .set_ydata([i.imag for i in waveFunction])
    probPlot.set_ydata([abs(i) for i in waveFunction])


if __name__ == "__main__":
    print(params['potential'](10))
    anim = animation.FuncAnimation(figure, animate, fargs=(params,))
    
    #animate(1)
    plt.show()
