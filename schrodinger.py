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
from scipy.sparse import csc_matrix
from scipy.sparse import csr_matrix
from scipy.sparse import identity
import scipy.sparse.linalg as sparse_linalg

dt = 0.8
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
def naiveMethod(psi, V, periodicPotential):


        #matrix for system of eq
        #systemMatrix = np.zeros((totalSteps, totalSteps), complex)
        rowIndices = []
        colIndices = []
        data       = []
        x = boundaryConditions[0]

        coeff =  1j*dt/(dx ** 2)
        #create system of equations where each row in the matrix
        #corrseponds to the at a given x
        for i in range(totalSteps):
                rowIndices += [i,i,i]
                colIndices += [(i - 1)%totalSteps, (i)%totalSteps, (i + 1)%totalSteps]
                data       += [coeff, (V(x)*(dx ** 2) - 2)*coeff, coeff]
                x += dx
        if(not periodicPotential):
            # The first and last elements of data are the wrapping elements. 
            # So if it doesn't wrap, set them to 0
            data[0]  = 0
            data[-1] = 0
        
        mat=csc_matrix((np.array(data), (np.array(rowIndices), np.array(colIndices))))
        return normalizeNPArray(sparse_linalg.spsolve(mat, psi))


'''
Uses the Crank-Nicolson method to solve the TDSE for a given potential V and
wave function psi for a certain timestep

parameters:
        psi - vector of complex values
        V - python function dependent that takes x as a parameter

return:
        psi one step forward in time (vector of complex values)
'''

def initializeHamiltonian(V, size):
    rowIndices = []
    colIndices = []
    data       = []
    coeffMatrix = [1/(dx**2), -2/dx**2, 1/dx**2]
    
    x = boundaryConditions[0]
    
    for i in range(size):
        colIndices += [(i-1)%size,  i, (i+1)%size]
        rowIndices += [i,  i, i]
        
        data       += [1j*dt*.5*coeffMatrix[0],
                       1j*dt*.5*(coeffMatrix[1] + V(x)),
                       1j*dt*.5*coeffMatrix[2]]
        x+=dx
    return (np.array(data), np.array(rowIndices),np.array(colIndices))
    
            
def sparseCrankNicolsonMethod(psi, V):


        data, rowIndices, colIndices = initializeHamiltonian(V, totalSteps)
        for i in range(len(data)):
            if((i-1)%3 == 0):
                data[i] = 1+data[i]
        hB = csc_matrix((data, (rowIndices, colIndices)), dtype=complex)
        
        for i in range(len(data)):
            if((i-1)%3 == 0):
                data[i] = 2-data[i]
            else:
                data[i] = -data[i]
        hA = csc_matrix((data, (rowIndices, colIndices)), dtype=complex)
        
        
        hC = hA*sparse_linalg.inv(hB)
        newPsi = sparse_linalg.spsolve(hC, psi)
        print newPsi[:10]
        return newPsi
    
def crankNicolsonMethod(psi, V, periodicPotential):
    
    H = diags([1, -2, 1], [-1, 0, 1], totalSteps)
    
    #account for wrapping if periodic
    if(periodicPotential):
        H[0, totalSteps - 1] = 1
        H[totalSteps - 1, 0] = 1
    
    H = H/(dx ** 2)
    
    potential = np.zeros((totalSteps, totalSteps), complex) #matrix for system of eq
    x = boundaryConditions[0]
    for i in range(totalSteps):
        potential[i, i] = V(x)
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
def normalizeList(psi):
        alpha = (1/np.sqrt(dx*sum([x**2 for x in psi])))
        return [elem*alpha for elem in psi]
    
def normalizeNPArray(psi):
        s = 0
        for x in psi:
            s+=x**2
        alpha = 1/np.sqrt(dx*s)
        for i in range(len(psi)):
            psi[i]*=alpha
        return psi



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



