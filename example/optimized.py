import monopole
import scipy.optimize
import numpy as np

# A function that will be minimized when the impedance is 50 Ohms
def target(x):
  freq = 34.5
  z0 = np.exp(x[0]) # Make it positive
  height = np.exp(x[1])  # Make it positive
  z = monopole.impedance(freq, z0, height)
  return np.abs(z - 50.0)
  

# Starting value 
x0 = [-1.0, 1.5]

z0, height = scipy.optimize.fmin(target, x0)

print "Optimium z0=%fm, h=%fm, impedance=%s Ohms" % (np.exp(z0), np.exp(height), monopole.impedance(34.5, z0, height))