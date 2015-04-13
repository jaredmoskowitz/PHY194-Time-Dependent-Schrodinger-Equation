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

potential = potentials.generateTriangularWell(0, 0.005)
potentialData = {'name':'Triangular','x_offset':0, 'width':10, 'height':.3, 'slope':.1}
initialWaveData = {'x_offset':0, 'momentum':1.5, 'deviation':.5}
params={
        'potential':potential,
        'method':schrodinger.naiveMethod,
        'waveFunction':schrodinger.generateWavePacket(0,1.5,.5),
        'paused':False,
        'periodicPotential':True
        }


# Initialize GUI stuff from matplotlib
figure, axes = plt.subplots(figsize=(12,6))
#plt.subplot(211)
axes.set_xlim(schrodinger.boundaryConditions)
axes.set_ylim(-0.5, 3)
plt.subplots_adjust(left=0.3, right=0.7)


xData=[dx*i + boundaryConditions[0] for i in range(len(params['waveFunction']))]
# Initialize plots of the real, complex, and probability of the wave function ...
#plt.subplot(211)
realPlot, = axes.plot(xData, xData, 'r',  label="Real")
imPlot,   = axes.plot(xData, xData, 'b',  label="Imaginary")
probPlot, = axes.plot(xData, xData, 'k-', label="Probablility", linewidth=2)
#  And the plot of the potential
potPlot,  = axes.plot(xData, [abs(potential(x)) for x in xData], 'k:', label="Potential")
legend = axes.legend(loc='upper right', shadow=True)

def updatePotential():
    potential = potentials.generatePotential(potentialData['name'], 
                                             potentialData['x_offset'],
                                             potentialData['width'], 
                                             potentialData['height'],
                                             potentialData['slope'])
    potPlot.set_ydata([abs(potential(x)) for x in xData])
    params['potential']=potential
    
def setPotentialName(potentialName):
    potentialData['name'] = potentialName
    updatePotential()
    
def setPotentialOffset(val):
    potentialData['x_offset']=val
    updatePotential()
    
def setPotentialWidth(val):
    potentialData['width']=val
    updatePotential()
    
def setPotentialHeight(val):
    potentialData['height']=val
    updatePotential()
    
def setPotentialSlope(val):
    potentialData['slope']=val**2
    updatePotential()
 
def setMethod(methodName):
    if(methodName == "$Crank\ Nicolson$"):
        params['method'] = schrodinger.crankNicolsonMethod
    else:
        params['method'] = schrodinger.naiveMethod

def play():
    params['paused']=False
    playButton.label.set_text("Pause")

def pause():
    params['paused']=True
    playButton.label.set_text("Play")

def playPause():
    if(params['paused']):
        play()
    else:
        pause()

def updateWavePacket():
    params['waveFunction'] = schrodinger.generateWavePacket(initialWaveData['x_offset'],
                                                            initialWaveData['momentum'],
                                                            initialWaveData['deviation'])
def playButtonClicked(e):
    playPause()

def setWaveOffset(val):
    pause()
    initialWaveData['x_offset'] = val
    updateWavePacket()

def setWaveEnergy(energy):
    pause()
    momentum = np.sqrt(2*energy)
    initialWaveData['momentum'] = energy
    updateWavePacket()
    
def setWaveDeviation(val):
    initialWaveData['deviation'] = val
    updateWavePacket()
    pause()

def resetButtonClicked(e):
    updateWavePacket()

def changePotentialWrap(x):
    if(params["periodicPotential"]):
        periodicPotentialButton.label.set_text("Use Periodic Boundary Conditions")
    else:
        periodicPotentialButton.label.set_text("Use Zero Boundary Conditions")
    params["periodicPotential"] = not params["periodicPotential"]

guiAxes = plt.axes([0.05, 0.6, 0.2, 0.3])
guiAxes.set_title("Potential:", loc="left")
potentialChooser = widgets.RadioButtons(guiAxes, potentials.potentialNames)
potentialChooser.on_clicked(setPotentialName)

guiAxes = plt.axes([0.05, 0.4, 0.2, 0.05])
guiAxes.set_title("X-Offset", loc="left")
xOffsetChooser = widgets.Slider(guiAxes, "", -20, 20, 0)
xOffsetChooser.on_changed(setPotentialOffset)

guiAxes = plt.axes([0.05, 0.3, 0.2, 0.05])
guiAxes.set_title("Potential Width", loc="left")
widthChooser = widgets.Slider(guiAxes, "", 1, 20, 10)
widthChooser.on_changed(setPotentialWidth)


guiAxes = plt.axes([0.05, 0.2, 0.2, 0.05])
guiAxes.set_title("Potential Height", loc="left")
heightChooser = widgets.Slider(guiAxes, "", -1, 5, .5)
heightChooser.on_changed(setPotentialHeight)

guiAxes = plt.axes([0.05, 0.1, 0.2, 0.05])
guiAxes.set_title("Potential Slope", loc="left")
slopeChooser = widgets.Slider(guiAxes, "", 0.01, 0.5, .1)
slopeChooser.on_changed(setPotentialSlope)

guiAxes = plt.axes([0.75, 0.7, 0.2, 0.15])
guiAxes.set_title("Method", loc="left")
methodChooser = widgets.RadioButtons(guiAxes, [r"""$Na\ddot ive\ Method$""", r"""$Crank\ Nicolson$"""])
methodChooser.on_clicked(setMethod)

guiAxes = plt.axes([0.75, 0.6, 0.2, 0.05])
guiAxes.set_title("Wave Packet Offset", loc="left")
waveOffsetChooser = widgets.Slider(guiAxes, "", -20, 20, 0)
waveOffsetChooser.on_changed(setWaveOffset)


guiAxes = plt.axes([0.75, 0.5, 0.2, 0.05])
guiAxes.set_title("Wave Energy", loc="left")
waveMomentumChooser = widgets.Slider(guiAxes, "", 0, 10, 0)
waveMomentumChooser.on_changed(setWaveEnergy)

guiAxes = plt.axes([0.75, 0.4, 0.2, 0.05])
guiAxes.set_title("Wave Deviation", loc="left")
waveDeviationChooser = widgets.Slider(guiAxes, "", 0.01, .9, 0.4)
waveDeviationChooser.on_changed(setWaveDeviation)


guiAxes = plt.axes([0.75, 0.3, 0.1, 0.05])
playButton = widgets.Button(guiAxes, "Pause")
playButton.on_clicked(playButtonClicked)

guiAxes = plt.axes([0.85, 0.3, 0.1, 0.05])
resetButton = widgets.Button(guiAxes, "Reset")
resetButton.on_clicked(resetButtonClicked)


guiAxes = plt.axes([0.75, 0.1, 0.25, 0.05])
periodicPotentialButton = widgets.Button(guiAxes, "Use Zero Boundary Conditions")
periodicPotentialButton.on_clicked(changePotentialWrap)


def animate(j, params):
    if(not params['paused']):
        params['waveFunction'] = params['method'](params['waveFunction'], 
                                                  params['potential'], 
                                                  params['periodicPotential'])
    realPlot.set_ydata([i.real for i in params['waveFunction']])
    imPlot  .set_ydata([i.imag for i in params['waveFunction']])
    probPlot.set_ydata([abs(i) for i in params['waveFunction']])


if __name__ == "__main__":
    anim = animation.FuncAnimation(figure, animate, fargs=(params,))
    
    plt.show()
