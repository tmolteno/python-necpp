#
#  Plot of reflection coefficient vs antenna length for a fixed base height.
#
import monopole
import numpy as np
import pylab as plt
from antenna_util import reflection_coefficient

lengths = np.linspace(0.2, 5.0, 270)
reflections = []
z0 = 50

for l in lengths:
  freq = 134.5
  z = monopole.impedance(freq, base=0.5, length=l)
  reflections.append(reflection_coefficient(z, z0))
 
plt.plot(lengths, reflections)
plt.xlabel("Antenna length (m)")
plt.ylabel("Reflection coefficient")
plt.title("Reflection coefficient vs length (base_height=0.5m)")
plt.grid(True)
plt.show()
plt.savefig("reflection_coefficient.png")

