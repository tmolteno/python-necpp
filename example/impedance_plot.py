#
#  Plot of reflection coefficient vs antenna length for a fixed base height.
#
import monopole
import numpy as np
import pylab as plt

def reflection_coefficient(base_height, length, z0):
  freq = 134.5
  z = monopole.impedance(freq, base_height, length)
  return np.abs((z - z0) / (z + z0))

lengths = np.linspace(1.0, 8.0, 170)
reflections = []
z0 = 50

for l in lengths:
  reflections.append(reflection_coefficient(base_height=0.5, length=l, z0=z0))
 
plt.plot(lengths, reflections)
plt.xlabel("Antenna length (m)")
plt.ylabel("Reflection coefficient")
plt.title("Reflection coefficient vs length (base_height=0.5m)")
plt.grid(True)
plt.savefig("reflection_coefficient.png")

