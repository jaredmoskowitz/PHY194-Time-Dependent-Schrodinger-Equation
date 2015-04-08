''''
        schrodinger.py

        Jared Moskowitz, Chase Crumbagh, & Nolan Hawkins
        04/08/15

        This file contains the methods for generating a wave packet
        and nuerically solving the TDSE using a naive method
        and a Crank-Nicolson method for a given potential.

'''
import numpy as np
import os, sys, numpy.matlib, time
from scipy.sparse import diags

dt = 5
dx = 0.08
boundaryConditions = (-40, 40)
totalSteps = int((boundaryConditions[1] - boundaryConditions[0])/dx)

'''
Uses the finite difference scheme to solve the TDSE for a given potential V and
wave function psi for a certain timestep

parameters:
        psi - vector of complex values
        V - python function dependent that takes x as a parameter

return:
        psi one step forward in time (vector of complex values)

'''
def naiveMethod(psi, V):


        #matrix for system of eq
        systemMatrix = np.zeros((totalSteps, totalSteps), complex)
        x = boundaryConditions[0]

        coeff =  1j*dt/(dx ** 2)
        #create system of equations where each row in the matrix
        #corrseponds to the at a given x
        for i in range(totalSteps):
                systemMatrix[i, (i - 1)%totalSteps] = coeff
                systemMatrix[i, (i)%totalSteps] = (V(x)*(dx ** 2) - 2)*coeff
                systemMatrix[i, (i + 1)%totalSteps] = coeff
                x += dx

        return normalize(np.linalg.solve(systemMatrix, psi))


'''
Uses the Crank-Nicolson method to solve the TDSE for a given potential V and
wave function psi for a certain timestep

parameters:
        psi - vector of complex values
        V - python function dependent that takes x as a parameter

return:
        psi one step forward in time (vector of complex values)
'''
def crankNicolsonMethod(psi, V):


        H = diags([1, -2, 1], [-1, 0, 1], totalSteps)


        #account for wrapping
        H[0, totalSteps - 1] = 1
        H[totalSteps - 1, 0] = 1

        H = H/(dx ** 2)
        potential =  np.zeros((totalSteps, totalSteps), complex) #matrix for system of eq
        x = boundaryConditions[0]
        for i in range(totalSteps):
                potential[i, i%totalSteps] = V(x)
                x += dx

        H += potential
        I = np.matlib.identity(totalSteps, complex)
        hA = I - dt*1j*H/2
        hB = I + dt*1j*H/2
        hC = hA*np.linalg.inv(hB)

        return np.linalg.solve(hC, psi)

'''
generates a wave packet
parameters
        x0 - starting x value
        k0 - starting k value
        sigma
return
        wave function for a wave packet (vector of complex values)

'''
def generateWavePacket( x0, k0, sigma):
         psi = lambda x: np.exp(.25*(x-x0)*complex((x0-x)*sigma ** 2, 4*k0)*np.sqrt(np.pi)*sigma/np.sqrt(np.sqrt(2)*np.pi ** 3/2 * sigma))
         return np.array([psi(x*dx+boundaryConditions[0]) for x in range(totalSteps)])


'''

normalizes a given psi (vector of complex values) s.t.
the inner pruduct is 1

'''
def normalize(psi):
        alpha = (1/np.sqrt(dx*sum([x**2 for x in psi])))
        return [elem*alpha for elem in psi]



def diags(array, locations, width):
    matrix = np.zeros((width, width), complex)
    for i in range(width):
        for j in range(len(array)):
            if locations[j] <= 0:
                if i-locations[j]< width and i-locations[j]>= 0:
                    matrix[i - locations[j], i] = array[j]
            else:
                if i+locations[j]< width and i-locations[j]>= 0:
                    matrix[i, locations[j] + i] = array[j]
    return matrix



