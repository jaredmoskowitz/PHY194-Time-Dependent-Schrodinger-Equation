import numpy as np
import helpers, os, sys
#import potentials

dt = 1
dx = dt
boundaryConditions = (-45, 45)
totalSteps = int((boundaryConditions[1] - boundaryConditions[0])/dx)

def finiteDifferenceEquation(psi, V):
        systemMatrix = np.zeros((totalSteps, totalSteps), complex) #matrix for system of eq
        u = -1
        x = boundaryConditions[0]
        systemVector = np.zeros(totalSteps)


        #create system of equations x
        for i in range(totalSteps):
                systemMatrix[i, u%totalSteps] = dt/(1j*(dx ** 2))
                systemMatrix[i, (u + 1)%totalSteps] = V(u + 1) - 2*dt/(1j*(dx ** 2))
                systemMatrix[i, (u + 2)%totalSteps] = dt/(1j*(dx ** 2))

                systemVector[i] = psi[i]
                u += 1
                x += dx

        return np.linalg.solve(systemMatrix, systemVector)


def generateWavePacket( x0, k0, sigma):
         psi = lambda x: np.exp(.25*(x-x0)*complex((x0-x)*sigma ** 2, 4*k0)*np.sqrt(np.pi)*sigma/np.sqrt(np.sqrt(2)*np.pi ** 3/2 * sigma))
         return [psi((x*dx+boundaryConditions[0])) for x in range(totalSteps)]

def potential(x):
        return x

def main():
        ps = generateWavePacket(float(sys.argv[1]), float(sys.argv[2]), float(sys.argv[3]))
        potential = helpers.flatWell
        finiteDifferenceEquation(ps, potential);

if __name__ == "__main__":
            main()


