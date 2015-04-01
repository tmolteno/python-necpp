import monopole
import scipy.optimize
import numpy as np

# A function that will be minimized when the impedance is 50 Ohms
# We convert the height and antenna length to positive
# numbers using exp. because otherwise the antenna will lie
# below ground and cause an error in simulation.
def target(x):
  freq = 34.5
  height = np.exp(x[0]) # Make it positive
  length = np.exp(x[1])  # Make it positive
  z = monopole.impedance(freq, height, length)
  return np.abs(z - 50.0)
  

# Starting value 
x0 = [-1.0, 1.5]
opt_height, opt_length = scipy.optimize.fmin(target, x0)

ant_height = np.exp(opt_height)
ant_length = np.exp(opt_length)
ant_impedance = monopole.impedance(34.5, ant_height, ant_length)
print "Tuned z0=%fm, h=%fm, impedance=%s Ohms" % \
    (ant_height, ant_length, ant_impedance)