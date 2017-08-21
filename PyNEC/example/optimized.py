#
#  Automatically tune antenna
#
import monopole
import scipy.optimize
import numpy as np
from antenna_util import reflection_coefficient

# A function that will be minimized when the impedance is 50 Ohms
# We convert the height and antenna length to positive
# numbers using exp. because otherwise the antenna will lie
# below ground and cause an error in simulation.
def target(x):
  global freq
  base_height = np.exp(x[0]) # Make it positive
  length = np.exp(x[1])  # Make it positive
  z = monopole.impedance(freq, base_height, length)
  return reflection_coefficient(z, z0=50.0)
  

# Starting value 
freq = 134.5
x0 = [-2.0, 0.0]
# Carry out the minimization
log_base, log_length = scipy.optimize.fmin(target, x0)

base_height = np.exp(log_base)
length = np.exp(log_length)

print "Optimium base_height=%fm, h=%fm, impedance=%s Ohms" % \
  (base_height, length, monopole.impedance(freq, base_height, length))
