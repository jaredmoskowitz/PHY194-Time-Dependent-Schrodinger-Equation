''''
        animate.py

        Jared Moskowitz, Chase Crumbagh, & Nolan Hawkins
        04/08/15

        This file is the main program to be run, combining elements from
        schrodinger.py and potentials.py to show the animation of a wave function
        with control over the underlying potential, the method of solving, the initial
        wave packet, and the boundary conditions.
        Most of the code invvolves simply setting up the GUI elements, at the very bottom
        is the actual bit that runs the animation.

'''
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

# setup the intial parameters of the potential, the intial wave, and the overarching system
# start with a triangular well
potential = potentials.generateTriangularWell(0, 0.05)

# These data are changed by the potential GUI, on the left side of the screen,
# and when any of it is changed, it is used to generate a new potential with potentials.py
potentialData = {'name':'Triangular','x_offset':0, 'width':10, 'height':.5, 'slope':.1}

# These data are changed by the Wave GUI, on the right side of the screen,
# and when any of it is changed, the animation pauses and a new wave packet is generated
initialWaveData = {'x_offset':0, 'momentum':1.5, 'deviation':.5}

# These determine how the animation is working and all that jazz
params = {
        'potential':potential,
        'method':schrodinger.naiveMethod,
        'waveFunction':schrodinger.generateWavePacket(0,1.5,.5),
        'paused':False,
        'periodicPotential':True
        }


# Initialize GUI stuff from matplotlib
# Figure is the entire window, axes is the axes on which the wave function will be plotted
# figsize sets the windo to 12"x6", assuming the sccreen is 80dpi

figure, axes = plt.subplots(figsize=(12,6))

axes.set_xlim(boundaryConditions)
axes.set_ylim(-0.5, 3)

# Make room for the GUI elements
plt.subplots_adjust(left=0.3, right=0.7)

# xData is merely the coordinates on the x axis that matter
xData=[dx*i + boundaryConditions[0] for i in range(len(params['waveFunction']))]

# Initialize plots of the real, complex, and probability of the wave function ...
#plt.subplot(211)
realPlot, = axes.plot(xData, xData, 'r',  label="Real")
imPlot,   = axes.plot(xData, xData, 'b',  label="Imaginary")
probPlot, = axes.plot(xData, xData, 'k-', label="Probablility", linewidth=2)
#  And the plot of the potential
potPlot,  = axes.plot(xData, [abs(potential(x)) for x in xData], 'k:', label="Potential")
legend = axes.legend(loc='upper right', shadow=True)


# What follows is just a lot of GUI setup
# These functions are called by interactions with the matplotlib widgets
# which are set up directly below this section

# Called by any function that changes the parameters of the underlying potential
def updatePotential():
    potential = potentials.generatePotential(potentialData['name'], 
                                             potentialData['x_offset'],
                                             potentialData['width'], 
                                             potentialData['height'],
                                             potentialData['slope'])
    potPlot.set_ydata([abs(potential(x)) for x in xData])
    params['potential']=potential

# These functions are called by widgets that change the underlying potential

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

# This changes the method of solving the TISE  
def setMethod(methodName):
    if(methodName == "$Crank\ Nicolson$"):
        params['method'] = schrodinger.crankNicolsonMethod
    else:
        params['method'] = schrodinger.naiveMethod

# Functions determining whether to actively run the animation

def play():
    params['paused']=False
    playButton.label.set_text("Pause")

def pause():
    params['paused']=True
    playButton.label.set_text("Play")

def playButtonClicked(e):
    if(params['paused']):
        play()
    else:
        pause()

# This is called by any function that changes the inital parameters of the wave
def updateWavePacket():
    params['waveFunction'] = schrodinger.generateWavePacket(initialWaveData['x_offset'],
                                                            initialWaveData['momentum'],
                                                            initialWaveData['deviation'])

# These functions are called by widgets that change the inital parameters of the wace

def setWaveOffset(offset):
    pause()
    initialWaveData['x_offset'] = offset
    updateWavePacket()

def setWaveEnergy(energy):
    pause()
    momentum = np.sqrt(2*energy)
    initialWaveData['momentum'] = energy
    updateWavePacket()
    
def setWaveDeviation(deviation):
    initialWaveData['deviation'] = deviation
    updateWavePacket()
    pause()

def resetButtonClicked(e):
    updateWavePacket()

def changePotentialWrap(e):
    if(params["periodicPotential"]):
        periodicPotentialButton.label.set_text("Use Periodic Boundary Conditions")
    else:
        periodicPotentialButton.label.set_text("Use Zero Boundary Conditions")
    params["periodicPotential"] = not params["periodicPotential"]


# And here is the actual initializing of the various widgets.
# The coding is slightly repetitve but functionalizing doesn't make it much shorter
# Each block of code creates one GUI element, with the title describing
# adequately what it controls

guiAxes = plt.axes([0.05, 0.6, 0.2, 0.3])
guiAxes.set_title("Potential:", loc="left")
potentialChooser = widgets.RadioButtons(guiAxes, potentials.potentialNames, active = 1)
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
# I wanted the Umlaut
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


# And now, the actual animation code is rather short:

def animate(j, params):
    if(not params['paused']):
        params['waveFunction'] = params['method'](params['waveFunction'], 
                                                  params['potential'], 
                                                  params['periodicPotential'])
   
    # the xdata has already been set, so just update the y-data
    realPlot.set_ydata([i.real for i in params['waveFunction']])
    imPlot  .set_ydata([i.imag for i in params['waveFunction']])
    probPlot.set_ydata([abs(i) for i in params['waveFunction']])

# If this is the main program, run!
if __name__ == "__main__":
    anim = animation.FuncAnimation(figure, animate, fargs=(params,))
    
    plt.show()
