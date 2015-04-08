import monopole
import scipy.optimize
import numpy as np

# A function that will be minimized when the impedance is 50 Ohms
def target(x):
  freq = 34.5
  base_height = np.exp(x[0]) # Make it positive
  length = np.exp(x[1])  # Make it positive
  z = monopole.impedance(freq, base_height, length)
  return np.abs(z - 50.0)
  

# Starting value 
x0 = [-1.0, 1.5]
# Carry out the minimization
log_base, log_length = scipy.optimize.fmin(target, x0)

base_height = np.exp(log_base)
length = np.exp(log_length)

print "Optimium base_height=%fm, h=%fm, impedance=%s Ohms" % \
  (base_height, length, monopole.impedance(34.5, base_height, length))