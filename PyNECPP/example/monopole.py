#
#  Simple vertical monopole antenna simulation using python-necpp
#  pip install necpp
#
from PyNEC import *

from context_clean import *

import math

def geometry(freq, base, length):
  conductivity = 1.45e6 # Stainless steel
  ground_conductivity = 0.002
  ground_dielectric = 10

  wavelength = 3e8/(1e6*freq)
  n_seg = int(math.ceil(50*length/wavelength))

  nec = context_clean(nec_context())

  geo = nec.get_geometry()
  geo.wire(1, n_seg, 0, 0, base, 0, 0, base+length, 0.002, 1.0, 1.0)
  nec.geometry_complete(1)

  nec.set_all_wires_conductivity(conductivity)

  nec.set_finite_ground(ground_dielectric, ground_conductivity)
  nec.set_frequency(freq)

  # Voltage excitation one third of the way along the wire
  nec.voltage_excitation(wire_tag=1, segment_nr=int(n_seg/3), voltage=1.0)

  return nec

def impedance(freq, base, length):
  nec = geometry(freq, base, length)
  nec.xq_card(0) # Execute simulation

  index = 0

  ipt = nec.get_input_parameters(index)
  z = ipt.get_impedance()

  return z

if (__name__ == '__main__'):
  z = impedance(freq = 134.5, base = 0.5, length = 4.0)
  print "Impedance at base=%0.2f, length=%0.2f : (%6.1f,%+6.1fI) Ohms" % (0.5, 4.0, z.real, z.imag)
