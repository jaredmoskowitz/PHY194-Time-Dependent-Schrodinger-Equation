import numpy as np
import helpers, os, sys
import time
#import potentials

dt = .08
dx = dt
boundaryConditions = (-2, 2)
totalSteps = int((boundaryConditions[1] - boundaryConditions[0])/dx)

def finiteDifferenceEquation(psi, V):

        #normalize at each step
        psi = normalize(psi)

        systemMatrix = np.zeros((totalSteps, totalSteps), complex) #matrix for system of eq
        x = boundaryConditions[0]

        coeff =  dt/(1j*(dx ** 2))
        #create system of equations x
        for i in range(totalSteps):
                systemMatrix[i, (i - 1)%totalSteps] = coeff
                systemMatrix[i, (i)%totalSteps] = (V(x)*(dx ** 2) - 2)*coeff
                systemMatrix[i, (i + 1)%totalSteps] = coeff
                x += dx
        return normalize(np.linalg.solve(systemMatrix, psi))

def crankNicolson(psi, V):
        '''
        systemMatrix = np.zeros((totalSteps, totalSteps), complex) #matrix for system of eq
        x = boundaryConditions[0]

        coeff =  1j*dt/(2*(dx ** 2))
       #create system of equations x
        for i in range(totalSteps):
                systemMatrix[i, (i - 1)%totalSteps] = coeff
                systemMatrix[i, (i)%totalSteps] = (V(x)*(dx ** 2) - 2)*coeff
                systemMatrix[i, (i + 1)%totalSteps] = coeff
                x += dx
        return np.linalg.solve(systemMatrix, psi)

        '''
        ham = lambda x: -1*(1/dx ** 2) + V(x)
        exponential = lambda x: (1-0.5*1j*ham(x)*dt)/(1+0.5*1j*ham(x)*dt)
        for x in range(len(psi)):
                psi[x] = psi[x]*exponential(x)
        return psi

def generateWavePacket( x0, k0, sigma):
         psi = lambda x: np.exp(.25*(x-x0)*complex((x0-x)*sigma ** 2, 4*k0)*np.sqrt(np.pi)*sigma/np.sqrt(np.sqrt(2)*np.pi ** 3/2 * sigma))
         return np.array([psi(x*dx+boundaryConditions[0]) for x in range(totalSteps)])

def normalize(psi):
        alpha = (1/(sum(psi)*len(psi)*dx)) * (0.5)
        return [elem*alpha for elem in psi]

def main():
        ps = generateWavePacket(float(sys.argv[1]), float(sys.argv[2]), float(sys.argv[3]))
        print ps[:10]
        potential = helpers.flatWell
        for i in range(10):
                ps = crankNicolson(ps, potential)
                print ps[:10]
                time.sleep(1)

if __name__ == "__main__":
            main()


