
import numpy as np
import numpy.matlib as matlib

dt = 0.08
dx = dt
boundaryConditions = (-45, 45)

def finiteDifferenceEquation(ps, V):
        totalSteps = int((boundaryConditions[1] - boundaryConditions[0])/dt)
        systemMatrix = matlib.zeros((totalSteps, totalSteps), complex) #matrix for system of eq
        u = -1
        x = boundaryConditions[0]
        systemVector = matlib.zeros(shape=(totalSteps))


        #create system of equations x
        for i in range(totalSteps):
                systemMatrix[i, u] = dt/(1j*(dx ** 2))
                systemMatrix[i, u + 1] = V(u + 1) - 2*dt/(1j*(dx ** 2))
                systemMatrix[i, u + 2] = dt/(1j*(dx ** 2))

                systemVector[i] = psi(x)
                u += 1
                x += dx

        print systemMatrix
        print systemVector





def psi(x):
        return x

def potential(x):
        return x

def main():
        finiteDifferenceEquation(psi, potential);

if __name__ == "__main__":
            main()


