import numpy as np
import helpers, os, sys
import time
#import potentials

dt = 0.08
dx = dt
boundaryConditions = (-45, 45)
totalSteps = int((boundaryConditions[1] - boundaryConditions[0])/dx)

def finiteDifferenceEquation(psi, V):

        systemMatrix = np.zeros((totalSteps, totalSteps), complex) #matrix for system of eq
        x = boundaryConditions[0]

        coeff =  dt/(1j*(dx ** 2))
        #create system of equations x
        for i in range(totalSteps):
                systemMatrix[i, (i - 1)%totalSteps] = coeff
                systemMatrix[i, (i)%totalSteps] = (V(x)*(dx ** 2) - 2/(dx ** 2))*coeff
                systemMatrix[i, (i + 1)%totalSteps] = coeff

                x += dx

        return np.linalg.solve(systemMatrix, psi)


def generateWavePacket( x0, k0, sigma):
         psi = lambda x: np.exp(.25*(x-x0)*complex((x0-x)*sigma ** 2, 4*k0)*np.sqrt(np.pi)*sigma/np.sqrt(np.sqrt(2)*np.pi ** 3/2 * sigma))
         return np.array([psi((x*dx+boundaryConditions[0])) for x in range(totalSteps)])

def main():
        ps = np.array(generateWavePacket(float(sys.argv[1]), float(sys.argv[2]), float(sys.argv[3])))
        print ps[:10]
        potential = helpers.flatWell
        for i in range(10):
                ps = finiteDifferenceEquation(ps, potential)
                print ps[:10]
                time.sleep(1)

if __name__ == "__main__":
            main()


